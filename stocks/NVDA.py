import requests
import sys
import os
import traceback

from stocks.write_file import write_to_file
from const import ROOT_DIR
from write_exception import write_exception

sys.path.insert(0, os.path.abspath(ROOT_DIR))

from money_bals import *

# https://finnhub.io/

def get_stock_price(symbol):
    api_key = 'cpiuom1r01qlu1879ii0cpiuom1r01qlu1879iig'  # Replace with your actual API key from Finnhub
    endpoint = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}'

    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()

        if 'c' not in data:
            print("Error: 'c' (current price) not found in the response.")
            print("Response:", data)
            return None

        stock_price = data['c']
        stock_price = float(stock_price)

        write_to_file(symbol, stock_price)

        return stock_price
    except requests.exceptions.RequestException:
        write_exception(traceback.format_exc())
        return None
    except Exception:
        write_exception(traceback.format_exc())
        return None

if __name__ == "__main__":
    symbol = 'NVDA'  # Nvidia's stock symbol
    stock_price = get_stock_price(symbol)
    if stock_price is not None:
        print(f"The current stock price of {symbol} is ${stock_price:.2f}")
    else:
        print("Failed to retrieve stock price.")
