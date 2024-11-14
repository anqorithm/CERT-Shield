from fastapi import FastAPI
from src.modules.alerts.router import router as alerts_router

# Initialize FastAPI app
app = FastAPI(
    title="Alerts API",
    description="An API for scraping and managing security alerts.",
    version="1.0.0",
)

# Include routers
app.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
