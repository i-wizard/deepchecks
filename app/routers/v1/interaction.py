from typing import List

from fastapi import APIRouter, File, UploadFile, BackgroundTasks, Request, HTTPException

from app.config.settings import db
from app.use_cases.process_csv import StartCSVUploadUseCase
from app.use_cases.interaction import InteractionListUseCase
from app.repositories.mongo import MongoDB

router = APIRouter()


@router.get("/")
async def get_interactions(request: Request):
    return InteractionListUseCase(MongoDB(db)).execute()


@router.post("/upload/")
async def upload_csv(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    await StartCSVUploadUseCase(MongoDB(db)).execute(background_tasks, file)

    return {"message": " Request successful"}
