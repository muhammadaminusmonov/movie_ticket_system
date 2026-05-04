from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domain.booking import Booking, BookingStatus
from app.domain.booking_seat import BookingSeat
from app.repositories.cart_repository import CartRepository
from app.services.seat_service import SeatService


class BookingService:

    def __init__(self, db: Session):
        self.db = db
        self.cart_repo = CartRepository(db)
        self.seat_service = SeatService()

    def checkout(self, user_id: str) -> Booking:
        """
        Convert an active cart into a PENDING booking.

        Concurrency safety:
        - Validates Redis lock ownership (seat still held by this user)
        - UniqueConstraint on booking_seats(seat_id, show_id) is the DB-level
          last line of defence against any concurrent race.
        """
        try:
            cart = self.cart_repo.get_active_cart(user_id)
            if not cart:
                raise Exception("No active cart found")

            items = self.cart_repo.get_items(cart.id)
            if not items:
                raise Exception("Cart is empty")

            # Validate every seat lock is still owned by this user
            for item in items:
                if not self.seat_service.is_seat_locked_by(
                    seat_id=str(item.seat_id),
                    show_id=str(item.show_id),
                    user_id=user_id,
                ):
                    raise Exception(
                        f"Seat lock expired for seat {item.seat_id}. "
                        "Please re-select your seats."
                    )

            total_price = sum(item.price for item in items)
            show_id = items[0].show_id

            # Single atomic transaction: Booking + BookingSeats + cart status
            booking = Booking(
                user_id=user_id,
                show_id=show_id,
                total_price=total_price,
                status=BookingStatus.PENDING,
            )
            self.db.add(booking)
            self.db.flush()  # get booking.id without committing yet

            for item in items:
                self.db.add(BookingSeat(
                    booking_id=booking.id,
                    seat_id=item.seat_id,
                    show_id=item.show_id,
                    price=item.price,
                ))

            # Mark cart as checked out (no commit inside — part of this transaction)
            cart.status = "CHECKED_OUT"
            self.db.commit()
            self.db.refresh(booking)
            return booking

        except IntegrityError:
            self.db.rollback()
            raise Exception("Seat already booked by another user (concurrent booking detected)")

    def confirm_booking(self, booking_id: str) -> Booking:
        booking = self.db.query(Booking).filter_by(id=booking_id).first()
        if not booking:
            raise Exception("Booking not found")
        booking.status = BookingStatus.CONFIRMED
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def cancel_booking(self, booking_id: str) -> Booking:
        booking = self.db.query(Booking).filter_by(id=booking_id).first()
        if not booking:
            raise Exception("Booking not found")

        # Bug 4 fix: guard against double-cancel
        if booking.status == BookingStatus.CANCELLED:
            raise Exception("Booking is already cancelled")

        booking.status = BookingStatus.CANCELLED

        # Release Redis locks so seats become available again
        # (no-op if TTL already expired, which is fine)
        for seat in booking.seats:
            self.seat_service.release_seat(
                seat_id=str(seat.seat_id),
                show_id=str(seat.show_id),
            )

        self.db.commit()
        self.db.refresh(booking)
        return booking