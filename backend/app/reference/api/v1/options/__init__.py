from fastapi import APIRouter

from backend.app.reference.api.v1.options.level import router as level_router

router = APIRouter(prefix='/options')

router.include_router(level_router, prefix='/levels', tags=['Reference'])
