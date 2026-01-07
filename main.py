import csv
from datetime import datetime
from lego import fetch_lego
from sheets import update_sheet

results = []

with open("products.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["retailer"].lower() != "lego":
            continue  # skip non-LEGO products

        sku = row["product_id"]
        data = fetch_lego(sku)
        data["last_updated"] = datetime.utcnow().isoformat()
        results.append(data)

update_sheet(results)
print("LEGO inventory updated successfully")
