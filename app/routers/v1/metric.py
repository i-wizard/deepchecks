from fastapi import APIRouter, Request


from app.config.settings import db
from app.repositories.mongo import MongoDB
from app.use_cases.metric import ListMetricsUseCase


router = APIRouter()


@router.get("/")
async def get_alerts(request: Request):
    return ListMetricsUseCase(MongoDB(db)).execute({})
