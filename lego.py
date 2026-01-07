import requests
from bs4 import BeautifulSoup

def get_lego_retiring_data():
    """
    Scrape BrickEconomy 'Retiring Soon' sets with retail & projected prices.
    Returns list of lists for Google Sheets.
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

    results = [["Set Number", "Name", "Retail Price", "Projected Price", "Expected Retirement", "Availability"]]

    # Each set is in a div with class 'retiring-set-card' (example)
    cards = soup.find_all("div", class_="retiring-set-card")

    for card in cards:
        # Set number and name
        title = card.find("h4")
        if not title:
            continue
        title_text = title.get_text(strip=True)
        parts = title_text.split(" ", 1)
        if len(parts) != 2:
            continue
        set_number = parts[0]
        name = parts[1]

        # Retail price
        retail_price = ""
        retail_elem = card.find("span", class_="retail")
        if retail_elem:
            retail_price = retail_elem.get_text(strip=True).replace("$", "")

        # Projected price
        projected_price = ""
        projected_elem = card.find("span", class_="projected")
        if projected_elem:
            projected_price = projected_elem.get_text(strip=True)

        # Expected retirement
        expected_retirement = ""
        retire_elem = card.find("span", class_="retirement-date")
        if retire_elem:
            expected_retirement = retire_elem.get_text(strip=True)

        # Availability
        availability = ""
        avail_elem = card.find("span", class_="availability")
        if avail_elem:
            availability = avail_elem.get_text(strip=True)

        results.append([set_number, name, retail_price, projected_price, expected_retirement, availability])

    return results
