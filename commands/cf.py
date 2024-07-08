from discord.ext import commands
import asyncio
import random
import time
from money_bals import *

@commands.command()
async def cf(ctx, *, args):
    # Split the arguments
    args = args.split()

    # Check if there are enough arguments
    if len(args) < 2:
        await ctx.send("Please provide both an opponent and an amount.")
        return

    # Check if the first argument is a valid member
    try:
        opponent = await commands.MemberConverter().convert(ctx, args[0])
    except commands.errors.MemberNotFound:
        await ctx.send("Please provide a valid member.")
        return

    # Check if the second argument is a valid amount
    try:
        amount = float(args[1])
    except ValueError:
        await ctx.send("Please enter a valid amount.")
        return

    # Check if the amount is positive
    if amount <= 0:
        await ctx.send("Please enter a positive amount.")
        return

    # Sender
    sender = ctx.author
    sender_username = sender.name
    sender_id = str(sender.id)

    # Load money balances
    sender_money_balances = load_money_data()

    # Check if the sender has enough money
    if sender_id not in sender_money_balances or sender_money_balances[sender_id] < amount:
        await ctx.send("You don't have enough money to challenge.")
        return

    # Opponent
    opponent_username = opponent.name
    opponent_id = str(opponent.id)

    # Check if the opponent is Eli Bot
    if opponent_username == "Eli Bot":
        await ctx.send("Eli Bot automatically accepts the challenge.")
        accept_challenge = True
    else:
        # Send challenge message
        challenge_message = await ctx.send(f"{opponent.mention}, {sender_username} has challenged you to a coin flip for ${amount:.2f}. Do you accept? (Respond with `$cf accept` or `$cf deny`)")

        # Wait for opponent's response
        def check_acceptance(message):
            if message.author != opponent:
                return False
            opponent_money_balances = load_money_data()
            return message.content.lower() in ["$cf accept", "$cf deny"] and opponent_money_balances[opponent_id] >= amount

        try:
            acceptance_message = await ctx.bot.wait_for('message', timeout=30.0, check=check_acceptance)
        except asyncio.TimeoutError:
            await ctx.send(f"{opponent.mention} didn't respond in time. Challenge canceled.")
            return

        if acceptance_message.content.lower() == "$cf deny":
            await ctx.send(f"{opponent.mention} has denied the challenge. Challenge canceled.")
            return

        accept_challenge = True

    if accept_challenge:
        # Generate a random number (0 or 1) for the coin flip
        result = random.randint(0, 1)

        # Determine the winner and update balances accordingly
        if result == 1:
            gif_message = await ctx.send("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXd3aXJ2bWt6M3cyaGhzdGx5MmduaWI2MzB6bHU2cHA0ejAza2p2MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RFjWmNVMXtACCxQ2yw/source.gif")
            sender_money_balances[sender_id] += amount
            sender_money_balances[opponent_id] -= amount
            time.sleep(4)
            await gif_message.delete()
            await ctx.send(f"Heads, {sender_username} wins!")
        else:
            gif_message = await ctx.send("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTl0MXI0eW5uZWU0aWQwNWJla3pydm1heXRjdTRjaXpjbWo3dXl3YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JBDHHdpzI6PUBQdxEg/source.gif")
            sender_money_balances[sender_id] -= amount
            sender_money_balances[opponent_id] += amount
            time.sleep(4)
            await gif_message.delete()
            await ctx.send(f"Tails, {opponent_username} wins!")

        # Update balances in the JSON file
        update_money_balance(sender_money_balances) 