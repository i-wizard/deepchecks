from typing import Optional

from fastapi import APIRouter,  File, UploadFile, BackgroundTasks, Request, Query, HTTPException

from src.core.services.interaction import InteractionService
from src.core.services.metric import MetricService
from src.core.services.alert import AlertService
from src.core.serializers import list_metric_serializer, list_alerts_serializer, list_interaction_serializer
from src.utils.response_manager import ResponseModel
from src.utils.file_uploader import stream_file_upload


router = APIRouter(
    prefix="/api/v1/interaction",
    tags=["Interaction"],
    responses={
        404: {
            "description": "Not found"
        }
    },

)


@router.post("/upload", response_description="Process and record LLM interactions")
async def upload_csv(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=422, detail="File must be CSV")
    temp_file = await stream_file_upload(file)
    # Use bigger a tool like Celery for background async tasks in Production
    background_tasks.add_task(InteractionService.process_csv, temp_file)
    return ResponseModel({}, None, message="Request successful and is being processed", status_code=202).send()


@router.get("/", response_description="Lists all interactions in the database")
async def list_interactions(request: Request,
                            page_number: Optional[int] = Query(1, gt=0),
                            limit: Optional[int] = Query(10, gt=0, le=100)):

    query = {}
    interactions = InteractionService.list_interactions(query)
    return ResponseModel(interactions, list_interaction_serializer).paginate_response(page_number, limit, query, InteractionService.collection)


@router.get("/metrics", response_description="Lists all metrics in the database")
async def list_metrics(request: Request,
                       page_number: Optional[int] = Query(1, gt=0),
                       limit: Optional[int] = Query(10, gt=0, le=100),
                       metric_name: Optional[str] = Query(
                           None, description="Search by metric name"),
                       interaction_id: Optional[str] = Query(
                           None, description="Get all metrics from an interaction")):

    query = {}
    if interaction_id:
        query["interaction_id"] = interaction_id
    if metric_name:
        query['metric_name'] = {"$regex": f"^{metric_name}$", "$options": "i"}
    metrics = MetricService.list_metrics(query)
    return ResponseModel(metrics, list_metric_serializer).paginate_response(page_number, limit, query, MetricService.collection)


@router.get("/alerts", response_description="Lists all alerts in the database")
async def list_alerts(request: Request,
                      page_number: Optional[int] = Query(1, gt=0),
                      limit: Optional[int] = Query(10, gt=0, le=100),
                      metric_name: Optional[str] = Query(
                          None, description="Search by alert by metric name"),
                      interaction_id: Optional[str] = Query(
                          None, description="Get all alerts from an interaction"),
                      alert_type: Optional[str] = Query(
                          None, description="filter by alert type")):

    query = {}
    if interaction_id:
        query["interaction_id"] = interaction_id
    if metric_name:
        query['metric_name'] = {"$regex": f"^{metric_name}$", "$options": "i"}
    if alert_type:
        query['alert_type'] = alert_type
    alerts = AlertService.list_alerts(query)
    return ResponseModel(alerts, list_alerts_serializer).paginate_response(page_number, limit, query, AlertService.collection)
