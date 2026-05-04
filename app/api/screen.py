from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.deps import get_db, require_owner
from app.services.screen_service import ScreenService

router = APIRouter()


class ScreenCreateRequest(BaseModel):
    cinema_id: str
    name: str


class SeatCreateRequest(BaseModel):
    screen_id: str
    row: str
    number: int
    type: str = "STANDARD"


# ── Screens ──────────────────────────────────────────────────────────────────

@router.post("/", summary="Add a screen to a cinema (Owner)")
def create_screen(body: ScreenCreateRequest, db=Depends(get_db), _=Depends(require_owner)):
    try:
        return ScreenService(db).create_screen(cinema_id=body.cinema_id, name=body.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/cinema/{cinema_id}", summary="List screens in a cinema (Owner)")
def get_screens(cinema_id: str, db=Depends(get_db), _=Depends(require_owner)):
    return ScreenService(db).get_screens(cinema_id)


@router.delete("/{screen_id}", summary="Delete a screen (Owner)")
def delete_screen(screen_id: str, db=Depends(get_db), _=Depends(require_owner)):
    try:
        ScreenService(db).delete_screen(screen_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Seats (Configure Seats use case) ─────────────────────────────────────────

@router.post("/seats", summary="Add a seat to a screen (Owner)")
def add_seat(body: SeatCreateRequest, db=Depends(get_db), _=Depends(require_owner)):
    try:
        return ScreenService(db).add_seat(
            screen_id=body.screen_id,
            row=body.row,
            number=body.number,
            seat_type=body.type,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{screen_id}/seats", summary="List seats in a screen (Owner)")
def get_seats(screen_id: str, db=Depends(get_db), _=Depends(require_owner)):
    return ScreenService(db).get_seats(screen_id)


@router.delete("/seats/{seat_id}", summary="Delete a seat (Owner)")
def delete_seat(seat_id: str, db=Depends(get_db), _=Depends(require_owner)):
    try:
        ScreenService(db).delete_seat(seat_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))