from src.modules.alerts.service import (
    get_all_alerts,
    scrape_page,
    store_alerts_in_db,
    search_alerts,
)


def fetch_all_alerts(language: str):
    return {"status": "success", "alerts": get_all_alerts(language)}


def scrape_and_store_alerts(from_page: int, to_page: int):
    try:
        successful_pages = 0
        failed_pages = []

        for page in range(from_page, to_page + 1):
            try:
                alerts = scrape_page(page)
                store_alerts_in_db(alerts)
                successful_pages += 1
            except Exception as e:
                failed_pages.append({"page": page, "error": str(e)})

        message = f"Successfully scraped {successful_pages} pages"
        if failed_pages:
            message += f". Failed pages: {failed_pages}"

        return {"status": "success", "message": message}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def search_alerts_by_query(query: str):
    return {"status": "success", "alerts": search_alerts(query)}
