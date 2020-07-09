import os
import time
from abc import ABCMeta, abstractmethod
from multiprocessing import Pool

import pydata_google_auth
import gspread

from bithumb_api import BithumbPublicAPI, BithumbPrivateAPI

from dotenv import load_dotenv
load_dotenv(verbose=True)

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
SHEET_URL = os.getenv("SHEET_URL")

BITHUMB_CONNECT_KEY = os.getenv("BITHUMB_CONNECT_KEY")
BITHUMB_SECRET_KEY = os.getenv("BITHUMB_SECRET_KEY")

class Exchange(metaclass=ABCMeta):
    @abstractmethod
    def get_balance(self):
        pass

class Bithumb(Exchange):
    @staticmethod
    def get_balance(currency="KRW"):
        api = BithumbPrivateAPI(BITHUMB_CONNECT_KEY, BITHUMB_SECRET_KEY)
        balance_data = api.info_balance(currency="BTC")
        if "data" in balance_data and "available_krw" in balance_data["data"]:
            balance = balance_data["data"]["available_krw"]
            return balance
        else:
            raise Exception("Something's wrong")

def get_pool_size():
    all_keys = [
        BITHUMB_CONNECT_KEY, BITHUMB_SECRET_KEY
    ]
    all_keys = list(filter(lambda x: x, all_keys))
    return len(all_keys) // 2

def get_google_credentials():
    credentials = pydata_google_auth.get_user_credentials(SCOPES, auth_local_webserver=True)
    credentials.access_token = credentials.token
    return credentials

def get_balance_sheet(credentials):
    gc = gspread.authorize(credentials)
    doc = gc.open_by_url(SHEET_URL)
    worksheet = doc.worksheets()[0]
    return worksheet

def smap(f):
    result = f()
    time.sleep(1)
    return result

def main():
    # credentials = get_google_credentials()
    # worksheet = get_balance_sheet()
    # cell_data = worksheet.acell("A1").value
    # print(cell_data)

    # balance = getBithumbBalance("BTC")
    # print(balance)

    # while (True):
    #     balance = getBithumbBalance("BTC")
    #     print(balance)
    #     time.sleep(1)

    pool_size = get_pool_size()

    pool = Pool(processes=pool_size)

    while True:
        res = pool.map(smap, [Bithumb.get_balance])
        # pool.close()
        # pool.join()
        print(res)

if __name__ == "__main__":
    main()