# Balance Updater

Update Google Sheet periodically (every 1.2sec) to keep track of crypto asset balances (using [PyBithumb_API](https://github.com/kevink1103/PyBithumb_API))

## Get Started

### Step 1 - Clone this repo

```bash
git clone https://github.com/kevink1103/Balance_Updater.git
cd balance_updater
```

### Step 2 - Set Environment Variables

```bash
mv example.env .env
vi .env
```

```
SHEET_URL=https://docs.google.com/spreadsheets/d/13vUOOTjdfrRM_EvLPatbKGKSQlL0w5Z2yUJ2o3Jdeyg/edit#gid=0

BITHUMB_CONNECT_KEY=a41a7e553de1adc161f9fa1e3faf1e4e
BITHUMB_SECRET_KEY=1de7e77d93a8e31951763b7087d7db9a
```

- SHEET_URL : an url to your google sheet (make and open a sheet and copy & paste the link here)
- BITHUMB_CONNECT_KEY, BITHUMB_SECRET_KEY : get these from Bithumb website API section

### Step 3 - Install Dependencies and Run!

```bash
pipenv install
pipenv run python3 main.py
```

## Disclaimer

> This program will record (update) all the balances you have on Bithumb in `First Worksheet` of the provided Google Sheet. Make sure you do not have any important data in `First Worksheet` before you run this program.

## Todo

Use Pandas and enable multithreading if more than one exchange has to be integrated with this program in the future. Then, update the whole sheet with the Pandas DataFrame.

# Author

Kevin Kim
