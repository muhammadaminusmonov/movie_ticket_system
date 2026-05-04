from app.domain.cinema import Cinema


class CinemaRepository:

    def __init__(self, db):
        self.db = db

    def create(self, name: str, location: str, owner_id) -> Cinema:
        cinema = Cinema(name=name, location=location, owner_id=owner_id)
        self.db.add(cinema)
        self.db.commit()
        self.db.refresh(cinema)
        return cinema

    def get_by_id(self, cinema_id) -> Cinema | None:
        return self.db.query(Cinema).filter_by(id=cinema_id).first()

    def get_all(self) -> list[Cinema]:
        return self.db.query(Cinema).all()

    def get_by_owner(self, owner_id) -> list[Cinema]:
        return self.db.query(Cinema).filter_by(owner_id=owner_id).all()

    def update(self, cinema_id, name: str = None, location: str = None) -> Cinema | None:
        cinema = self.get_by_id(cinema_id)
        if not cinema:
            return None
        if name is not None:
            cinema.name = name
        if location is not None:
            cinema.location = location
        self.db.commit()
        self.db.refresh(cinema)
        return cinema

    def delete(self, cinema_id) -> bool:
        cinema = self.get_by_id(cinema_id)
        if not cinema:
            return False
        self.db.delete(cinema)
        self.db.commit()
        return True