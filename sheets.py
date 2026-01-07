import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Load JSON from GitHub secret
service_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
creds_dict = json.loads(service_json)

# Authenticate
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPES)
gc = gspread.authorize(creds)

# Open your sheet
SHEET_ID = "https://docs.google.com/spreadsheets/d/1ZjgX7_OfhsfVVkrFITcq8w1C61QJSxMgLKi5umPg1ZY/edit?gid=0#gid=0"
ws = gc.open_by_key(SHEET_ID).sheet1
