from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.reference.schema.level import (
    CreateLevelParam,
    DeleteLevelParam,
    GetLevelDetail,
    UpdateLevelParam,
)
from backend.app.reference.service.level_service import level_service
from backend.common.list import LabelValue
from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/{pk}', summary='Get Skill/experience level reference details', dependencies=[DependsJwtAuth])
async def get_level(
    db: CurrentSession, pk: Annotated[int, Path(description='Skill/experience level reference ID')]
) -> ResponseSchemaModel[GetLevelDetail]:
    """Get single level by ID"""
    level = await level_service.get(db=db, pk=pk)
    return response_base.success(data=level)


@router.get('', summary='Get Skill/experience level reference options list', dependencies=[DependsJwtAuth])
async def get_level_options(db: CurrentSession) -> ResponseSchemaModel[list[LabelValue]]:
    """Get all active levels as label-value pairs for dropdowns/selects"""
    options = await level_service.get_options(db=db)
    return response_base.success(data=options)


@router.get(
    '/paginated',
    summary='Get all Skill/experience level reference with pagination',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_levels_paginated(db: CurrentSession) -> ResponseSchemaModel[PageData[GetLevelDetail]]:
    """Get paginated list of all levels for admin management"""
    page_data = await level_service.get_list(db=db)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='Create Skill/experience level reference',
    dependencies=[
        Depends(RequestPermission('level:add')),
        DependsRBAC,
    ],
)
async def create_level(db: CurrentSessionTransaction, obj: CreateLevelParam) -> ResponseModel:
    await level_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='Update Skill/experience level reference',
    dependencies=[
        Depends(RequestPermission('level:edit')),
        DependsRBAC,
    ],
)
async def update_level(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='Skill/experience level reference ID')], obj: UpdateLevelParam
) -> ResponseModel:
    count = await level_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='Batch delete Skill/experience level reference',
    dependencies=[
        Depends(RequestPermission('level:del')),
        DependsRBAC,
    ],
)
async def delete_levels(db: CurrentSessionTransaction, obj: DeleteLevelParam) -> ResponseModel:
    count = await level_service.delete(db=db, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()
