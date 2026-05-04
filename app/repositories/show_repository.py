from app.domain.show import Show


class ShowRepository:

    def __init__(self, db):
        self.db = db

    def create(self, movie_id, screen_id, start_time, end_time, price: float) -> Show:
        show = Show(
            movie_id=movie_id,
            screen_id=screen_id,
            start_time=start_time,
            end_time=end_time,
            price=price,
        )
        self.db.add(show)
        self.db.commit()
        self.db.refresh(show)
        return show

    def get_by_id(self, show_id) -> Show | None:
        return self.db.query(Show).filter_by(id=show_id).first()

    def get_by_movie(self, movie_id) -> list[Show]:
        return self.db.query(Show).filter_by(movie_id=movie_id).all()

    def get_all(self) -> list[Show]:
        return self.db.query(Show).all()

    def delete(self, show_id) -> bool:
        show = self.get_by_id(show_id)
        if not show:
            return False
        self.db.delete(show)
        self.db.commit()
        return True