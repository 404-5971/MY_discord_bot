import requests
from discord.ext import commands
from money_bals import *
import traceback

from const import LICHESS_JSON_FILEPATH, EXCEPTION_MESSAGE
from write_exception import write_exception

LICHESS_API_URL = 'https://lichess.org/api/user/'

# Function to load Lichess account data from JSON file
def load_lichess_data():
    try:
        with open(LICHESS_JSON_FILEPATH, 'r') as f:
            return json.load(f)
    except Exception:
        write_exception(traceback.format_exc())
        return {}

# Function to save Lichess account data to JSON file
def save_lichess_data(lichess_data):
    with open(LICHESS_JSON_FILEPATH, 'w') as f:
        json.dump(lichess_data, f, indent=4)

# Function to add user's Lichess account to data
def add_lichess_account(user_id, account_name):
    lichess_data = load_lichess_data()
    lichess_data[str(user_id)] = account_name
    save_lichess_data(lichess_data)

# Function to check if Lichess account exists
def check_lichess_account_exists(account_name):
    response = requests.get(f"{LICHESS_API_URL}{account_name}")
    return response.status_code == 200

# Command to add user's Lichess account
@commands.command()
async def lichess(ctx, account_name):
    try:
        # Check if the account name is provided
        if not account_name:
            await ctx.send("Please provide your Lichess account name.")
            return

        # Check if the Lichess account exists
        if not check_lichess_account_exists(account_name):
            await ctx.send("The provided Lichess account does not exist.")
            return

        # Add user's Lichess account to data
        add_lichess_account(ctx.author.id, account_name)
        await ctx.send(f"Your Lichess account '{account_name}' has been added successfully.")

    except Exception:
        write_exception(traceback.format_exc())
        await ctx.send(EXCEPTION_MESSAGE)