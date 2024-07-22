from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.v1 import metric as metric_v1
from app.routers.v1 import alert as alert_v1
from app.routers.v1 import interaction as interaction_v1

app = FastAPI(
    title="Deepchecks Module",
    description="",
    version="0.0.1",
    contact={
        "name": "support",
        "email": "anon@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)
app.include_router(
    metric_v1.router, prefix='/api/v1/metrics', tags=['Metrics'])
app.include_router(alert_v1.router, prefix='/api/v1/alerts', tags=['Alerts'])
app.include_router(interaction_v1.router,
                   prefix='/api/v1/interactions', tags=['Interactions'])
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
