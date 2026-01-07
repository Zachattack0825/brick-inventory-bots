from sheets import update_sheet
from lego import get_lego_retiring_data

def main():
    # Get the latest retiring LEGO sets from BrickEconomy
    lego_data = get_lego_retiring_data()

    # Optional: print to logs to debug GitHub Actions run
    print(f"Found {len(lego_data)-1} LEGO sets retiring soon.")
    for row in lego_data[:5]:  # preview first 5 rows
        print(row)

    # Update your Google Sheet with the LEGO data
    update_sheet(lego_data)

if __name__ == "__main__":
    main()
