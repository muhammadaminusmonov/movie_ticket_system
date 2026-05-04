from sqlalchemy.orm import Session

from app.repositories.movie_repository import MovieRepository


class MovieService:

    def __init__(self, db: Session):
        self.repo = MovieRepository(db)

    def create_movie(self, title: str, duration_minutes: int) -> dict:
        movie = self.repo.create(title=title, duration_minutes=duration_minutes)
        return self._serialize(movie)

    def get_all_movies(self) -> list[dict]:
        return [self._serialize(m) for m in self.repo.get_all()]

    def get_movie(self, movie_id: str) -> dict:
        movie = self.repo.get_by_id(movie_id)
        if not movie:
            raise Exception("Movie not found")
        return self._serialize(movie)

    def update_movie(self, movie_id: str, title: str = None, duration_minutes: int = None) -> dict:
        movie = self.repo.update(movie_id, title=title, duration_minutes=duration_minutes)
        if not movie:
            raise Exception("Movie not found")
        return self._serialize(movie)

    def delete_movie(self, movie_id: str) -> None:
        deleted = self.repo.delete(movie_id)
        if not deleted:
            raise Exception("Movie not found")

    def _serialize(self, movie) -> dict:
        return {
            "id": str(movie.id),
            "title": movie.title,
            "duration_minutes": movie.duration_minutes,
        }