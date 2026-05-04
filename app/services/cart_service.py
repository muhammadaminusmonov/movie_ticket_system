from app.services.seat_service import SeatService
from app.repositories.cart_repository import CartRepository


class CartService:

    def __init__(self, db):
        self.repo = CartRepository(db)
        self.seat_service = SeatService()

    def add_to_cart(self, user_id: str, seat_id: str, show_id: str, price: float):
        # Check if this user already has this seat locked (their own cart)
        if self.seat_service.is_seat_locked_by(seat_id, show_id, user_id):
            raise Exception("This seat is already in your cart")

        # Atomically lock the seat in Redis (SET NX)
        locked = self.seat_service.lock_seat(seat_id, show_id, user_id)
        if not locked:
            raise Exception("This seat is already reserved by another user")

        # DB operations — release Redis lock if anything fails
        try:
            cart = self.repo.get_active_cart(user_id)
            if not cart:
                cart = self.repo.create_cart(user_id)
            item = self.repo.add_item(cart.id, seat_id, show_id, price)
        except Exception:
            # Bug 3 fix: don't leak the Redis lock on DB failure
            self.seat_service.release_seat(seat_id, show_id)
            raise

        return {
            "cart_id": str(cart.id),
            "item_id": str(item.id),
        }

    def get_cart(self, user_id: str):
        cart = self.repo.get_active_cart(user_id)
        if not cart:
            return {"cart": None, "items": []}

        items = self.repo.get_items(cart.id)
        return {
            "cart_id": str(cart.id),
            "status": cart.status,
            "items": [
                {
                    "id": str(i.id),
                    "seat_id": str(i.seat_id),
                    "show_id": str(i.show_id),
                    "price": float(i.price),
                }
                for i in items
            ],
        }