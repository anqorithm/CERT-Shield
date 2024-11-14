from src.modules.alerts.service import (
    get_all_alerts,
    scrape_page,
    store_alerts_in_db,
    search_alerts,
)


def fetch_all_alerts(language: str):
    return {"status": "success", "alerts": get_all_alerts(language)}


def scrape_and_store_alerts(from_page: int, to_page: int):
    for page in range(from_page, to_page + 1):
        alerts = scrape_page(page)
        store_alerts_in_db(alerts)
    return {"status": "success", "message": f"Scraped pages {from_page} to {to_page}"}


def search_alerts_by_query(query: str):
    return {"status": "success", "alerts": search_alerts(query)}
