from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.deps import get_db, get_current_user
from app.services.payment_service import PaymentService

router = APIRouter()


class PayRequest(BaseModel):
    booking_id: str
    amount: float
    method: str


@router.post("/pay", summary="Pay for a booking (Customer)")
def pay(
    body: PayRequest,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    try:
        payment = PaymentService(db).pay(
            booking_id=body.booking_id,
            amount=body.amount,
            method=body.method,
        )
        return {
            "payment_id": str(payment.id),
            "booking_id": str(payment.booking_id),
            "status": payment.status,
            "amount": float(payment.amount),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))