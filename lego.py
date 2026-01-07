import requests
from bs4 import BeautifulSoup

def get_lego_retiring_data():
    """
    Scrape BrickEconomy 'Retiring Soon' sets list and return
    a list of lists (rows) for Google Sheets.
    """
    url = "https://www.brickeconomy.com/sets/retiring-soon"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # Build header row
    results = [
        ["Set Number", "Name", "Expected Retirement", "Retail Price", "Availability"]
    ]

    # Each set entry on BrickEconomy appears as a headline (<h4>) followed by details
    items = soup.find_all("h4")
    for item in items:
        title_text = item.get_text(strip=True)

        # BrickEconomy titles look like:
        #   "77053 Stargazing with Celeste"
        #   "60373 Fire Rescue Boat"
        # So first token is set number, rest is name
        parts = title_text.split(" ", 1)
        if len(parts) != 2:
            continue

        set_number = parts[0]   # e.g., "77053"
        name = parts[1]         # e.g., "Stargazing with Celeste"

        # Next element sibling typically contains additional info
        info = item.find_next_sibling(text=True)
        if info:
            info_text = info.strip()
        else:
            info_text = ""

        # Extract price and status if present
        # BrickEconomy tends to include "Retail $9.99" and "Available at retail"
        price = ""
        availability = ""
        if "Retail" in info_text:
            # Rough parse: split on "Retail"
            tokens = info_text.split("Retail")
            if len(tokens) > 1:
                price_info = tokens[1].split("|")[0].strip()
                price = price_info.replace("$", "").strip()

        if "Available" in info_text:
            availability = "Available"
        else:
            availability = ""

        # Expected retirement estimate may be buried in the text
        # e.g., "Expected retirement Mid 2026 97.7%"
        expected = ""
        if "Expected retirement" in info_text:
            try:
                expected = info_text.split("Expected retirement")[1].split("|")[0].strip()
            except:
                expected = ""

        # Append the row
        results.append([set_number, name, expected, price, availability])

    return results
