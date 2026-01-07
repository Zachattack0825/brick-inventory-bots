import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.brickeconomy.com"

def get_lego_retiring_data():
    """
    Scrapes BrickEconomy 'Sets Retiring Soon' page and extracts:
    Set Number, Name, Theme, Retail Price, Expected Retirement, Availability.
    Returns a table (list of lists) for Google Sheets.
    """
    url = f"{BASE_URL}/sets/retiring-soon"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    results = [["Set Number", "Name", "Theme", "Year", "Retail Price", "Expected Retirement", "Availability"]]

    # On the page, each set section begins with a heading: "#### 77053 Stargazing with Celeste"
    # followed by text like "Theme Animal Crossing Year 2025 ... Retail $9.99 Available at retail Retiring soon"
    h4_tags = soup.find_all("h4")

    for h4 in h4_tags:
        text = h4.get_text(strip=True)

        # Parse set number and name
        parts = text.split(" ", 1)
        if len(parts) < 2:
            continue
        set_number = parts[0]
        name = parts[1]

        # Default values
        theme = ""
        year = ""
        retail_price = ""
        expected_retirement = ""
        availability = ""

        # The info is in the sibling text after <h4>
        info = h4.find_next_sibling(text=True)
        if info:
            info_text = info.strip()

            # Theme
            m = re.search(r"Theme\s+([^0-9]+?)Year", info_text)
            if m:
                theme = m.group(1).strip()

            # Year
            m = re.search(r"Year\s+(\d{4})", info_text)
            if m:
                year = m.group(1).strip()

            # Retail Price
            m = re.search(r"Retail\s+\$([0-9.,]+)", info_text)
            if m:
                retail_price = m.group(1).strip()

            # Expected Retirement
            m = re.search(r"Expected retirement\s+([A-Za-z0-9\s]+?)(?=\s+\d{1,3}%|Available|$)", info_text)
            if m:
                expected_retirement = m.group(1).strip()

            # Availability
            if "Available at retail" in info_text:
                availability = "Available"

        results.append([
            set_number,
            name,
            theme,
            year,
            retail_price,
            expected_retirement,
            availability
        ])

    return results
