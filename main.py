from lego import get_lego_retiring_data

...

lego_data = get_lego_retiring_data()
all_data = lego_data  # you can combine Walmart/Target later
update_sheet(all_data)
