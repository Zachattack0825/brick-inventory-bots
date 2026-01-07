import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -------------------------------
# CONFIG
# -------------------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_ID = "1ZjgX7_OfhsfVVkrFITcq8w1C61QJSxMgLKi5umPg1ZY"  # just the ID!

# -------------------------------
# LOAD SERVICE ACCOUNT JSON FROM SECRET
# -------------------------------
service_json = os.environ.get("GOOGLE_SERVICE_JSON")

if not service_json:
    raise ValueError(
        "GOOGLE_SERVICE_JSON secret not found! "
        "Check spelling and branch."
    )

creds_dict = json.loads(service_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPES)
gc = gspread.authorize(creds)

# Open the spreadsheet
ws = gc.open_by_key(SHEET_ID).sheet1

# -------------------------------
# HELPER FUNCTION TO UPDATE SHEET
# -------------------------------
def update_sheet(data):
    """
    data: list of lists, each sublist = a row
    Example: [["Set", "Price", "Exclusive"], ["12345", "$49.99", "Yes"]]
    """
    if not data or len(data) == 0:
        print("No data to update.")
        return

    ws.clear()            # remove old data
    ws.update("A1", data) # write new data
    print(f"Sheet updated with {len(data)-1} rows.")
