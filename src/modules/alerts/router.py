from fastapi import APIRouter, Query
from src.modules.alerts.controller import (
    fetch_all_alerts,
    search_alerts_by_query,
)

router = APIRouter()

@router.get("/")
def get_alerts(
    language: str = Query("en", description="Language for alerts", enum=["en", "ar"])
):
    return fetch_all_alerts(language)


@router.get("/search")
def search_alerts(query: str = Query(...)):
    return search_alerts_by_query(query)
