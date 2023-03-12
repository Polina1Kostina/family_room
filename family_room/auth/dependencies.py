from fastapi import Depends
import fastapi_users
from .manager import get_user_manager
from .auth import auth_backend
from .models import User


fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

current_superuser = fastapi_users.current_user(active=True, superuser=True)


def get_current_user(cur_user: User = Depends(current_user)):
    return cur_user
