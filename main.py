from sheets import update_sheet
import lego  # your lego.py script

def main():
    # Get LEGO data as list of lists
    # Example from lego.py: [["Set", "Price", "Exclusive"], ["12345", "$49.99", "Yes"]]
    data = lego.get_lego_data()  # make sure lego.py has a function that returns this

    print("Data to update:", data)  # debug in workflow logs
    update_sheet(data)

if __name__ == "__main__":
    main()
