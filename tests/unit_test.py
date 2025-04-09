import pytest
from httpx import AsyncClient

from app.app_utils.jwt import JWT
from app.models import User, Image
from app.settings import settings
from tests.test_dto import FileBody, AuthBody


class TestApi:
    token = None

    @pytest.mark.asyncio
    async def test_auth(
        self,
        _client: AsyncClient,
        mock_body,
        mock_factory_for_find
    ):
        body = mock_body(AuthBody)
        mock_factory_for_find(User, "app.dao.auth_dao.AuthDao.find", **body.dict())

        response = await _client.get(
            url=f"local/api/v1/auth",
            auth=(body.name, body.password)
        )
        TestApi.token = response.cookies.get(settings.TOKEN_ACCESS)
        payload = JWT.validate_token(TestApi.token)

        assert response.status_code == 200
        assert body.id == payload.get("user_id")
        assert body.name == payload.get("user_name")


    @pytest.mark.asyncio
    async def test_upload_file(
        self,
        _client: AsyncClient,
        mock_body,
        mock_factory_for_find
    ):
        body: FileBody = mock_body(FileBody)

        response = await _client.post(
            url=f"local/api/v1/image/",
            files={"file_body": (body.name, body.content, "image/png")},
            cookies={settings.TOKEN_ACCESS: TestApi.token}
        )

        assert response.status_code == 200
        assert response.json().get("file_name_hash") == body.name_hash

    @pytest.mark.asyncio
    async def test_download_file(
        self,
        _client: AsyncClient,
        mock_body,
        mock_factory_for_find
    ):
        body: FileBody = mock_body(FileBody)
        mock_factory_for_find(Image, "app.dao.image_dao.ImageDao.find", **body.dict())

        response = await _client.get(
            url=f"local/api/v1/image/{body.name_hash}",
            cookies={settings.TOKEN_ACCESS: TestApi.token}
        )
        assert response.status_code == 200
        assert response.content == body.content


    @pytest.mark.asyncio
    async def test_delete_file(
        self,
        _client: AsyncClient,
        mock_body,
        mock_factory_for_find
    ):
        body: FileBody = mock_body(FileBody)
        mock_factory_for_find(Image, "app.dao.image_dao.ImageDao.find", **body.dict())

        response = await _client.delete(
            url=f"local/api/v1/image/{body.name_hash}",
            cookies={settings.TOKEN_ACCESS: TestApi.token}
        )

        assert response.status_code == 200
        assert response.json().get("status") == "success"
