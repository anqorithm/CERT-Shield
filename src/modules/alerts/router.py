from fastapi import APIRouter, BackgroundTasks, Query
from src.modules.alerts.controller import (
    fetch_all_alerts,
    scrape_and_store_alerts,
    search_alerts_by_query,
)

router = APIRouter()


@router.get("/")
def get_alerts(language: str = Query(None)):
    return fetch_all_alerts(language)


@router.post("/scrape")
def scrape_alerts(
    background_tasks: BackgroundTasks, from_page: int = 1, to_page: int = 1
):
    background_tasks.add_task(scrape_and_store_alerts, from_page, to_page)
    return {"status": "success", "message": "Scraping started in background"}


@router.get("/search")
def search_alerts(query: str = Query(...)):
    return search_alerts_by_query(query)
