from sqlalchemy.orm import Session

from app.repositories.cinema_repository import CinemaRepository
from app.repositories.user_repository import UserRepository
from app.domain.user import UserRole


class CinemaService:

    def __init__(self, db: Session):
        self.cinema_repo = CinemaRepository(db)
        self.user_repo = UserRepository(db)

    def create_cinema(self, name: str, location: str, owner_id: str) -> dict:
        # Validate owner exists and has OWNER role
        owner = self.user_repo.get_by_id(owner_id)
        if not owner:
            raise Exception("Owner not found")
        if owner.role not in (UserRole.OWNER, UserRole.ADMIN):
            raise Exception("Assigned user must have OWNER or ADMIN role")

        cinema = self.cinema_repo.create(name=name, location=location, owner_id=owner_id)
        return self._serialize(cinema)

    def get_all_cinemas(self) -> list[dict]:
        return [self._serialize(c) for c in self.cinema_repo.get_all()]

    def get_cinema(self, cinema_id: str) -> dict:
        cinema = self.cinema_repo.get_by_id(cinema_id)
        if not cinema:
            raise Exception("Cinema not found")
        return self._serialize(cinema)

    def get_my_cinemas(self, owner_id: str) -> list[dict]:
        return [self._serialize(c) for c in self.cinema_repo.get_by_owner(owner_id)]

    def update_cinema(self, cinema_id: str, name: str = None, location: str = None) -> dict:
        cinema = self.cinema_repo.update(cinema_id, name=name, location=location)
        if not cinema:
            raise Exception("Cinema not found")
        return self._serialize(cinema)

    def delete_cinema(self, cinema_id: str) -> None:
        deleted = self.cinema_repo.delete(cinema_id)
        if not deleted:
            raise Exception("Cinema not found")

    # ── Admin: Manage Cinema Owners (use case) ─────────────────────────────

    def assign_owner_role(self, user_id: str) -> dict:
        """Promote a CUSTOMER to OWNER role."""
        user = self.user_repo.update_role(user_id, UserRole.OWNER)
        if not user:
            raise Exception("User not found")
        return {"id": str(user.id), "name": user.name, "email": user.email, "role": user.role}

    def list_owners(self) -> list[dict]:
        users = self.user_repo.get_all()
        owners = [u for u in users if u.role == UserRole.OWNER]
        return [{"id": str(u.id), "name": u.name, "email": u.email, "role": u.role} for u in owners]

    def _serialize(self, cinema) -> dict:
        return {
            "id": str(cinema.id),
            "name": cinema.name,
            "location": cinema.location,
            "owner_id": str(cinema.owner_id),
        }