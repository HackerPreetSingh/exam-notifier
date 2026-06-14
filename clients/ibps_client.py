import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


def fetch_notices(url):
    response = requests.get(
        url,
        timeout=30,
        verify=False
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch IBPS notices. Status code: {response.status_code}"
        )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    notices = []

    links = soup.find_all(
        "a",
        href=True
    )

    for link in links:

        href = link["href"]

        date_div = link.find(
            "div",
            class_="detail-first-heading"
        )

        title_div = link.find(
            "div",
            class_="detail-second-heading"
        )

        if not date_div or not title_div:
            continue

        notices.append({
            "id": href,
            "title": title_div.get_text(
                strip=True
            ),
            "date": date_div.get_text(
                strip=True
            ),
            "url": href,
            "source": "IBPS_CRP"
        })

    return notices