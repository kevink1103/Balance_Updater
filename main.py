import os
import time
import datetime
# from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv
load_dotenv(verbose=True)
import pydata_google_auth
import gspread
import pandas as pd
from pyprnt import prnt

from exchanges import Bithumb

EXCHANGES = [Bithumb]
REFRESH_RATE = 1.2

START_COLUMN = os.getenv("START_CELL")[0]
START_ROW = int(os.getenv("START_CELL")[1])

# DATAFRAME = pd.DataFrame()
COUNTER = 0

def get_google_credentials():
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = pydata_google_auth.get_user_credentials(scopes, auth_local_webserver=True)
    credentials.access_token = credentials.token
    return credentials

def get_worksheet_with_credentials(credentials):
    gc = gspread.authorize(credentials)
    sheet_url = os.getenv("SHEET_URL")
    doc = gc.open_by_url(sheet_url)
    worksheet = doc.worksheets()[0]
    return worksheet

def get_start_row_index_for_exchange(exchange):
    return EXCHANGES.index(exchange) * 2 + START_ROW

def get_current_datetime_string():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def create_batch_data_for_sheet_update(exchange, balance, orderbook):
    next_alphabet = lambda x: chr(ord(x) + 1)

    batch_data = []

    start_column = START_COLUMN
    start_row = get_start_row_index_for_exchange(exchange)

    batch_data.append({
        "range": f"{start_column}{start_row}:{start_column}{start_row+1}",
        "values": [
            [exchange.__name__],
            [get_current_datetime_string()]
        ]
    })
    start_column = next_alphabet(start_column)

    for currency, balances in balance.items():
        available = balances["available"]
        total = balances["total"]

        batch_data.append({
            "range": f"{start_column}{start_row}:{start_column}{start_row+1}",
            "values": [
                [f"available_{currency}"],
                [available]
            ]
        })
        start_column = next_alphabet(start_column)

        batch_data.append({
            "range": f"{start_column}{start_row}:{start_column}{start_row+1}",
            "values": [
                [f"total_{currency}"],
                [total]
            ]
        })
        start_column = next_alphabet(start_column)

    for k, v in orderbook.items():
        if type(v) is dict:
            # either ask or bid
            for tag, value in v.items():
                batch_data.append({
                    "range": f"{start_column}{start_row}:{start_column}{start_row+1}",
                    "values": [
                        [f"{k}_{tag}"],
                        [value]
                    ]
                })
                start_column = next_alphabet(start_column)
        else:
            # spread
            batch_data.append({
                "range": f"{start_column}{start_row}:{start_column}{start_row+1}",
                "values": [
                    [f"{k}"],
                    [v]
                ]
            })
            start_column = next_alphabet(start_column)

    return batch_data

def runner(exchange, worksheet):
    try:
        start_t = time.time()
        balance = exchange.get_balance()
        orderbook = exchange.get_orderbook("BTC")
        print("EXCHAGNE API CALL TOOK: ", time.time() - start_t)

        start_t = time.time()
        batch_data = create_batch_data_for_sheet_update(exchange, balance, orderbook)
        worksheet.batch_update(batch_data)
        print("GOOGLE API CALL TOOK: ", time.time() - start_t)

        global COUNTER
        COUNTER += 1
        print("UPDATED", COUNTER)
        # return balance
    except Exception as e:
        print(f"runner() error: {e}")

def main():
    credentials = get_google_credentials()
    worksheet = get_worksheet_with_credentials(credentials)

    # threads = []
    while True:
        start_t = time.time()
        # with ThreadPoolExecutor(max_workers=20) as executor:
        #     for e in EXCHANGES:
        #         threads.append(executor.submit(runner, e, worksheet))
        for e in EXCHANGES:
            runner(e, worksheet)

        remain_t = REFRESH_RATE - (time.time() - start_t)
        if remain_t > 0:
            time.sleep(remain_t)
        print("ONE UPDATE TOOK: ", time.time() - start_t)
    
    # For Synchronous Update if needed
    # for task in as_completed(threads):
    #     result = task.result()
    #     print(result, time.time())


if __name__ == "__main__":
    main()
