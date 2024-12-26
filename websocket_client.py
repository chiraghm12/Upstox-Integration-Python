"""
Script for websocket client
"""

import asyncio
import json
import os
import ssl
import webbrowser

import requests
import upstox_client
import websockets
from dotenv import load_dotenv
from google.protobuf.json_format import MessageToDict

import MarketDataFeed_pb2 as pb

load_dotenv()


# get credentials from .env file and define constant
CLIENT_ID = os.getenv("API_KEY")
CLIENT_SECRET = os.getenv("API_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")
CODE = ""
GRANT_TYPE = "authorization_code"
ACCESS_TOKEN = ""
INSTRUMENT_KEYS = []
AUTHORIZED_WEBSOCKET_URL = ""


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


def get_authorize_url():
    """
    Method for get the authorizeurl for connect the websocket for live data.
    """
    global AUTHORIZED_WEBSOCKET_URL
    url = "https://api.upstox.com/v2/feed/market-data-feed/authorize"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json"}

    response = requests.get(url, headers=headers, timeout=300)

    AUTHORIZED_WEBSOCKET_URL = response.json().get("data").get("authorizedRedirectUri")


def decode_protobuf(buffer):
    """Decode protobuf message."""
    feed_response = pb.FeedResponse()
    feed_response.ParseFromString(buffer)
    return feed_response


async def fetch_market_data():
    """Fetch market data using WebSocket and print it."""

    # Create default SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Configure OAuth2 access token for authorization
    configuration = upstox_client.Configuration()

    # api_version = "2.0"
    configuration.access_token = "ACCESS_TOKEN"

    # Get market data feed authorization
    # response = get_market_data_feed_authorize(
    #     api_version, configuration)

    # Connect to the WebSocket with SSL context
    async with websockets.connect(
        AUTHORIZED_WEBSOCKET_URL, ssl=ssl_context
    ) as websocket:
        print("Connection established")

        await asyncio.sleep(1)  # Wait for 1 second

        # Data to be sent over the WebSocket
        data = {
            "guid": "someguid",
            "method": "sub",
            "data": {
                "mode": "full",
                "instrumentKeys": ["NSE_INDEX|Nifty Bank", "NSE_INDEX|Nifty 50"],
            },
        }

        # Convert data to binary and send over WebSocket
        binary_data = json.dumps(data).encode("utf-8")
        await websocket.send(binary_data)

        # Continuously receive and decode data from WebSocket
        while True:
            message = await websocket.recv()
            decoded_data = decode_protobuf(message)

            # Convert the decoded data to a dictionary
            data_dict = MessageToDict(decoded_data)

            # Print the dictionary representation
            print("Data: -----------------------------------------")
            print(json.dumps(data_dict))


if __name__ == "__main__":
    # main method
    get_authorize_code()
    get_access_token()
    get_authorize_url()
    asyncio.run(fetch_market_data())
