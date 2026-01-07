import csv
from datetime import datetime
from lego import fetch_lego
from sheets import update_sheet

def main():
    results = []

    # Open the products CSV
    with open("products.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only process LEGO products for now
            if row["retailer"].lower() != "lego":
                continue

            sku = row["product_id"]

            try:
                data = fetch_lego(sku)
            except Exception as e:
                print(f"Error fetching {sku}: {e}")
                continue

            # Add timestamp
            data["last_updated"] = datetime.utcnow().isoformat()
            results.append(data)

    if results:
        try:
            update_sheet(results)
            print("LEGO inventory updated successfully")
        except Exception as e:
            print(f"Error updating Google Sheet: {e}")
    else:
        print("No LEGO products processed")

if __name__ == "__main__":
    main()

