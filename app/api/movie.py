from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.deps import get_db, get_current_user, require_owner
from app.services.movie_service import MovieService

router = APIRouter()


class MovieCreateRequest(BaseModel):
    title: str
    duration_minutes: int


class MovieUpdateRequest(BaseModel):
    title: str | None = None
    duration_minutes: int | None = None


@router.get("/", summary="Browse all movies (Customer)")
def get_movies(db=Depends(get_db)):
    return MovieService(db).get_all_movies()


@router.get("/{movie_id}", summary="Get movie details (Customer)")
def get_movie(movie_id: str, db=Depends(get_db)):
    try:
        return MovieService(db).get_movie(movie_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", summary="Add a new movie (Owner)")
def create_movie(body: MovieCreateRequest, db=Depends(get_db), _=Depends(require_owner)):
    return MovieService(db).create_movie(
        title=body.title,
        duration_minutes=body.duration_minutes,
    )


@router.put("/{movie_id}", summary="Edit a movie (Owner)")
def update_movie(movie_id: str, body: MovieUpdateRequest, db=Depends(get_db), _=Depends(require_owner)):
    try:
        return MovieService(db).update_movie(
            movie_id=movie_id,
            title=body.title,
            duration_minutes=body.duration_minutes,
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{movie_id}", summary="Delete a movie (Owner)")
def delete_movie(movie_id: str, db=Depends(get_db), _=Depends(require_owner)):
    try:
        MovieService(db).delete_movie(movie_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))