import requests

def fetch_lego(set_number):
    url = f"https://www.lego.com/api/productdetails/v2/products/{set_number}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    j = r.json()

    price = j["price"]["currentPrice"]
    sale = j["price"].get("discountPercentage", 0)
    
    return {
        "sku": set_number,
        "retailer": "LEGO",
        "name": j["name"],
        "price": price,
        "sale_price": price if sale == 0 else j["price"]["discountedPrice"],
        "percent_off": sale,
        "exclusive": j.get("exclusive", False),
        "retiring": j.get("retiringSoon", False),
        "stock": j["availability"]["availabilityStatus"]
    }
