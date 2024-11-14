from src.modules.alerts.service import (
    get_all_alerts,
    search_alerts,
)

def fetch_all_alerts(language: str):
    return {"status": "success", "alerts": get_all_alerts(language)}

def search_alerts_by_query(query: str):
    return {"status": "success", "alerts": search_alerts(query)}
