import os
import time

from exchanges import Exchange
from bithumb_api import BithumbPrivateAPI

BITHUMB_CONNECT_KEY = os.getenv("BITHUMB_CONNECT_KEY")
BITHUMB_SECRET_KEY = os.getenv("BITHUMB_SECRET_KEY")

class Bithumb(Exchange):
    @staticmethod
    def get_balance(currency="KRW"):
        api = BithumbPrivateAPI(BITHUMB_CONNECT_KEY, BITHUMB_SECRET_KEY)
        balance_data = api.info_balance(currency=currency)
        if "data" in balance_data:
            balance = balance_data["data"]
            balance = {k:v for k, v in balance.items() if k.startswith("total_") or k.startswith("available_")}
            result = {}

            for k, v in balance.items():
                tag, currency = k.split("_")
                if currency not in result:
                    result[currency] = {}
                result[currency][tag] = v
            return result
        else:
            raise Exception("Something's wrong")
