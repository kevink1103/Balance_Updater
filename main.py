import os
import time
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import pydata_google_auth
import gspread
from dotenv import load_dotenv
load_dotenv(verbose=True)

from exchanges import Bithumb

EXCHANGES = [Bithumb]

def get_google_credentials():
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = pydata_google_auth.get_user_credentials(scopes, auth_local_webserver=True)
    credentials.access_token = credentials.token
    return credentials

def get_balance_sheet_with_credentials(credentials):
    gc = gspread.authorize(credentials)
    sheet_url = os.getenv("SHEET_URL")
    doc = gc.open_by_url(sheet_url)
    worksheet = doc.worksheets()[0]
    return worksheet

def record_balance_to_balance_sheet(worksheet, exchange, balance):
    next_alphabet = lambda x: chr(ord(x) + 1)

    start_column = "A"
    start_row = EXCHANGES.index(exchange) * 2 + 1

    worksheet.update_acell(f"{start_column}{start_row}", exchange.__name__)
    worksheet.update_acell(f"{start_column}{start_row+1}", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    start_column = next_alphabet(start_column)

    for currency, balances in balance.items():
        available = balances["available"]
        total = balances["total"]

        worksheet.update_acell(f"{start_column}{start_row}", f"available_{currency}")
        worksheet.update_acell(f"{start_column}{start_row+1}", available)

        start_column = next_alphabet(start_column)

        worksheet.update_acell(f"{start_column}{start_row}", f"total_{currency}")
        worksheet.update_acell(f"{start_column}{start_row+1}", total)

        start_column = next_alphabet(start_column)
    print("UPDATED")

def runner(exchange, worksheet):
    try:
        balance = exchange.get_balance("BTC")
        record_balance_to_balance_sheet(worksheet, exchange, balance)
        # return balance
    except Exception as e:
        print(f"runner() error: {e}")

def main():
    credentials = get_google_credentials()
    worksheet = get_balance_sheet_with_credentials(credentials)

    threads = []
    while True:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for e in EXCHANGES:
                threads.append(executor.submit(runner, e, worksheet))
        # time.sleep(1)
    
    # for task in as_completed(threads):
    #     result = task.result()
    #     print(result, time.time())

if __name__ == "__main__":
    main()