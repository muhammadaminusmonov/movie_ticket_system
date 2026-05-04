from app.domain.cart import Cart, CartStatus
from app.domain.cart_item import CartItem


class CartRepository:

    def __init__(self, db):
        self.db = db

    def create_cart(self, user_id) -> Cart:
        cart = Cart(user_id=user_id)
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def get_active_cart(self, user_id) -> Cart | None:
        return (
            self.db.query(Cart)
            .filter_by(user_id=user_id, status=CartStatus.ACTIVE)
            .first()
        )

    def add_item(self, cart_id, seat_id, show_id, price) -> CartItem:
        item = CartItem(cart_id=cart_id, seat_id=seat_id, show_id=show_id, price=price)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_items(self, cart_id) -> list[CartItem]:
        return self.db.query(CartItem).filter_by(cart_id=cart_id).all()

    def checkout_cart(self, cart: Cart) -> None:
        cart.status = CartStatus.CHECKED_OUT
        self.db.commit()