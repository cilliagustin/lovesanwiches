import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    run a while loop to collect valid data from user which
    must be 6 numbers separataed by commas. The loop will request data
    until this is valid.

    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60")

        data_str = input("Enter your data here:\n")   
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("valid data")
            break

    return sales_data


def validate_data(values):
    """
    converts string to interger,
    raises value error if not possible,
    raises error if there are not 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )

    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


def update_worksheet(worksheet, data):
    """
    update sales/surplus worksheet. Add new row with data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    current_worksheet = SHEET.worksheet(worksheet)
    current_worksheet.append_row(data)
    print(f"{worksheet} worksheet succesfully added\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with strock to establish surplus
    """
    print("calculating surplus...")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]  
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    collects columns of data from sales worksheet, colecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1, 7):
        col = sales.col_values(ind)
        columns.append(col[-5:])
    return columns


def calculate_stock_data(data):
    """
    calculate average stock of each item and add 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data


def main():
    """
    Run all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet("sales", sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet("surplus", new_surplus_data)
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet("stock", stock_data)


print("Welcome to love sandwiches data automation")
main()