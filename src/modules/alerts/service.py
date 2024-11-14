import requests
from bs4 import BeautifulSoup
from src.config.database import get_database

db = get_database()


def get_collection(base_url):
    if "ar" in base_url:
        return db["alerts_ar"]
    elif "en" in base_url:
        return db["alerts_en"]
    else:
        raise ValueError(f"Unsupported base URL: {base_url}")


def scrape_alert_details(alert_url):
    response = requests.get(alert_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        alert_details_div = soup.find("div", class_="cert-body cert-gray-70 m-3")

        details = {}

        if alert_details_div:
            warning_number_elem = alert_details_div.find(
                "p", string=lambda text: "Warning Number" in text
            )
            if warning_number_elem:
                details["warning_number"] = warning_number_elem.find_next_sibling(
                    "p"
                ).text.strip()

            release_date_elem = alert_details_div.find(
                "p", string=lambda text: "Release Date" in text
            )
            if release_date_elem:
                details["release_date"] = release_date_elem.find_next_sibling(
                    "p"
                ).text.strip()

            last_update_elem = alert_details_div.find(
                "p", string=lambda text: "Last Update" in text
            )
            if last_update_elem:
                details["last_update"] = last_update_elem.find_next_sibling(
                    "p"
                ).text.strip()

            cves_elem = alert_details_div.find("p", string=lambda text: "CVEs" in text)
            if cves_elem:
                details["cves"] = [
                    cve.strip()
                    for cve in cves_elem.find_next_sibling("p").text.split(",")
                ]

            affected_products_elem = alert_details_div.find(
                "p", string=lambda text: "Affected Products" in text
            )
            if affected_products_elem:
                details["affected_products"] = [
                    prod.strip()
                    for prod in affected_products_elem.find_next_sibling(
                        "p"
                    ).text.split(",")
                ]

            summary_elem = alert_details_div.find(
                "p", string=lambda text: "Summary" in text
            )
            if summary_elem:
                details["summary"] = summary_elem.find_next_sibling("p").text.strip()

            return details

    return {}


def scrape_page(page_number, base_url):
    url = f"{base_url}/?page={page_number}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        alerts_severity = soup.find_all("div", class_="card-header")
        alerts_title = soup.find_all("p", class_="cert-card-body-warning")
        alert_images = soup.find_all(
            "img", class_=["card-img-top", "security-alerts-cover-image"]
        )
        alert_cards = soup.find_all("div", class_="card mb-4 light-gray-border")
        alerts_data = []

        for severity, title, image, card in zip(
            alerts_severity, alerts_title, alert_images, alert_cards
        ):
            alert_url = base_url + card.find("a").get("href")
            alert_details = scrape_alert_details(alert_url)

            alert_info = {
                "title": title.text.strip(),
                "severity": severity.text.strip(),
                "logo": base_url + image.get("src"),
                "alert_url": alert_url,
                "details": alert_details,
            }
            alerts_data.append(alert_info)

        return alerts_data
    return []


def store_alerts_in_db(alerts, base_url):
    collection = get_collection(base_url)
    for alert in alerts:
        warning_number = alert["details"].get("warning_number")
        if warning_number and not collection.find_one(
            {"details.warning_number": warning_number}
        ):
            collection.insert_one(alert)
        else:
            print(
                f"Alert with warning number {warning_number} already exists, skipping."
            )


def get_all_alerts(langauge):
    collection = get_collection(langauge)
    return list(collection.find({}))


def search_alerts(query: str, base_url):
    collection = get_collection(base_url)
    return list(collection.find({"title": {"$regex": query, "$options": "i"}}))


def process_pages(from_page: int, to_page: int, base_url: str):
    collection = get_collection(base_url)
    all_alerts = []
    for i in range(from_page, to_page + 1):
        data = scrape_page(i, base_url)
        all_alerts.extend(data)
    store_alerts_in_db(all_alerts, base_url)
    return f"Successfully processed pages {from_page} to {to_page}"
