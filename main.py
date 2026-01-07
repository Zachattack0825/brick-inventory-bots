import csv
from datetime import datetime
from lego import fetch_lego
from walmart import fetch_walmart
from target import fetch_target
from sheets import update_sheet

results = []

with open("products.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        retailer = row["retailer"].lower()
        sku = row["product_id"]

        if retailer == "lego":
            data = fetch_lego(sku)
        elif retailer == "walmart":
            data = fetch_walmart(sku)
        elif retailer == "target":
            data = fetch_target(sku)
        else:
            continue

        data["last_updated"] = datetime.utcnow().isoformat()
        results.append(data)

update_sheet(results)
print("Inventory updated successfully")
