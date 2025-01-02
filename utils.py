"""
Script has Utility Methods
"""

import csv
import os
from datetime import datetime, timedelta


def get_symbols():
    """
    Method for get the instruments key of Nifty500 Stocks.
    """
    csv_file_path = "Nifty500.csv"
    # key_column = "ISIN Code"
    # value_column = "Symbol"
    column_name = "ISIN Code"

    # Initialize the dictionary
    result = []

    # Open and read the CSV file
    with open(csv_file_path, mode="r", encoding="UTF-8") as file:
        reader = csv.DictReader(file)  # Use DictReader to access columns by name
        for row in reader:
            result.append(row[column_name])

    return result


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


def symbol_purify(symbol):
    """
    Method for purify the symbol for use in query params
    """
    symbol = symbol.replace("&", "%26")  # URL Parse for Stocks Like M&M Finance
    return symbol


def get_last_friday():
    """
    Method for get the last friday date

    Returns:
        _type_: _description_
    """
    today = datetime.today()
    # Calculate the number of days to subtract to get to last Friday
    days_since_last_friday = (today.weekday() - 4) % 7
    last_friday = today - timedelta(days=days_since_last_friday)
    return last_friday.date()


def is_bullish_engulfing(first_candle, second_candle):
    """
    Method for bullish engulfing candle stick pattern.
    """

    # first_high = first_candle.get("CH_TRADE_HIGH_PRICE")
    # first_low = first_candle.get("CH_TRADE_LOW_PRICE")
    first_open = first_candle.get("CH_OPENING_PRICE")
    first_close = first_candle.get("CH_CLOSING_PRICE")

    # second_high = second_candle.get("CH_TRADE_HIGH_PRICE")
    # second_low = second_candle.get("CH_TRADE_LOW_PRICE")
    second_open = second_candle.get("CH_OPENING_PRICE")
    second_close = second_candle.get("CH_CLOSING_PRICE")

    # Check if the first candle is bearish
    is_first_bearish = first_close < first_open

    # Check if the second candle is bullish
    is_second_bullish = second_close > second_open

    # Check if the second candle engulfs the first candle
    is_engulfing = (second_open <= first_close) and (second_close >= first_open)

    # Return True if all conditions are met
    return is_first_bearish and is_second_bullish and is_engulfing


