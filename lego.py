import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.brickeconomy.com"

def get_lego_sets():
    """
    Scrape retiring LEGO sets from BrickEconomy.
    Returns list of dicts with basic info.
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
        if len(cols) < 6:
            continue
        sets.append({
            "set_number": cols[0].get_text(strip=True),
            "name": cols[1].get_text(strip=True),
            "theme": cols[2].get_text(strip=True),
            "expected_retirement": cols[4].get_text(strip=True),
            "availability": cols[5].get_text(strip=True)
        })
    return sets


def get_set_prices_and_info(set_number):
    """
    Scrape a LEGO set page for detailed info:
    Retail Price, Projected Price, % Increase, Year, Where to Buy
    """
    url = f"{BASE_URL}/sets/{set_number}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code != 200:
        return {
            "retail_price": "",
            "projected_price": "",
            "percent_increase": "",
            "retirement_year": "",
            "where_to_buy": ""
        }

    soup = BeautifulSoup(r.text, "html.parser")

    def get_td_value(label):
        elem = soup.find("td", string=label)
        if elem and elem.find_next_sibling("td"):
            return elem.find_next_sibling("td").get_text(strip=True).replace("$", "")
        return ""

    return {
        "retail_price": get_td_value("Retail Price"),
        "projected_price": get_td_value("Projected Price"),
        "percent_increase": get_td_value("% Increase"),
        "retirement_year": get_td_value("Year"),
        "where_to_buy": get_td_value("Where to Buy")
    }


def get_lego_retiring_data():
    """
    Combine set info + detailed prices into a clean sheet-ready table.
    """
    sets = get_lego_sets()
    results = [[
        "Set Number", "Name", "Theme", "Retail Price", "Projected Price",
        "% Increase", "Retirement Year", "Expected Retirement", "Availability", "Where to Buy"
    ]]

    for set_data in sets:
        set_number = set_data["set_number"]
        name = set_data["name"]

        prices_info = get_set_prices_and_info(set_number)

        results.append([
            set_number,
            name,
            set_data["theme"],
            prices_info["retail_price"],
            prices_info["projected_price"],
            prices_info["percent_increase"],
            prices_info["retirement_year"],
            set_data["expected_retirement"],
            set_data["availability"],
            prices_info["where_to_buy"]
        ])

        time.sleep(0.5)  # polite delay

    return results
