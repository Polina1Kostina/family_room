import fastapi_users
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .events.router import router as router_event
from .family.router import router as router_family
from .tasks.router import router as router_email
from .auth.auth import auth_backend
from .auth.manager import get_user_manager
from .auth.schemas import UserCreate, UserRead
from .auth.models import User

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


from redis import asyncio as aioredis


description = """
Family_room API поможет тебе создать пользователя и организовывать мероприятия. 🚀


## auth

Ты можешь:

* **Создать пользователя**.
* **Авторизоваться, чтобы выполнять другие запросы**.

## event

Ты можешь:

* **Создать мероприятие**.
* **Посмотреть данные мероприятия**.
* **Отредактировать своё мероприятие**.
* **Удалить своё мероприятие**.
* **Пригласить на своё мероприятие другого пользователя. Ему также придёт уведомление на почту**.
"""


app = FastAPI(
    title="FamilyRoomApp",
    description=description,
)

app.mount('/static', StaticFiles(directory='static'), name='static')


fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(router_event)
app.include_router(router_family)
app.include_router(router_email)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url(
        'redis://localhost', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
