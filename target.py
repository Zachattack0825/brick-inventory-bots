import requests

def fetch_target(sku):
    url = f"https://www.target.com/p/{sku}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    data = {"sku": sku, "retailer": "Target"}
    data.update({
        "name": f"Target Item {sku}",
        "price": 0,
        "sale_price": 0,
        "percent_off": 0,
        "exclusive": False,
        "retiring": False,
        "stock": "Unknown"
    })
    return data
