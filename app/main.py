from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config import settings

from app.routers import (
    health,
    predict,
    dashboard,
    students,
    interventions,
    fairness,
    districts,
    resources,
    opportunities,
    root_cause,
    early_warning,
    policy,
    quality,
    digital_twin,
    student_intelligence,
)


# ============================================================
# VIZHIPPAAN FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Backend API for VIZHIPPAAN – "
        "Child Education Risk Intelligence Platform"
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT ROUTE
# ============================================================

@app.get("/", include_in_schema=False)
def root():
    """
    Redirect the root URL to Swagger documentation.
    """
    return RedirectResponse(url="/docs")


# ============================================================
# SIMPLE HEALTH CHECK
# ============================================================

@app.get("/ping", tags=["System"])
def ping():
    """
    Lightweight API health check.
    """
    return {
        "status": "ok",
        "project": "VIZHIPPAAN",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "api_prefix": settings.API_PREFIX,
    }


# ============================================================
# API ROUTERS
# ============================================================

routers = [
    health.router,
    predict.router,
    dashboard.router,
    students.router,
    interventions.router,
    fairness.router,
    districts.router,
    resources.router,
    opportunities.router,
    root_cause.router,
    early_warning.router,
    policy.router,
    quality.router,
    digital_twin.router,
    student_intelligence.router,
]


for router in routers:
    app.include_router(
        router,
        prefix=settings.API_PREFIX,
    )
