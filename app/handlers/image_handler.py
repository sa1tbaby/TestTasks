from fastapi import APIRouter, Depends, Request, File, UploadFile, HTTPException
from fastapi.responses import Response
from starlette import status

from app.app_utils.jwt import JWT
from app.dao.image_dao import ImageDao
from app.dto.auth_dto import TokenPayload
from app.dto.image_dto import ImageDto
from app.models import Image

router = APIRouter(tags=["image"], prefix="/image")


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Отправить фотографию"
)
async def upload_image(
        request: Request,
        file_body: UploadFile = File(...),
        payload: dict = Depends(JWT.authorization)
) -> ImageDto:
    async with request.app.state.db.get_master_session() as db_session:
        user_image_dao = ImageDao(session=db_session, model=Image)
        file_name_hash = await user_image_dao.upload_image(
            file_body=file_body,
            payload=payload
        )
        return ImageDto(file_name_hash=file_name_hash)


@router.get(
    "/{file_name}",
    status_code=status.HTTP_200_OK,
    summary="Получить фотографию",
)
async def download_image(
        request: Request,
        file_name: str,
        payload: TokenPayload = Depends(JWT.authorization)
):
    async with request.app.state.db.get_master_session() as db_session:
        user_image_dao = ImageDao(session=db_session, model=Image)
        file_metadata, file_content = await user_image_dao.download_image(file_name=file_name)
        return Response(
            content=file_content,
            media_type=file_metadata.type,
            headers={
                "Content-Disposition": f"attachment; filename={file_metadata.name_hash}"
            }
        )


@router.delete(
    "/{file_name}",
    status_code=status.HTTP_200_OK,
    summary="Удалить фотографию"
)
async def delete_image(
        request: Request,
        file_name: str,
        payload = Depends(JWT.authorization)
) -> dict:
    async with request.app.state.db.get_master_session() as db_session:
        user_image_dao = ImageDao(session=db_session, model=Image)
        if await user_image_dao.delete_image(payload=payload, file_name=file_name):
            return {"status": "success"}
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="access denied",
            )

