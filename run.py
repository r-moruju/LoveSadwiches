# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

from pprint import pprint
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

        data_str = input("Enter your data here: ")

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


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales Worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worsheet update successfully. \n")


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


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)


print("welcome to Love Sandwiches Data Automation")
main()