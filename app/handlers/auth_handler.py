from fastapi import status, APIRouter, Request, Response, Depends
from fastapi.security import HTTPBasicCredentials
from starlette.exceptions import HTTPException

from app.app_utils.jwt import JWT
from app.dao.auth_dao import AuthDao
from app.dto.auth_dto import TokenPayload
from app.models import User
from app.settings import settings

router = APIRouter(tags=["auth"])

@router.get(
    "/auth",
    status_code=status.HTTP_200_OK,
    summary="Авторизация пользователя",
    description="""
    Авторизация пользователя по схеме Basic
    возвращает токен с персональными данными
    """
)
async def auth(
        response: Response,
        request: Request,
        credentials: HTTPBasicCredentials = Depends(JWT.security)
):
    async with request.app.state.db.get_master_session() as session:
        auth_dao = AuthDao(session=session, model=None)
        user: User = await auth_dao.authentication(credentials)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        token_pyload = TokenPayload(user_id=user.id, user_name=user.name)
        response.set_cookie(
            key=settings.TOKEN_ACCESS,
            value=JWT.create_token(token_pyload.dict()),
            secure=True
        )
    return {"status": "success"}
