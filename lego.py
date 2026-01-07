import requests
from bs4 import BeautifulSoup

def get_lego_retiring_data():
    """
    Scrape BrickEconomy 'Retiring Soon' sets and return a list of lists
    for Google Sheets including set number, name, retail price, expected retirement,
    projected price, and availability.
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

    # Header row
    results = [
        ["Set Number", "Name", "Retail Price", "Projected Price", "Expected Retirement", "Availability"]
    ]

    # Each set entry on BrickEconomy appears as a headline <h4>
    items = soup.find_all("h4")
    for item in items:
        title_text = item.get_text(strip=True)
        parts = title_text.split(" ", 1)
        if len(parts) != 2:
            continue

        set_number = parts[0]
        name = parts[1]

        # Next sibling usually contains info text
        info = item.find_next_sibling(text=True)
        info_text = info.strip() if info else ""

        # Retail Price
        retail_price = ""
        if "Retail" in info_text:
            try:
                tokens = info_text.split("Retail")[1].split("|")
                retail_price = tokens[0].replace("$", "").strip()
            except:
                retail_price = ""

        # Projected Price (if present in BrickEconomy, sometimes shown as % gain)
        projected_price = ""
        if "Projected" in info_text:
            try:
                tokens = info_text.split("Projected")[1].split("|")
                projected_price = tokens[0].strip()
            except:
                projected_price = ""

        # Expected Retirement
        expected_retirement = ""
        if "Expected retirement" in info_text:
            try:
                expected_retirement = info_text.split("Expected retirement")[1].split("|")[0].strip()
            except:
                expected_retirement = ""

        # Availability
        availability = "Available" if "Available" in info_text else ""

        results.append([set_number, name, retail_price, projected_price, expected_retirement, availability])

    return results
