from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.domain.user import UserRole
from app.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, name: str, email: str, password: str, role: UserRole = UserRole.CUSTOMER) -> dict:
        existing = self.repo.get_by_email(email)
        if existing:
            raise Exception("Email already registered")

        user = self.repo.create(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=role,
        )
        token = create_access_token(str(user.id), user.role)
        return {"access_token": token, "token_type": "bearer", "user_id": str(user.id), "role": user.role}

    def login(self, email: str, password: str) -> dict:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise Exception("Invalid email or password")

        token = create_access_token(str(user.id), user.role)
        return {"access_token": token, "token_type": "bearer", "user_id": str(user.id), "role": user.role}

    def get_me(self, user_id: str) -> dict:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        return {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }