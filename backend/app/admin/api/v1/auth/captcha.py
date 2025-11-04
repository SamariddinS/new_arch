from uuid import uuid4

from fast_captcha import img_captcha
from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from starlette.concurrency import run_in_threadpool

from backend.app.admin.schema.captcha import GetCaptchaDetail
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.core.conf import settings
from backend.database.redis import redis_client

router = APIRouter()


@router.get(
    '/captcha',
    summary='Get login captcha',
    dependencies=[Depends(RateLimiter(times=5, seconds=10))],
)
async def get_captcha() -> ResponseSchemaModel[GetCaptchaDetail]:
    """
    This endpoint may have performance overhead. Although it's an async endpoint, captcha generation is an IO-intensive task. Thread pool is used to minimize performance impact.
    """
    img_type: str = 'base64'
    img, code = await run_in_threadpool(img_captcha, img_byte=img_type)
    uuid = str(uuid4())
    await redis_client.set(
        f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{uuid}',
        code,
        ex=settings.CAPTCHA_LOGIN_EXPIRE_SECONDS,
    )
    data = GetCaptchaDetail(uuid=uuid, img_type=img_type, image=img)
    return response_base.success(data=data)
