from app.app_utils.jwt import JWT
from app.dao.base_dao import BaseDao
from app.models import User

class AuthDao(BaseDao):

    def __init__(self, session, model):
        BaseDao.__init__(self, session, model)

    async def authentication(self, credentials):
        user = await self.find(User, name=credentials.username)
        if not user:
            return False

        if not JWT.verify_password(credentials.password, user.hashed_password):
            return False

        return user





