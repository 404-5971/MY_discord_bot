from discord.ext import commands
import asyncio
import json
from money_bals import *
import traceback

from const import USER_STOCKS, EXCEPTION_MESSAGE
from write_exception import write_exception

# Define your role IDs here
role_ids = {
    "role_1k": 1235445271920508998,  # Replace with actual role ID
    "role_10k": 1235445595695747123,  # Replace with actual role ID
    "role_100k": 1235445963280224308,  # Replace with actual role ID
    "role_1m": 1235446849876525137,  # Replace with actual role ID
    "role_1b": 1235448562460917780,  # Replace with actual role ID
    "role_1t": 1235448860457828443,  # Replace with actual role ID
    # Add more role IDs as needed
}

items = {
    "role_1k": 1000,  # Example item with price
    "role_10k": 10000,  # Add more items with their prices
    "role_100k": 100000,
    "role_1m": 1000000,
    "role_1b": 1000000000,
    "role_1t": 1000000000000,
    "RNG": 1000,
    "NVDA": 1000,
    "DOGE": 1000,
    "UP": 1000,
    "DOWN": 10000,
    "GAY": 5.2,
}

def update_stocks_json(buyer, stock_name, quantity, stock_price, money_balances):
    with open(USER_STOCKS, 'r') as f:
        stocks = json.load(f)

    if buyer in stocks:
        if stock_name in stocks[buyer]:
            stocks[buyer][stock_name] += quantity
        else:
            stocks[buyer][stock_name] = quantity
    else:
        stocks[buyer] = {stock_name: quantity}

    with open(USER_STOCKS, 'w') as f:
        json.dump(stocks, f, indent=4)  # Use indent=4 for pretty-printing

    total_cost = stock_price * quantity
    money_balances[buyer] -= total_cost
    update_money_balance(money_balances)

    return total_cost

@commands.command()
async def buy(ctx, item_name: str, quantity: int = 1):
    buyer = str(ctx.author.id)

    money_balances = read_money_balances()  # Load money balances

    if buyer not in money_balances:
        await ctx.send("You don't have any money balance yet.")
        return

    item_price = items.get(item_name)
    if item_price is None:
        await ctx.send("Sorry, that item is not available.")
        return

    total_price = item_price * quantity
    if money_balances[buyer] < total_price:
        await ctx.send(f"You don't have enough money to buy {quantity} of {item_name}. You need ${total_price:.2f}.")
        return

    await ctx.send(f"To confirm your purchase of {quantity} {item_name}(s) for ${total_price:.2f}, type `$confirm` or `$deny`.")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['$confirm', '$deny']

    try:
        confirmation = await ctx.bot.wait_for('message', check=check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.send("Timed out. Purchase canceled.")
        return

    if confirmation.content.lower() == '$deny':
        await ctx.send("Purchase canceled.")
        return

    if item_name in ['RNG', 'NVDA', 'DOGE', 'UP', 'DOWN', 'GAY']:
        total_cost = update_stocks_json(buyer, item_name, quantity, item_price, money_balances)
        await ctx.send(f"You've purchased {quantity} {item_name}(s) for ${total_cost:.2f}.")
        return

    # Grant role
    role_id = role_ids.get(item_name)
    role = ctx.guild.get_role(role_id)
    try:
        await ctx.author.add_roles(role)
        money_balances[buyer] -= item_price
        # Update the money balance and add the item to the inventory or perform relevant actions
        update_money_balance(money_balances)
        await ctx.send(f"You've purchased {item_name} for ${item_price:.2f} and received the corresponding role.")
    except Exception as e:
        await ctx.send(EXCEPTION_MESSAGE)
        write_exception(traceback.format_exc())
