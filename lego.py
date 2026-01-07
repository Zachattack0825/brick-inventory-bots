import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.brickeconomy.com"

def get_lego_sets():
    """
    Step 1: Scrape retiring LEGO sets for set number and name.
    Returns list of [set_number, name].
    """
    url = f"{BASE_URL}/sets/retiring-soon"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    sets = []
    table = soup.find("table")
    if not table:
        print("No table found on retiring page.")
        return sets

    rows = table.find_all("tr")[1:]  # skip header
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        set_number = cols[0].get_text(strip=True)
        name = cols[1].get_text(strip=True)
        sets.append([set_number, name])

    return sets


def get_set_prices(set_number):
    """
    Step 2: For a given set_number, scrape BrickEconomy set page
    for Retail and Projected prices.
    Returns (retail_price, projected_price)
    """
    url = f"{BASE_URL}/sets/{set_number}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code != 200:
        return ("", "")  # return empty if page not found
    soup = BeautifulSoup(r.text, "html.parser")

    # Retail price
    retail = ""
    retail_elem = soup.find("td", string="Retail Price")
    if retail_elem and retail_elem.find_next_sibling("td"):
        retail = retail_elem.find_next_sibling("td").get_text(strip=True).replace("$", "")

    # Projected price
    projected = ""
    proj_elem = soup.find("td", string="Projected Price")
    if proj_elem and proj_elem.find_next_sibling("td"):
        projected = proj_elem.find_next_sibling("td").get_text(strip=True)

    return (retail, projected)


def get_lego_retiring_data():
    """
    Combines steps 1 & 2 and returns full dataset for Google Sheets.
    Columns: ["Set Number", "Name", "Retail Price", "Projected Price"]
    """
    sets = get_lego_sets()
    results = [["Set Number", "Name", "Retail Price", "Projected Price"]]

    for set_number, name in sets:
        retail, projected = get_set_prices(set_number)
        results.append([set_number, name, retail, projected])
        time.sleep(0.5)  # be polite, avoid overloading server

    return results
