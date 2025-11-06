from fastapi import APIRouter

from backend.app.reference.api.v1.options import router as options_router
from backend.core.conf import settings

v1 = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

v1.include_router(options_router)
