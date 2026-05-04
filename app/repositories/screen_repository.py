from app.domain.screen import Screen


class ScreenRepository:

    def __init__(self, db):
        self.db = db

    def create(self, name: str, cinema_id) -> Screen:
        screen = Screen(name=name, cinema_id=cinema_id)
        self.db.add(screen)
        self.db.commit()
        self.db.refresh(screen)
        return screen

    def get_by_id(self, screen_id) -> Screen | None:
        return self.db.query(Screen).filter_by(id=screen_id).first()

    def get_by_cinema(self, cinema_id) -> list[Screen]:
        return self.db.query(Screen).filter_by(cinema_id=cinema_id).all()

    def delete(self, screen_id) -> bool:
        screen = self.get_by_id(screen_id)
        if not screen:
            return False
        self.db.delete(screen)
        self.db.commit()
        return True