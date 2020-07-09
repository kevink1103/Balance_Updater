import os
import time

from exchanges import Exchange
from bithumb_api import BithumbPublicAPI, BithumbPrivateAPI

BITHUMB_CONNECT_KEY = os.getenv("BITHUMB_CONNECT_KEY")
BITHUMB_SECRET_KEY = os.getenv("BITHUMB_SECRET_KEY")

class Bithumb(Exchange):
    @staticmethod
    def get_balance():
        api = BithumbPrivateAPI(BITHUMB_CONNECT_KEY, BITHUMB_SECRET_KEY)
        balance = api.info_balance(currency="BTC")
        if "data" in balance:
            balance_data = balance["data"]
            balance_data = {k:v for k, v in balance_data.items() if k.startswith("total_") or k.startswith("available_")}
            result = {}

            for k, v in balance_data.items():
                tag, currency = k.split("_")
                if currency not in result:
                    result[currency] = {}
                result[currency][tag] = v
            return result
        else:
            raise Exception("Something's wrong")

    @staticmethod
    def get_orderbook(ticker="BTC"):
        orderbook = BithumbPublicAPI.orderbook(order_currency=ticker, payment_currency="KRW", count=1)
        if "data" in orderbook:
            orderbook_data = orderbook["data"]
            result = {
                "ask": orderbook_data["asks"][0],
                "bid": orderbook_data["bids"][0],
                "spread": str(float(orderbook_data["asks"][0]["price"]) - float(orderbook_data["bids"][0]["price"]))
            }
            return result
