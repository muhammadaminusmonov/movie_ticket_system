from app.domain.booking import Booking


class BookingRepository:

    def __init__(self, db):
        self.db = db

    def get_by_id(self, booking_id) -> Booking | None:
        return self.db.query(Booking).filter_by(id=booking_id).first()

    def get_by_user(self, user_id) -> list[Booking]:
        return self.db.query(Booking).filter_by(user_id=user_id).all()