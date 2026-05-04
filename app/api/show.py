from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.deps import get_db, require_owner
from app.services.show_service import ShowService

router = APIRouter()


class ShowCreateRequest(BaseModel):
    movie_id: str
    screen_id: str
    start_time: datetime
    end_time: datetime
    price: float


@router.get("/", summary="List all shows (Customer)")
def get_all_shows(db=Depends(get_db)):
    return ShowService(db).get_all_shows()


@router.get("/{show_id}", summary="Get show details (Customer)")
def get_show(show_id: str, db=Depends(get_db)):
    try:
        return ShowService(db).get_show(show_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/movie/{movie_id}", summary="View showtimes for a movie (Customer)")
def get_shows_by_movie(movie_id: str, db=Depends(get_db)):
    return ShowService(db).get_shows_by_movie(movie_id)


@router.get("/{show_id}/seats", summary="Get available seats for a show (Customer)")
def get_available_seats(show_id: str, db=Depends(get_db)):
    """
    Returns all seats for this show annotated with available: true/false.
    Frontend uses this to render the seat-picker UI.
    """
    try:
        return ShowService(db).get_available_seats(show_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", summary="Schedule a new show (Owner)")
def create_show(body: ShowCreateRequest, db=Depends(get_db), _=Depends(require_owner)):
    try:
        return ShowService(db).create_show(
            movie_id=body.movie_id,
            screen_id=body.screen_id,
            start_time=body.start_time,
            end_time=body.end_time,
            price=body.price,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{show_id}", summary="Delete a show (Owner)")
def delete_show(show_id: str, db=Depends(get_db), _=Depends(require_owner)):
    try:
        ShowService(db).delete_show(show_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))