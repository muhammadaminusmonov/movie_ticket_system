from app.domain.payment import Payment


class PaymentRepository:

    def __init__(self, db):
        self.db = db

    def create(self, booking_id, amount, method) -> Payment:
        payment = Payment(booking_id=booking_id, amount=amount, method=method)
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_by_booking(self, booking_id) -> Payment | None:
        return self.db.query(Payment).filter_by(booking_id=booking_id).first()