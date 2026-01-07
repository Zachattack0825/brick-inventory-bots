import requests
from bs4 import BeautifulSoup
import re

def get_lego_retiring_data():
    """
    Scrapes LEGO "Last Chance to Buy / Retiring Soon" page
    Returns a list of lists (table) for sheet update.
    """
    url = "https://www.lego.com/en-us/categories/last-chance-to-buy"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Header row for the sheet
    results = [["Set", "Price", "Availability", "Retailer"]]

    # Each product card on the page
    # The specific class names may change over time — update if needed
    product_cards = soup.select("a.product-card--product")

    for card in product_cards:
        # Extract the product name
        name_tag = card.select_one("span.product-card__title")
        name = name_tag.text.strip() if name_tag else "No name"

        # Extract price if available
        price_tag = card.select_one("span.product-price__price")
        price = price_tag.text.strip() if price_tag else "Price N/A"

        # Try extracting a LEGO set number from the link
        href = card.get("href", "")
        set_id = None
        # Some LEGO URLs contain the set number at the end
        match = re.search(r"/product/(?:.*)-(\d+)", href)
        if match:
            set_id = match.group(1)
        else:
            set_id = "Unknown"

        # always mention it's LEGO (since this scraper is LEGO.com)
        retailer = "LEGO"

        results.append([set_id, name, price, retailer])

    return results
