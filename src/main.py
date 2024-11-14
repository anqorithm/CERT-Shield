from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.modules.alerts.router import router as alerts_router
from src.config.config import settings

app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    summary="Root Endpoint",
    description="Welcome message for the Alerts API",
    response_description="Welcome message",
)
def root():
    return {"message": "Welcome to the Alerts API"}


# Include routers
app.include_router(alerts_router, prefix="/api/alerts", tags=["Alerts"])
