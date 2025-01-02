"""
Script for analyze the chart pattern
"""

import os
import webbrowser

import requests
from dotenv import load_dotenv

import utils

load_dotenv()


# get credentials from .env file and define constant
CLIENT_ID = os.getenv("API_KEY")
CLIENT_SECRET = os.getenv("API_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")
CODE = ""
GRANT_TYPE = "authorization_code"
ACCESS_TOKEN = ""
INSTRUMENT_KEYS = utils.get_symbols()


def initialize_files():
    """
    Method for Initialize the csv files for store the Stocks name according to the pattern.
    """
    # initialize file for Hammer
    utils.write_to_csv_file(file_name="Hammer", mode="w", data="NAME")

    # initialize file for Doji
    utils.write_to_csv_file(file_name="Doji", mode="w", data="NAME")

    # initialize file for Inverted Hammer
    utils.write_to_csv_file(file_name="Inverted_Hammer", mode="w", data="NAME")

    # initialize file for Spinning Top-Bottom
    utils.write_to_csv_file(file_name="Spinning_Top_Bottom", mode="w", data="NAME")


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
                if utils.is_hammer(
                    open_price=ohlc.get("open", 0),
                    close_price=ohlc.get("close", 0),
                    high_price=ohlc.get("high", 0),
                    low_price=ohlc.get("low", 0),
                ):
                    # Append to CSV
                    utils.write_to_csv_file(
                        file_name="Hammer", mode="a", data=company_name
                    )
                # check for doji
                if utils.is_doji(
                    open_price=ohlc.get("open", 0),
                    close_price=ohlc.get("close", 0),
                    high_price=ohlc.get("high", 0),
                    low_price=ohlc.get("low", 0),
                ):
                    # Append to CSV
                    utils.write_to_csv_file(
                        file_name="Doji", mode="a", data=company_name
                    )
                # check for inverted hammer
                if utils.is_inverted_hammer(
                    open_price=ohlc.get("open", 0),
                    close_price=ohlc.get("close", 0),
                    high_price=ohlc.get("high", 0),
                    low_price=ohlc.get("low", 0),
                ):
                    # Append to CSV
                    utils.write_to_csv_file(
                        file_name="Inverted_Hammer", mode="a", data=company_name
                    )
                # check for spinning top-bottom
                if utils.is_spinning_top_bottom(
                    open_price=ohlc.get("open", 0),
                    close_price=ohlc.get("close", 0),
                    high_price=ohlc.get("high", 0),
                    low_price=ohlc.get("low", 0),
                ):
                    # Append to CSV
                    utils.write_to_csv_file(
                        file_name="Spinning_Top_Bottom", mode="a", data=company_name
                    )


if __name__ == "__main__":
    # main method
    initialize_files()
    get_authorize_code()
    get_access_token()
    print("Filtering Data...")
    filter_data()
    print("Finished..!!")
