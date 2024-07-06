import requests
import traceback

from stocks.write_file import write_to_file
from write_exception import write_exception

stock_name = 'DOGE'

def get_doge_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=usd'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        doge_price = data['dogecoin']['usd']
        doge_price = doge_price * 1000
        doge_price = round(doge_price, 2)

        write_to_file(stock_name, doge_price)

        return doge_price
    else:
        write_exception(traceback.format_exc())
        return None
    

if __name__ == "__main__":
    # Call the function to get the price and print it
    doge_price = get_doge_price()
    if doge_price:
        doge_price = doge_price * 1000
        print("Current Dogecoin Price: ${}".format(doge_price))