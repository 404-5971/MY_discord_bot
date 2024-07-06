import json

from commands.buy import items
from const import STOCK_HISTORY_FILE

def write_to_file(stock_name, stock_value):
    items[stock_name] = stock_value

    # Read the current stock history from the file
    try:
        with open(STOCK_HISTORY_FILE, 'r') as file:
            stock_history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        stock_history = {}

    # Ensure 'demostock' is a list in the stock history
    if stock_name not in stock_history:
        stock_history[stock_name] = []

    # Append the new value to the list
    stock_history[stock_name].append(stock_value)

    # Write the updated stock history back to the file
    with open(STOCK_HISTORY_FILE, 'w') as file:
        json.dump(stock_history, file, indent=4)