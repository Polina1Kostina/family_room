from fastapi import APIRouter, Depends
from family_room.auth.dependencies import current_superuser
from family_room.auth.models import User
from .tasks import send_email_invite_event


router = APIRouter(
    prefix='/email',
    tags=['email'],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
def send(email: str, sup_user: User = Depends(current_superuser)):
    send_email_invite_event.delay(email, event='')
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }
