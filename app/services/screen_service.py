from sqlalchemy.orm import Session

from app.repositories.screen_repository import ScreenRepository
from app.repositories.seat_repository import SeatRepository
from app.domain.seat import SeatType


class ScreenService:

    def __init__(self, db: Session):
        self.screen_repo = ScreenRepository(db)
        self.seat_repo = SeatRepository(db)

    # ── Screens ────────────────────────────────────────────────────────────

    def create_screen(self, cinema_id: str, name: str) -> dict:
        screen = self.screen_repo.create(name=name, cinema_id=cinema_id)
        return self._serialize_screen(screen)

    def get_screens(self, cinema_id: str) -> list[dict]:
        return [self._serialize_screen(s) for s in self.screen_repo.get_by_cinema(cinema_id)]

    def delete_screen(self, screen_id: str) -> None:
        deleted = self.screen_repo.delete(screen_id)
        if not deleted:
            raise Exception("Screen not found")

    # ── Seats (Configure Seats use case) ───────────────────────────────────

    def add_seat(self, screen_id: str, row: str, number: int, seat_type: str) -> dict:
        try:
            typed = SeatType(seat_type.upper())
        except ValueError:
            raise Exception(f"Invalid seat type '{seat_type}'. Must be STANDARD or VIP")

        seat = self.seat_repo.create(screen_id=screen_id, row=row, number=number, seat_type=typed)
        return self._serialize_seat(seat)

    def get_seats(self, screen_id: str) -> list[dict]:
        return [self._serialize_seat(s) for s in self.seat_repo.get_by_screen(screen_id)]

    def delete_seat(self, seat_id: str) -> None:
        deleted = self.seat_repo.delete(seat_id)
        if not deleted:
            raise Exception("Seat not found")

    def _serialize_screen(self, screen) -> dict:
        return {
            "id": str(screen.id),
            "name": screen.name,
            "cinema_id": str(screen.cinema_id),
        }

    def _serialize_seat(self, seat) -> dict:
        return {
            "id": str(seat.id),
            "screen_id": str(seat.screen_id),
            "row": seat.row,
            "number": seat.number,
            "type": seat.type,
        }