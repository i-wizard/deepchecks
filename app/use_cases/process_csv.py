import os
import traceback
import pandas as pd

from fastapi import BackgroundTasks, HTTPException, UploadFile

from app.repositories import BaseRepository
from app.utils.logger import CustomLogger
from app.utils.file_uploader import stream_file_upload
from app.use_cases import BaseUseCase
from app.use_cases.interaction import SaveInteractionsUseCase


class StartCSVUploadUseCase(BaseUseCase):
    def __init__(self,  repo: BaseRepository):
        self.repo = repo
        self.save_interactions_use_case = SaveInteractionsUseCase(repo)

    async def execute(self, task: BackgroundTasks, file: UploadFile):
        if file.content_type != 'text/csv':
            raise HTTPException(status_code=422, detail="File must be CSV")
        file_path = await stream_file_upload(file)
        usecase = ProcessCSVUseCase(self.repo)
        # Use bigger libary like Celery to process background jobs or Use Kafka for streaming data to a consumer
        task.add_task(usecase.execute, file_path)


class ProcessCSVUseCase(BaseUseCase):
    def __init__(self,  repo: BaseRepository):
        self.repo = repo
        self.save_interactions_use_case = SaveInteractionsUseCase(repo)

    async def execute(self, file_path):
        try:
            reader = pd.read_csv(
                file_path, skipinitialspace=True, chunksize=10, on_bad_lines='skip')
            for chunk in reader:
                interactions = []
                for _, row in chunk.iterrows():
                    interaction = {"identifier": row.get("id"), "input": row.get(
                        "Input"), "output": row.get("Output")}
                    interactions.append(interaction)
                await self.save_interactions_use_case.execute(interactions)

        except Exception as e:
            extra = {"traceback": traceback.format_exc(), "error": str(e)}
            CustomLogger.error(
                "Error occurred processing LLM interaction CSV file", extra=extra)
        finally:
            os.remove(file_path)
