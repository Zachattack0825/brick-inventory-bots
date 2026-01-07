import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Replace 'service_account.json' with your JSON key
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", SCOPES)
gc = gspread.authorize(creds)

SHEET_ID = "https://docs.google.com/spreadsheets/d/1ZjgX7_OfhsfVVkrFITcq8w1C61QJSxMgLKi5umPg1ZY/edit?gid=0#gid=0"
ws = gc.open_by_key(SHEET_ID).sheet1

def update_sheet(results):
    # Clear existing rows except header
    ws.resize(rows=1)
    
    # Add header
    ws.append_row(["SKU", "Retailer", "Name", "Price", "Sale Price", "% Off", "Exclusive", "Retiring", "Stock", "Last Updated"])
    
    for item in results:
        ws.append_row([
            item.get("sku"),
            item.get("retailer"),
            item.get("name"),
            item.get("price"),
            item.get("sale_price"),
            item.get("percent_off"),
            item.get("exclusive"),
            item.get("retiring"),
            item.get("stock"),
            item.get("last_updated")
        ])
