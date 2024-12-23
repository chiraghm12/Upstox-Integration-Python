"""
Script for analyze the chart pattern
"""

import csv
import os
import webbrowser

import requests
from dotenv import load_dotenv

load_dotenv()


# get credentials from .env file and define constant
CLIENT_ID = os.getenv("API_KEY")
CLIENT_SECRET = os.getenv("API_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")
CODE = ""
GRANT_TYPE = "authorization_code"
ACCESS_TOKEN = ""
INSTRUMENT_KEYS = []


def initialize_files():
    """
    Method for Initialize the csv files for store the Stocks name according to the pattern.
    """
    # initialize file for Hammer
    with open("Hammer.csv", mode="w", newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name"])

    # initialize file for Doji
    with open("Doji.csv", mode="w", newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name"])

    # initialize file for Inverted Hammer
    with open("Inverted_Hammer.csv", mode="w", newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name"])

    # initialize file for Spinning Top-Bottom
    with open(
        "Spinning_Top_Bottom.csv", mode="w", newline="", encoding="UTF-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["Name"])


def get_authorize_code():
    """
    Method for get the Authorization code from Upstox
    """
    url = f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}"
    # open link in browser for login in upstox
    webbrowser.open_new_tab(url)
    c = input("Enter Code : ")
    global CODE  # pylint:disable=W0603
    CODE = c
    # print("Code is : ", CODE)


def get_access_token():
    """
    Method for get the Access token from Upstox
    """
    url = "https://api.upstox.com/v2/login/authorization/token"

    payload = {
        "code": CODE,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URL,
        "grant_type": GRANT_TYPE,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    response = requests.post(url, headers=headers, data=payload, timeout=300)
    global ACCESS_TOKEN  # pylint:disable=W0603
    ACCESS_TOKEN = response.json().get("access_token")
    # print(response.text)


def fetch_instrument_keys_from_csv():
    """
    Method for get the instruments key of Nifty500 Stocks.
    """
    csv_file_path = "Nifty500.csv"
    column_name = "ISIN Code"
    global INSTRUMENT_KEYS  # pylint:disable=W0602

    # Open and read the CSV file
    with open(csv_file_path, mode="r", encoding="UTF-8") as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name
        for row in reader:
            # Extract only the desired columns
            INSTRUMENT_KEYS.append(row[column_name])

    # print("Column values:", len(INSTRUMENT_KEYS))


def is_inverted_hammer(open_price, high_price, low_price, close_price):
    """
    Method for check if candle is inverted hammer or not.

    Args:
        open_price (float): candle's open price
        high_price (float): candle's high price
        low_price (float): candle's low price
        close_price (float): candle's close price

    Returns:
        bool: True or False
    """
    if open_price == 0 and close_price == 0 and low_price == 0 and high_price == 0:
        return False

    if open_price == close_price == high_price == low_price:
        return False

    body = abs(close_price - open_price)  # Real body
    lower_shadow = 0
    upper_shadow = 0
    if close_price > open_price:
        upper_shadow = high_price - close_price
        lower_shadow = open_price - low_price
    else:
        upper_shadow = high_price - open_price
        lower_shadow = close_price - low_price

    if (upper_shadow >= (body * 2)) and (lower_shadow <= (body * 0.5)):
        return True
    return False


def is_hammer(open_price, high_price, low_price, close_price):
    """
    Method for check if candle is hammer or not.

    Args:
        open_price (float): candle's open price
        high_price (float): candle's high price
        low_price (float): candle's low price
        close_price (float): candle's close price

    Returns:
        bool: True or False
    """
    if open_price == 0 and close_price == 0 and low_price == 0 and high_price == 0:
        return False

    if open_price == close_price == high_price == low_price:
        return False

    body = abs(close_price - open_price)  # Real body
    lower_shadow = 0
    upper_shadow = 0
    if close_price > open_price:
        upper_shadow = high_price - close_price
        lower_shadow = open_price - low_price
    else:
        upper_shadow = high_price - open_price
        lower_shadow = close_price - low_price

    if (lower_shadow >= (body * 2)) and (upper_shadow <= (body * 0.5)):
        return True
    return False


def is_spinning_top_bottom(open_price, high_price, low_price, close_price):
    """
    Method for check if candle is spinning top-bottom or not.

    Args:
        open_price (float): candle's open price
        high_price (float): candle's high price
        low_price (float): candle's low price
        close_price (float): candle's close price

    Returns:
        bool: True or False
    """
    if open_price == 0 and close_price == 0 and low_price == 0 and high_price == 0:
        return False

    if open_price == close_price == high_price == low_price:
        return False

    body = abs(close_price - open_price)  # Real body
    lower_shadow = 0
    upper_shadow = 0

    if close_price > open_price:
        upper_shadow = high_price - close_price
        lower_shadow = open_price - low_price
    else:
        upper_shadow = high_price - open_price
        lower_shadow = close_price - low_price

    if (lower_shadow >= body * 1.5) and (upper_shadow >= body * 1.5):
        return True

    return False


def is_doji(open_price, high_price, low_price, close_price):
    """
    Method for check if candle is doji or not.

    Args:
        open_price (float): candle's open price
        high_price (float): candle's high price
        low_price (float): candle's low price
        close_price (float): candle's close price

    Returns:
        bool: True or False
    """
    if open_price == close_price == high_price == low_price:
        return False

    if open_price == close_price:
        return True

    return False


def filter_data():
    """
    MEthod for filter the candlestick pattern data from all data
    """

    url = "https://api.upstox.com/v2/market-quote/quotes"

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json"}

    count = 0

    while count < 500:
        instrument_keys = INSTRUMENT_KEYS[count : count + 100]
        count = count + 100
        instrument_keys_str = ",".join(["NSE_EQ|" + s for s in instrument_keys])
        data = {"instrument_key": instrument_keys_str}

        # 100 instrument n one request
        response = requests.get(url, headers=headers, params=data, timeout=300)
        response = response.json()
        if response.get("status") == "success":
            equity_data = response.get("data")
            for key, value in equity_data.items():  # pylint:disable=W0612
                ohlc = value.get("ohlc", {})
                company_name = value.get("symbol")
                # check for hammer
                if is_hammer(
                    open_price=ohlc.get("open", 0),
                    close_price=ohlc.get("close", 0),
                    high_price=ohlc.get("high", 0),
                    low_price=ohlc.get("low", 0),
                ):
                    # Append to CSV
                    with open(
                        "Hammer.csv", mode="a", newline="", encoding="UTF-8"
                    ) as hammer_file:
                        writer = csv.writer(hammer_file)
                        writer.writerow([company_name])
                # check for doji
                if is_doji(
                    open_price=ohlc.get("open", 0),
                    close_price=ohlc.get("close", 0),
                    high_price=ohlc.get("high", 0),
                    low_price=ohlc.get("low", 0),
                ):
                    # Append to CSV
                    with open(
                        "Doji.csv", mode="a", newline="", encoding="UTF-8"
                    ) as doji_file:
                        writer = csv.writer(doji_file)
                        writer.writerow([company_name])
                # check for inverted hammer
                if is_inverted_hammer(
                    open_price=ohlc.get("open", 0),
                    close_price=ohlc.get("close", 0),
                    high_price=ohlc.get("high", 0),
                    low_price=ohlc.get("low", 0),
                ):
                    with open(
                        "Inverted_Hammer.csv", mode="a", newline="", encoding="UTF-8"
                    ) as inverted_hammer_file:
                        writer = csv.writer(inverted_hammer_file)
                        writer.writerow([company_name])
                # check for spinning top-bottom
                if is_spinning_top_bottom(
                    open_price=ohlc.get("open", 0),
                    close_price=ohlc.get("close", 0),
                    high_price=ohlc.get("high", 0),
                    low_price=ohlc.get("low", 0),
                ):
                    with open(
                        "Spinning_Top_Bottom.csv",
                        mode="a",
                        newline="",
                        encoding="UTF-8",
                    ) as spinning_top_bottom_file:
                        writer = csv.writer(spinning_top_bottom_file)
                        writer.writerow([company_name])


if __name__ == "__main__":
    # main method
    initialize_files()
    get_authorize_code()
    get_access_token()
    fetch_instrument_keys_from_csv()
    print("Filtering Data...")
    filter_data()
    print("Finished..!!")
