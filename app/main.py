from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config import settings
from app.routers import (
    health, predict, dashboard, students, interventions, fairness,
    districts, resources, opportunities, root_cause, early_warning, policy, quality
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for VIZHIPPAAN – Child Education Risk Intelligence Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

for router in [
    health.router, predict.router, dashboard.router, students.router,
    interventions.router, fairness.router, districts.router, resources.router,
    opportunities.router, root_cause.router, early_warning.router,
    policy.router, quality.router,
]:
    app.include_router(router, prefix=settings.API_PREFIX)
