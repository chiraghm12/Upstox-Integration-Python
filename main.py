import csv
import os
import webbrowser

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("API_KEY")
CLIENT_SECRET = os.getenv("API_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")
CODE = ""
# CODE=os.getenv("CODE")
GRANT_TYPE = "authorization_code"
ACCESS_TOKEN = ""
INSTRUMENT_KEYS = []


def initialize_files():
    # initialize file for Hammer
    with open("hammer.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name"])

    # initialize file for Doji
    with open("doji.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name"])


def get_authorize_code():
    url = f"https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}"
    webbrowser.open_new_tab(url)
    c = input("Enter Code : ")
    global CODE
    CODE = c
    # print("Code is : ", CODE)


def get_access_token():
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

    response = requests.post(url, headers=headers, data=payload)
    global ACCESS_TOKEN
    ACCESS_TOKEN = response.json().get("access_token")
    # print(response.text)


def fetch_instrument_keys_from_csv():
    # Path to your CSV file
    csv_file_path = "Nifty500.csv"
    # column_name = ["instrument_key", "tradingsymbol", "name"]
    column_name = "ISIN Code"
    global INSTRUMENT_KEYS

    # Open and read the CSV file
    with open(csv_file_path, mode="r") as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name
        for row in reader:
            # Extract only the desired columns
            # filtered_row = {col: row[col] for col in column_name}
            INSTRUMENT_KEYS.append(row[column_name])

    # print("Column values:", len(INSTRUMENT_KEYS))


def is_hammer(open_price, high_price, low_price, close_price):
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

    # upper_shadow = high_price - max(open_price, close_price)
    # lower_shadow = min(open_price, close_price) - low_price

    # Check conditions for a Hammer
    # if (
    #     body <= (high_price - low_price) * 0.3 and  # Small real body
    #     lower_shadow >= 2 * body and                # Long lower wick
    #     upper_shadow <= body * 0.1                # Minimal upper wick
    # ):
    if (lower_shadow >= (body * 2)) and (upper_shadow <= (body * 0.3)):
        return True
    return False


def is_doji(open_price, high_price, low_price, close_price):
    if open_price == close_price == high_price == low_price:
        return False

    if open_price == close_price:
        return True

    return False


def filter_data():

    url = "https://api.upstox.com/v2/market-quote/quotes"

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json"}

    count = 0

    while count < 500:
        instrument_keys = INSTRUMENT_KEYS[count : count + 100]
        count = count + 100
        instrument_keys_str = ",".join(["NSE_EQ|" + s for s in instrument_keys])

        data = {"instrument_key": instrument_keys_str}

        response = requests.get(url, headers=headers, params=data)
        response = response.json()
        if response.get("status") == "success":
            equity_data = response.get("data")
            for key, value in equity_data.items():
                ohlc = value.get("ohlc", {})
                company_name = value.get("symbol")
                if is_hammer(
                    open_price=ohlc.get("open", 0),
                    close_price=ohlc.get("close", 0),
                    high_price=ohlc.get("high", 0),
                    low_price=ohlc.get("low", 0),
                ):
                    # Append to CSV
                    with open("hammer.csv", mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([company_name])

                if is_doji(
                    open_price=ohlc.get("open", 0),
                    close_price=ohlc.get("close", 0),
                    high_price=ohlc.get("high", 0),
                    low_price=ohlc.get("low", 0),
                ):
                    # Append to CSV
                    with open("doji.csv", mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([company_name])


if __name__ == "__main__":
    initialize_files()
    get_authorize_code()
    get_access_token()
    fetch_instrument_keys_from_csv()
    filter_data()
