import json

from stocks.write_file import write_to_file
from const import STOCK_HISTORY_FILE

try:
    with open(STOCK_HISTORY_FILE, 'r') as file:
        stock_history = json.load(file)
        num = stock_history['UP'][-1]
except:
    num = 1

STOCK_NAME = 'UP'

def generate_stock_price():
    global num
    num_zeros = len(str(int(num)))
    if num_zeros == 1:
        multiplier = 1.1  # Minimum multiplier to avoid constant value
    elif num_zeros >= 2:
        multiplier = 1
        for _ in range(num_zeros):
            multiplier = str(multiplier) + '0' 
        multiplier = insert_decimal(multiplier)
    num *= multiplier

    write_to_file(STOCK_NAME, num)

    return num


def insert_decimal(num):
    num_str = num
    result = num_str[:1] + '.' + num_str[1:]
    result += '1'
    return float(result)  # Convert back to float if needed