from discord.ext import commands
import asyncio
import time
from money_bals import *
from commands.lichess import *
import re
import traceback

#I want an optional argument for the oppenent, so I can play against the bot.

from const import EXCEPTION_MESSAGE
from write_exception import write_exception

@commands.command()
async def chess(ctx, time: int, increment: int, amount: float, opponent=None):
    try:
        # Check if the user has a linked Lichess account
        lichess_data = load_lichess_data()
        user_id = str(ctx.author.id)
        if user_id not in lichess_data:
            await ctx.send("You need to link your Lichess account before creating a game. You can do that by using the `$lichess username` command.")
            return
        try:
            # Check if time, increment, and amount are valid
            if time <= 0 or increment < 0 or amount <= 0:
                await ctx.send("Time should be in minutes, increment should be in seconds, amount should be in dollars, and all numbers must be positive numbers.")
                return

            if time > 10:
                await ctx.send('The maximum amount of time allowed is 10 minutes.')
                return
            
            if increment > 5:
                await ctx.send('The maximum amount of increment allowed is 5 seconds.')
                return

            # Check if the user has enough money
            user_id = str(ctx.author.id)
            money_balances = read_money_balances()
            if user_id not in money_balances or money_balances[user_id] < amount:
                await ctx.send("You don't have enough money to play.")
                return

            time = time * 60

            # Generate game link
            game_link = generate_game_link(time, increment)

            # Send game link to users
            await ctx.send(f"{ctx.author.mention} has initiated a chess game. Type `$accept` to join the game.")

            # Wait for opponent's response
            def check_acceptance(message):
                return message.content.lower() == "$accept" and message.author != ctx.author

            try:
                acceptance_message = await ctx.bot.wait_for('message', check=check_acceptance, timeout=30)
                opponent = acceptance_message.author

                # Check if the opponent has a linked Lichess account
                opponent_id = str(opponent.id)
                if opponent_id not in lichess_data:
                    await ctx.send(f"{opponent.mention} you need to link your Lichess account before joining the game. You can do that by using the `$lichess username` command.")
                    return

                await ctx.send(f"Click here to play chess: {game_link}")
                game_id = game_link.split('/')[-1]
                print(game_id)
                result = get_game_result(game_id)
                print(result)

                #take the game result and update the money balances
                if result == "1-0":
                    money_balances[user_id] += amount
                    money_balances[opponent_id] -= amount
                    update_money_balance(money_balances)
                    await ctx.send(f"{ctx.author.mention} has won the game!")
                elif result == "0-1":
                    money_balances[user_id] -= amount
                    money_balances[opponent_id] += amount
                    update_money_balance(money_balances)
                    await ctx.send(f"{opponent.mention} has won the game!")
                else:
                    await ctx.send("The game ended in a draw.")

            except asyncio.TimeoutError:
                await ctx.send("No one accepted the game. The game has been cancelled.")

        except Exception:
            write_exception(traceback.format_exc())
            await ctx.send(EXCEPTION_MESSAGE)
    except BaseException:
        write_exception(traceback.format_exc())
        await ctx.send(EXCEPTION_MESSAGE)
        return None

def generate_game_link(time_control, increment):
    try:
        # Use Lichess API to create a new game
        response = requests.post('https://lichess.org/api/challenge/open', 
                                data={'clock.limit': str(time_control), 'clock.increment': str(increment)})
        
        # Check if the request was successful
        if response.status_code == 200:
            # Extract game ID from response
            game_id = response.json()['challenge']['id']
            
            # Generate link using game ID
            game_link = f"https://lichess.org/{game_id}"
            return game_link
        else:
            write_exception(traceback.format_exc())
            return None
    except Exception:
        write_exception(traceback.format_exc())
        return None

game_is_not_over = True

def get_game_result(game_id):
    global game_is_not_over
    while game_is_not_over:
        try:
            time.sleep(5)
            url = f"https://lichess.org/game/export/{game_id}"
            response = requests.get(url)
            if response.status_code == 200:
                # Parse PGN format
                pgn_data = response.text
                
                # Check for termination
                termination_match = re.search(r"\[Termination \"(.*?)\"\]", pgn_data)
                if termination_match:
                    termination = termination_match.group(1)
                    if termination != "Unterminated":
                        result_match = re.search(r"\[Result \"(.*?)\"\]", pgn_data)
                        if result_match:
                            result = result_match.group(1)
                            game_is_not_over = False
                            return result
                    else:
                        print("Game still in progress. Waiting for update...")
                else:
                    print("Game result not finalized yet. Waiting for update...")
            else:
                write_exception(traceback.format_exc())
                return None
        except Exception:
            write_exception(traceback.format_exc())