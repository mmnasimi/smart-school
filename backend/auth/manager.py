from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin
from backend.models import User
from backend.database import get_user_db
from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy


SECRET = "Zxcvb1362"

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request=None):
        print(f"✅ کاربر جدید ثبت‌نام کرد: {user.email}")

# تابعی که به FastAPIUsers می‌دیم
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret="SECRET", lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

async def validate_password(password: str):
    if len(password) < 8:
        raise ValueError("رمز عبور باید حداقل ۸ کاراکتر باشد.")
    if not any(char.isdigit() for char in password):
        raise ValueError("رمز عبور باید حداقل یک عدد داشته باشد.")