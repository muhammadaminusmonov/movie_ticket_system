from app.domain.movie import Movie


class MovieRepository:

    def __init__(self, db):
        self.db = db

    def create(self, title: str, duration_minutes: int) -> Movie:
        movie = Movie(title=title, duration_minutes=duration_minutes)
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def get_by_id(self, movie_id) -> Movie | None:
        return self.db.query(Movie).filter_by(id=movie_id).first()

    def get_all(self) -> list[Movie]:
        return self.db.query(Movie).all()

    def update(self, movie_id, title: str = None, duration_minutes: int = None) -> Movie | None:
        movie = self.get_by_id(movie_id)
        if not movie:
            return None
        if title is not None:
            movie.title = title
        if duration_minutes is not None:
            movie.duration_minutes = duration_minutes
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete(self, movie_id) -> bool:
        movie = self.get_by_id(movie_id)
        if not movie:
            return False
        self.db.delete(movie)
        self.db.commit()
        return True