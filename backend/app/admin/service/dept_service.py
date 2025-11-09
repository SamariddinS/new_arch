from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_dept import dept_dao
from backend.app.admin.model import Dept
from backend.app.admin.schema.dept import CreateDeptParam, UpdateDeptParam
from backend.app.admin.schema.user import GetUserInfoWithRelationDetail
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.build_tree import get_tree_data


class DeptService:
    """Department service class"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Dept:
        """
        Get department details

        :param db: Database session
        :param pk: Department ID
        :return:
        """

        dept = await dept_dao.get(db, pk)
        if not dept:
            raise errors.NotFoundError(msg='Department does not exist')
        return dept

    @staticmethod
    async def get_tree(
        *,
        db: AsyncSession,
        request_user: GetUserInfoWithRelationDetail,
        name: str | None,
        leader: str | None,
        phone: str | None,
        status: int | None,
    ) -> list[dict[str, Any]]:
        """
        Get department tree structure

        :param db: Database session
        :param request_user: Request User
        :param name: Department name
        :param leader: Department leader
        :param phone: Contact phone
        :param status: Status
        :return:
        """

        dept_select = await dept_dao.get_all(db, request_user, name, leader, phone, status)
        tree_data = get_tree_data(dept_select)
        return tree_data

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateDeptParam) -> None:
        """
        Create department

        :param db: Database session
        :param obj: Department creation parameters
        :return:
        """
        dept = await dept_dao.get_by_name(db, obj.name)
        if dept:
            raise errors.ConflictError(msg='Department name already exists')
        if obj.parent_id:
            parent_dept = await dept_dao.get(db, obj.parent_id)
            if not parent_dept:
                raise errors.NotFoundError(msg='Parent department does not exist')
        await dept_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateDeptParam) -> int:
        """
        Update department

        :param db: Database session
        :param pk: Department ID
        :param obj: Department update parameters
        :return:
        """
        dept = await dept_dao.get(db, pk)
        if not dept:
            raise errors.NotFoundError(msg='Department does not exist')
        if dept.name != obj.name and await dept_dao.get_by_name(db, obj.name):
            raise errors.ConflictError(msg='Department name already exists')
        if obj.parent_id:
            parent_dept = await dept_dao.get(db, obj.parent_id)
            if not parent_dept:
                raise errors.NotFoundError(msg='Parent department does not exist')
        if obj.parent_id == dept.id:
            raise errors.ForbiddenError(msg='Cannot associate self as parent')
        count = await dept_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        Delete department

        :param db: Database session
        :param pk: Department ID
        :return:
        """
        dept = await dept_dao.get_with_relation(db, pk)
        if dept.users:
            raise errors.ConflictError(msg='Cannot delete department with users')
        children = await dept_dao.get_children(db, pk)
        if children:
            raise errors.ConflictError(msg='Cannot delete department with subdepartments')
        count = await dept_dao.delete(db, pk)
        for user in dept.users:
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
        return count


dept_service: DeptService = DeptService()
