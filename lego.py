import time
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ================== CONFIG ==================

BRICKSET_API_KEY = "3-2fKf-8Kxv-lMDwh"
BRICKSET_USERNAME = "Zaach"
BRICKSET_PASSWORD = "nbCIfwx3S1"

GOOGLE_CREDS_FILE = "service_account.json"
SHEET_NAME = "LEGO Data"

SET_NUMBERS = [
    "75331",
    "10283",
    "21318"
]

EBAY_FEE = 0.15
REQUEST_DELAY = 2  # seconds (be polite)

# ================== GOOGLE SHEETS ==================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    GOOGLE_CREDS_FILE, scope
)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# ================== BRICKSET LOGIN ==================

login_url = "https://brickset.com/api/v3.asmx/login"
login_params = {
    "apiKey": BRICKSET_API_KEY,
    "username": BRICKSET_USERNAME,
    "password": BRICKSET_PASSWORD
}

login_resp = requests.get(login_url, params=login_params).json()

if "hash" not in login_resp:
    raise Exception("Brickset login failed")

USER_HASH = login_resp["hash"]

# ================== HELPERS ==================

def calculate_metrics(msrp, current_price):
    try:
        msrp = float(msrp)
        current_price = float(current_price)
    except:
        return "", ""

    gross = ((current_price - msrp) / msrp) * 100
    net_price = current_price * (1 - EBAY_FEE)
    net = ((net_price - msrp) / msrp) * 100

    return round(gross, 2), round(net, 2)


def fetch_set(set_number):
    url = "https://brickset.com/api/v3.asmx/getSets"
    params = {
        "apiKey": BRICKSET_API_KEY,
        "userHash": USER_HASH,
        "params": f'{{"setNumber":"{set_number}-1"}}'
    }

    resp = requests.get(url, params=params).json()

    if not resp.get("sets"):
        return None

    s = resp["sets"][0]

    name = s.get("name", "")
    msrp = s.get("USRetailPrice") or ""
    retirement_year = s.get("retirementYear") or ""
    retired = "Y" if retirement_year else "N"

    return {
        "set_number": set_number,
        "name": name,
        "msrp": msrp,
        "current_price": "",
        "retired": retired,
        "retirement_year": retirement_year
    }

# ================== MAIN ==================

for set_number in SET_NUMBERS:
    print(f"Processing {set_number}...")

    data = fetch_set(set_number)
    if not data:
        print(f"  ❌ Not found")
        continue

    gross_roi, net_roi = calculate_metrics(
        data["msrp"],
        data["current_price"]
    )

    sheet.append_row([
        data["set_number"],
        data["name"],
        data["msrp"],
        data["current_price"],
        data["retired"],
        data["retirement_year"],
        gross_roi,
        net_roi
    ])

    print(f"  ✅ Added {data['name']}")
    time.sleep(REQUEST_DELAY)

print("Done.")
