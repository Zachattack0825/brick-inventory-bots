import requests
from bs4 import BeautifulSoup

def get_lego_retiring_data():
    url = "https://www.brickeconomy.com/sets/retiring-soon"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    results = [["Set Number", "Name", "Retail Price", "Projected Price", "Expected Retirement", "Availability"]]

    # Find the main table
    table = soup.find("table")
    if not table:
        print("Error: Could not find the retiring sets table!")
        return results

    rows = table.find_all("tr")
    for row in rows[1:]:  # skip header
        cols = row.find_all("td")
        if len(cols) < 6:
            continue
        set_number = cols[0].get_text(strip=True)
        name = cols[1].get_text(strip=True)
        retail_price = cols[2].get_text(strip=True).replace("$", "")
        projected_price = cols[3].get_text(strip=True)
        expected_retirement = cols[4].get_text(strip=True)
        availability = cols[5].get_text(strip=True)

        results.append([set_number, name, retail_price, projected_price, expected_retirement, availability])

    return results
