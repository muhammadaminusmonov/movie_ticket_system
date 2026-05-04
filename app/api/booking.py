from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import get_db, get_current_user, require_owner
from app.services.booking_service import BookingService
from app.repositories.booking_repository import BookingRepository

router = APIRouter()


@router.post("/checkout", summary="Checkout cart → create PENDING booking (Customer)")
def checkout(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    try:
        booking = BookingService(db).checkout(current_user["user_id"])
        return {
            "booking_id": str(booking.id),
            "show_id": str(booking.show_id),
            "status": booking.status,
            "total_price": float(booking.total_price),
        }
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/{booking_id}/cancel", summary="Cancel a booking (Customer)")
def cancel_booking(
    booking_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    try:
        booking = BookingService(db).cancel_booking(booking_id)
        return {"booking_id": str(booking.id), "status": booking.status}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/history", summary="View my booking history (Customer)")
def get_my_bookings(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    bookings = BookingRepository(db).get_by_user(current_user["user_id"])
    return [
        {
            "booking_id": str(b.id),
            "show_id": str(b.show_id),
            "status": b.status,
            "total_price": float(b.total_price),
            "created_at": b.created_at.isoformat(),
        }
        for b in bookings
    ]


@router.get("/show/{show_id}", summary="View all bookings for a show (Owner)")
def get_show_bookings(show_id: str, db=Depends(get_db), _=Depends(require_owner)):
    from app.domain.booking import Booking
    bookings = db.query(Booking).filter_by(show_id=show_id).all()
    return [
        {
            "booking_id": str(b.id),
            "user_id": str(b.user_id),
            "status": b.status,
            "total_price": float(b.total_price),
        }
        for b in bookings
    ]