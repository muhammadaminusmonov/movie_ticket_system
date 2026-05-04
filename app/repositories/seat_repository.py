from app.domain.seat import Seat, SeatType


class SeatRepository:

    def __init__(self, db):
        self.db = db

    def create(self, screen_id, row: str, number: int, seat_type: SeatType = SeatType.STANDARD) -> Seat:
        seat = Seat(screen_id=screen_id, row=row, number=number, type=seat_type)
        self.db.add(seat)
        self.db.commit()
        self.db.refresh(seat)
        return seat

    def get_by_id(self, seat_id) -> Seat | None:
        return self.db.query(Seat).filter_by(id=seat_id).first()

    def get_by_screen(self, screen_id) -> list[Seat]:
        return self.db.query(Seat).filter_by(screen_id=screen_id).all()

    def delete(self, seat_id) -> bool:
        seat = self.get_by_id(seat_id)
        if not seat:
            return False
        self.db.delete(seat)
        self.db.commit()
        return True