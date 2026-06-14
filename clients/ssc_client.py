import requests
from datetime import datetime
from urllib.parse import quote


def build_pdf_url(notice):
    attachments = notice.get("attachments", [])

    if not attachments:
        return None

    pdf_path = attachments[0]["path"]

    normalized_path = pdf_path.replace("\\", "/")

    encoded_path = quote(
        normalized_path,
        safe="/"
    )

    return (
        f"https://ssc.gov.in/api/attachment/"
        f"{encoded_path}"
    )


def get_latest_notices(url):

    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    raw_notices = response.json()["data"]

    notices = []

    for notice in raw_notices:

        notices.append({
            "id": notice["id"],
            "title": notice["headline"],
            "date": datetime.fromisoformat(
                notice["createdAt"].replace(
                    "Z",
                    "+00:00"
                )
            ).strftime("%d %b %Y"),
            "url": build_pdf_url(notice),
            "source": "SSC"
        })

    return notices