from sqlalchemy.orm import Session

from app.repositories.show_repository import ShowRepository
from app.repositories.seat_repository import SeatRepository
from app.core.redis import redis_client


class ShowService:

    def __init__(self, db: Session):
        self.show_repo = ShowRepository(db)
        self.seat_repo = SeatRepository(db)
        self.db = db

    def create_show(self, movie_id, screen_id, start_time, end_time, price) -> dict:
        show = self.show_repo.create(
            movie_id=movie_id,
            screen_id=screen_id,
            start_time=start_time,
            end_time=end_time,
            price=price,
        )
        return self._serialize(show)

    def get_all_shows(self) -> list[dict]:
        return [self._serialize(s) for s in self.show_repo.get_all()]

    def get_show(self, show_id: str) -> dict:
        show = self.show_repo.get_by_id(show_id)
        if not show:
            raise Exception("Show not found")
        return self._serialize(show)

    def get_shows_by_movie(self, movie_id: str) -> list[dict]:
        return [self._serialize(s) for s in self.show_repo.get_by_movie(movie_id)]

    def get_available_seats(self, show_id: str) -> list[dict]:
        """
        Returns all seats for the show's screen, annotated with available: true/false.
        Frontend uses this to render the seat-picker.

        A seat is unavailable if EITHER:
          - it has a Redis lock (someone is currently in the 5-min booking window), OR
          - it has a CONFIRMED or PENDING booking_seat record in the DB
            (permanent — Redis TTL is irrelevant for these)
        """
        from app.domain.booking_seat import BookingSeat
        from app.domain.booking import Booking, BookingStatus

        show = self.show_repo.get_by_id(show_id)
        if not show:
            raise Exception("Show not found")

        # Seats permanently taken (CONFIRMED or PENDING bookings in DB)
        booked_seat_ids = {
            str(bs.seat_id)
            for bs in (
                self.db.query(BookingSeat)
                .join(Booking, BookingSeat.booking_id == Booking.id)
                .filter(
                    BookingSeat.show_id == show_id,
                    Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING]),
                )
                .all()
            )
        }

        seats = self.seat_repo.get_by_screen(str(show.screen_id))
        result = []
        for seat in seats:
            seat_id_str = str(seat.id)
            # Check Redis lock (temporary — someone is mid-checkout)
            redis_key = f"seat_lock:{show_id}:{seat.id}"
            redis_locked = redis_client.exists(redis_key) == 1
            # Check DB (permanent booking)
            db_booked = seat_id_str in booked_seat_ids

            result.append({
                "id": seat_id_str,
                "row": seat.row,
                "number": seat.number,
                "type": seat.type,
                "available": not (redis_locked or db_booked),
            })
        return result

    def delete_show(self, show_id: str) -> None:
        deleted = self.show_repo.delete(show_id)
        if not deleted:
            raise Exception("Show not found")

    def _serialize(self, show) -> dict:
        return {
            "id": str(show.id),
            "movie_id": str(show.movie_id),
            "screen_id": str(show.screen_id),
            "start_time": show.start_time.isoformat(),
            "end_time": show.end_time.isoformat(),
            "price": float(show.price),
        }