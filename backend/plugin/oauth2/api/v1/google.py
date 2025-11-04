from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Response
from fastapi_limiter.depends import RateLimiter
from fastapi_oauth20 import FastAPIOAuth20, GoogleOAuth20
from starlette.responses import RedirectResponse

from backend.common.enums import UserSocialType
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.core.conf import settings
from backend.database.db import CurrentSessionTransaction
from backend.plugin.oauth2.service.oauth2_service import oauth2_service

router = APIRouter()

google_client = GoogleOAuth20(settings.OAUTH2_GOOGLE_CLIENT_ID, settings.OAUTH2_GOOGLE_CLIENT_SECRET)


@router.get('', summary='Get Google authorization URL')
async def get_google_oauth2_url() -> ResponseSchemaModel[str]:
    auth_url = await google_client.get_authorization_url(redirect_uri=settings.OAUTH2_GOOGLE_REDIRECT_URI)
    return response_base.success(data=auth_url)


@router.get(
    '/callback',
    summary='Google authorization auto redirect',
    description='After Google authorization, automatically redirect to current address and get user info, automatically create system user through user info',
    dependencies=[Depends(RateLimiter(times=5, minutes=1))],
)
async def google_oauth2_callback(  # noqa: ANN201
    db: CurrentSessionTransaction,
    response: Response,
    background_tasks: BackgroundTasks,
    oauth2: Annotated[
        FastAPIOAuth20,
        Depends(FastAPIOAuth20(google_client, redirect_uri=settings.OAUTH2_GOOGLE_REDIRECT_URI)),
    ],
):
    token_data, _state = oauth2
    access_token = token_data['access_token']
    user = await google_client.get_userinfo(access_token)
    data = await oauth2_service.create_with_login(
        db=db,
        response=response,
        background_tasks=background_tasks,
        user=user,
        social=UserSocialType.google,
    )
    return RedirectResponse(
        url=f'{settings.OAUTH2_FRONTEND_REDIRECT_URI}?access_token={data.access_token}&session_uuid={data.session_uuid}',
    )
