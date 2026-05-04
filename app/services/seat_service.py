from app.core.redis import redis_client

SEAT_LOCK_TTL = 300  # 5 minutes


class SeatService:

    def _key(self, seat_id: str, show_id: str) -> str:
        return f"seat_lock:{show_id}:{seat_id}"

    def lock_seat(self, seat_id: str, show_id: str, user_id: str) -> bool:
        """
        Atomically lock a seat using Redis SET NX (set-if-not-exists).

        SET NX is a single atomic command — no race condition possible.
        If two requests arrive simultaneously, exactly one will get True.
        """
        key = self._key(seat_id, show_id)
        result = redis_client.set(key, user_id, ex=SEAT_LOCK_TTL, nx=True)
        return result is not None  # SET NX returns None if key already existed

    def is_seat_locked_by(self, seat_id: str, show_id: str, user_id: str) -> bool:
        """Check that the seat is locked specifically by this user (validates ownership)."""
        key = self._key(seat_id, show_id)
        locked_by = redis_client.get(key)
        return locked_by == user_id

    def release_seat(self, seat_id: str, show_id: str) -> None:
        key = self._key(seat_id, show_id)
        redis_client.delete(key)