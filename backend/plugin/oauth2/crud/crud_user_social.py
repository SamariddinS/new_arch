from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.oauth2.model import UserSocial
from backend.plugin.oauth2.schema.user_social import CreateUserSocialParam


class CRUDUserSocial(CRUDPlus[UserSocial]):
    """User social account database operations"""

    async def check_binding(self, db: AsyncSession, pk: int, source: str) -> UserSocial | None:
        """
        Check system user social account binding

        :param db: Database session
        :param pk: User ID
        :param source: Social account type
        :return:
        """
        return await self.select_model_by_column(db, user_id=pk, source=source)

    async def get_by_sid(self, db: AsyncSession, sid: str, source: str) -> UserSocial | None:
        """
        Get social user by SID

        :param db: Database session
        :param sid: Third-party user ID
        :param source: Social account type
        :return:
        """
        return await self.select_model_by_column(db, sid=sid, source=source)

    async def create(self, db: AsyncSession, obj: CreateUserSocialParam) -> None:
        """
        Create user social account binding

        :param db: Database session
        :param obj: Create user social account binding parameters
        :return:
        """
        await self.create_model(db, obj)

    async def delete(self, db: AsyncSession, social_id: int) -> int:
        """
        Delete user social account binding

        :param db: Database session
        :param social_id: Social account binding ID
        :return:
        """
        return await self.delete_model(db, social_id)


user_social_dao: CRUDUserSocial = CRUDUserSocial(UserSocial)
