from sqlalchemy.orm import Session

from app.domain.payment import Payment, PaymentStatus
from app.repositories.payment_repository import PaymentRepository
from app.services.booking_service import BookingService


class PaymentService:
    """
    Follows the sequence diagram:
      pay(booking_id) → create Payment (INITIATED) → simulate gateway →
      on success: confirmBooking + mark Payment SUCCESS
      on failure:  cancelBooking + mark Payment FAILED
    """

    def __init__(self, db: Session):
        self.db = db
        self.payment_repo = PaymentRepository(db)
        self.booking_service = BookingService(db)

    def pay(self, booking_id: str, amount: float, method: str) -> Payment:
        # Create payment record in INITIATED state
        payment = self.payment_repo.create(
            booking_id=booking_id,
            amount=amount,
            method=method,
        )

        try:
            # --- Payment gateway call would go here ---
            # For now we simulate success (gateway returns True)
            gateway_success = True

            if gateway_success:
                payment.status = PaymentStatus.SUCCESS
                self.db.commit()
                self.booking_service.confirm_booking(booking_id)
            else:
                payment.status = PaymentStatus.FAILED
                self.db.commit()
                self.booking_service.cancel_booking(booking_id)

        except Exception:
            payment.status = PaymentStatus.FAILED
            self.db.commit()
            self.booking_service.cancel_booking(booking_id)
            raise

        self.db.refresh(payment)
        return payment