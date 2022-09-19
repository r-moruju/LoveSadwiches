"""
# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
"""
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('cred.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    '''
    Get sales figures from the user
    '''
    while True:
        print("Please input sales data from the las market day.")
        print('Data should be six numbers separated by commas.')
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n")

        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data


def validate_data(values):
    '''
    Check if integers and total inputs
    '''
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as error:
        print(f"Invalid data: {error}, please try again\n")
        return False
    return True


def update_worksheet(data, worksheet):
    """
    Receive a list of integer to be added to the worcksheet
    Update the relevand worcksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet\n")
    sheet = SHEET.worksheet(worksheet)
    sheet.append_row(data)
    print(f"{worksheet.capitalize()} worksheet updated successfully\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock ad calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entry_sales():
    """
    Collects collumns of data from sales worksheet, collecting the
    last 5 entries for each sandwich and return the data as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(6):
        column = sales.col_values(ind + 1)
        columns.append(column[-5:])

    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating the stock data...\n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entry_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("welcome to Love Sandwiches Data Automation")
main()
