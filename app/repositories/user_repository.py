from app.domain.user import User, UserRole


class UserRepository:

    def __init__(self, db):
        self.db = db

    def create(self, name: str, email: str, password_hash: str, role: UserRole = UserRole.CUSTOMER) -> User:
        user = User(name=name, email=email, password_hash=password_hash, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id) -> User | None:
        return self.db.query(User).filter_by(id=user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter_by(email=email).first()

    def get_all(self) -> list[User]:
        return self.db.query(User).all()

    def update_role(self, user_id, role: UserRole) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        user.role = role
        self.db.commit()
        self.db.refresh(user)
        return user