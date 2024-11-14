from src.config.database import get_database

db = get_database()

def get_collection(base_url):
    if "ar" in base_url:
        return db["alerts_ar"]
    elif "en" in base_url:
        return db["alerts_en"]
    else:
        raise ValueError(f"Unsupported base URL: {base_url}")


def get_all_alerts(language):
    collection = get_collection(language)
    return list(collection.find({}))


def search_alerts(query: str, base_url):
    collection = get_collection(base_url)
    return list(collection.find({"title": {"$regex": query, "$options": "i"}}))
