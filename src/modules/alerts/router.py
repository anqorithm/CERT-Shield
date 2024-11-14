from fastapi import APIRouter, Query
from src.modules.alerts.controller import (
    fetch_all_alerts,
    scrape_and_store_alerts,
    search_alerts_by_query,
)

router = APIRouter()


@router.get("/")
def get_alerts(
    language: str = Query("en", description="Language for alerts", enum=["en", "ar"])
):
    return fetch_all_alerts(language)


@router.post("/scrape")
def scrape_alerts(
    from_: int = Query(1, alias="from", ge=1, description="Starting page number"),
    to: int = Query(1, ge=1, description="Ending page number"),
):
    scrape_and_store_alerts(from_, to)
    return {"status": "success", "message": "Scraping completed"}


@router.get("/search")
def search_alerts(query: str = Query(...)):
    return search_alerts_by_query(query)
