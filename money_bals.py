import json
import traceback

from const import MONEY_JSON_FILEPATH
from write_exception import write_exception

# Function to load money data from money.json
def load_money_data():
    try:
        with open(MONEY_JSON_FILEPATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        write_exception(traceback.format_exc())
        return {}

# Function to save money data to money.json
def save_money_data(money_data):
    with open(MONEY_JSON_FILEPATH, 'w') as f:
        json.dump(money_data, f, indent=4)

# Function to read money balances from money.json
def read_money_balances():
    return load_money_data()

# Function to update money balance in money.json
def update_money_balance(money_balances):
    save_money_data(money_balances)