def write_to_csv_file(file_name, data, mode):
    """
    Method for write into CSV File
    """
    if not os.path.exists("CandleStick"):
        os.mkdir("CandleStick")

    date_folder_path = os.path.join("CandleStick", datetime.now().strftime("%d-%m-%Y"))
    if not os.path.exists(date_folder_path):
        os.mkdir(date_folder_path)

    file_path = os.path.join(date_folder_path, f"{file_name}.csv")
    with open(file_path, mode=mode, newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow([data])


def get_date_for_one_candle():
    """
    Method for generate date for one candle pattern

    Returns:
        str: date for one candle pattern
    """
    date = ""
    if datetime.now().strftime("%A") in ["Sunday", "Saturday"]:
        date = get_last_friday().strftime("%d-%m-%Y")
    else:
        date = datetime.now().strftime("%d-%m-%Y")

    return date


def get_date_for_two_candle():
    """
    Method for generate date for two candle pattern

    Returns:
        list: starting and ending date
    """
    from_date = ""
    to_date = ""
    if datetime.now().strftime("%A") == "Monday":
        from_date = datetime.now() - timedelta(days=3)
        to_date = datetime.now()
    elif datetime.now().strftime("%A") in ["Sunday", "Saturday"]:
        to_date = get_last_friday()
        from_date = to_date - timedelta(days=1)
    else:
        from_date = datetime.now() - timedelta(days=1)
        to_date = datetime.now().strftime("%d-%m-%Y")

    from_date = from_date.strftime("%d-%m-%Y")
    to_date = to_date.strftime("%d-%m-%Y")

    return [from_date, to_date]


def is_bearish_engulfing(first_candle, second_candle):
    """
    Method for bearish engulfing candle stick pattern.
    """

    # first_high = first_candle.get("CH_TRADE_HIGH_PRICE")
    # first_low = first_candle.get("CH_TRADE_LOW_PRICE")
    first_open = first_candle.get("CH_OPENING_PRICE")
    first_close = first_candle.get("CH_CLOSING_PRICE")

    # second_high = second_candle.get("CH_TRADE_HIGH_PRICE")
    # second_low = second_candle.get("CH_TRADE_LOW_PRICE")
    second_open = second_candle.get("CH_OPENING_PRICE")
    second_close = second_candle.get("CH_CLOSING_PRICE")

    # Check if the first candle is bullish
    is_first_bullish = first_close > first_open

    # Check if the second candle is bearish
    is_second_bearish = second_close < second_open

    # Check if the second candle engulfs the first candle
    is_engulfing = (second_open >= first_close) and (second_close <= first_open)

    # Return True if all conditions are met
    return is_first_bullish and is_second_bearish and is_engulfing


def is_bullish_kicker(first_candle, second_candle):
    """
    Method for bullish kicker candle stick pattern.
    """
    first_high = first_candle.get("CH_TRADE_HIGH_PRICE")
    # first_low = first_candle.get("CH_TRADE_LOW_PRICE")
    first_open = first_candle.get("CH_OPENING_PRICE")
    first_close = first_candle.get("CH_CLOSING_PRICE")

    # second_high = second_candle.get("CH_TRADE_HIGH_PRICE")
    second_low = second_candle.get("CH_TRADE_LOW_PRICE")
    second_open = second_candle.get("CH_OPENING_PRICE")
    second_close = second_candle.get("CH_CLOSING_PRICE")

    # check if the first candle is bearish
    is_first_bearish = first_close < first_open

    # check if the second candle is bullish
    is_second_bullish = second_close > second_open

    # No overlap in prices
    no_overlap = first_high <= second_low

    return is_first_bearish and is_second_bullish and no_overlap


def is_bearish_kicker(first_candle, second_candle):
    """
    Method for bearish kicker candle stick pattern.
    """
    # first_high = first_candle.get("CH_TRADE_HIGH_PRICE")
    first_low = first_candle.get("CH_TRADE_LOW_PRICE")
    first_open = first_candle.get("CH_OPENING_PRICE")
    first_close = first_candle.get("CH_CLOSING_PRICE")

    second_high = second_candle.get("CH_TRADE_HIGH_PRICE")
    # second_low = second_candle.get("CH_TRADE_LOW_PRICE")
    second_open = second_candle.get("CH_OPENING_PRICE")
    second_close = second_candle.get("CH_CLOSING_PRICE")

    # check if the first candle is bullish
    is_first_bullish = first_close > first_open

    # check if the second candle is bearish
    is_second_bearish = second_close < second_open

    # No overlap in prices
    no_overlap = first_low >= second_high

    return is_first_bullish and is_second_bearish and no_overlap


def is_pro_gap_positive(first_candle, second_candle):
    """
    Method for bearish kicker candle stick pattern.
    """
    # first_high = first_candle.get("CH_TRADE_HIGH_PRICE")
    # first_low = first_candle.get("CH_TRADE_LOW_PRICE")
    first_open = first_candle.get("CH_OPENING_PRICE")
    first_close = first_candle.get("CH_CLOSING_PRICE")

    # second_high = second_candle.get("CH_TRADE_HIGH_PRICE")
    # second_low = second_candle.get("CH_TRADE_LOW_PRICE")
    second_open = second_candle.get("CH_OPENING_PRICE")
    second_close = second_candle.get("CH_CLOSING_PRICE")

    # check if the first candle is bearish
    is_first_bearish = first_close < first_open

    # check if the second candle is bullish
    is_second_bullish = second_close > second_open

    # condition for pro gap
    gap_positive = second_open > first_close

    return is_first_bearish and is_second_bullish and gap_positive
