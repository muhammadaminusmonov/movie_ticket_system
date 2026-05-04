from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.deps import get_db, get_current_user
from app.services.cart_service import CartService

router = APIRouter()


class AddToCartRequest(BaseModel):
    seat_id: str
    show_id: str
    price: float


@router.post("/add", summary="Add a seat to cart and lock it (Customer)")
def add_to_cart(
    body: AddToCartRequest,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    service = CartService(db)
    try:
        return service.add_to_cart(
            user_id=current_user["user_id"],
            seat_id=body.seat_id,
            show_id=body.show_id,
            price=body.price,
        )
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/", summary="Get current user's active cart (Customer)")
def get_cart(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    return CartService(db).get_cart(current_user["user_id"])