from discord.ext import commands
import asyncio
import json
from money_bals import *
from commands.buy import items
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

def update_stocks_json_sell(buyer, stock_name, quantity, stock_price, money_balances):
    with open(USER_STOCKS, 'r') as f:
        stocks = json.load(f)

    if buyer in stocks and stock_name in stocks[buyer]:
        if stocks[buyer][stock_name] < quantity:
            return None, f"You don't have enough {stock_name} to sell."
        stocks[buyer][stock_name] -= quantity
        if stocks[buyer][stock_name] == 0:
            del stocks[buyer][stock_name]
    else:
        return None, f"You don't own any {stock_name}."

    with open(USER_STOCKS, 'w') as f:
        json.dump(stocks, f, indent=4)  # Use indent=4 for pretty-printing

    total_gain = stock_price * quantity
    money_balances[buyer] += total_gain
    update_money_balance(money_balances)

    return total_gain, None

@commands.command()
async def sell(ctx, item_name: str, quantity: int = 1):
    seller = str(ctx.author.id)

    money_balances = read_money_balances()  # Load money balances

    if seller not in money_balances:
        await ctx.send("You don't have any money balance yet.")
        return

    item_price = items.get(item_name)
    if item_price is None:
        await ctx.send("Sorry, that item is not available.")
        return

    total_price = item_price * quantity

    await ctx.send(f"To confirm your sale of {quantity} {item_name}(s) for ${total_price:.2f}, type `$confirm` or `$deny`.")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['$confirm', '$deny']

    try:
        confirmation = await ctx.bot.wait_for('message', check=check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.send("Timed out. Sale canceled.")
        return

    if confirmation.content.lower() == '$deny':
        await ctx.send("Sale canceled.")
        return

    if item_name in ['RNG', 'NVDA', "DOGE", "UP", "DOWN", 'GAY']:
        total_gain, error = update_stocks_json_sell(seller, item_name, quantity, item_price, money_balances)
        if error:
            await ctx.send(error)
        else:
            await ctx.send(f"You've sold {quantity} {item_name}(s) for ${total_gain:.2f}.")
        return

    # Revoke role
    role_id = role_ids.get(item_name)
    role = ctx.guild.get_role(role_id)
    try:
        await ctx.author.remove_roles(role)
        money_balances[seller] += item_price
        # Update the money balance and perform relevant actions
        update_money_balance(money_balances)
        await ctx.send(f"You've sold {item_name} for ${item_price:.2f} and the corresponding role has been removed.")
    except Exception:
        await ctx.send(EXCEPTION_MESSAGE)
        write_exception(traceback.format_exc())