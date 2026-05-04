from fastapi import APIRouter, HTTPException

from app.services.seat_service import SeatService

router = APIRouter()
seat_service = SeatService()


@router.post("/lock")
def lock_seat(seat_id: str, show_id: str, user_id: str):
    success = seat_service.lock_seat(seat_id, show_id, user_id)
    if not success:
        raise HTTPException(status_code=409, detail="Seat already locked")
    return {"success": True}


@router.delete("/lock")
def release_seat(seat_id: str, show_id: str):
    seat_service.release_seat(seat_id, show_id)
    return {"success": True}