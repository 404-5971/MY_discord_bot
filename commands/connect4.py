import discord
from discord.ext import commands
import asyncio
import random
from money_bals import *

# Function to print the Connect 4 board
def print_board(board):
    output = ""
    for row in board:
        output += "|"
        for cell in row:
            output += "_" if cell == 0 else "X" if cell == 1 else "O"
            output += "|"
        output += "\n"
    output += " 1 2 3 4 5 6 7"
    return output

# Function to initialize the Connect 4 board
def initialize_board():
    return [[0 for _ in range(7)] for _ in range(6)]

# Function to check if a move is valid
def is_valid_move(board, column):
    return board[0][column] == 0

# Function to drop a piece onto the board
def drop_piece(board, column, player):
    for row in range(5, -1, -1):
        if board[row][column] == 0:
            board[row][column] = player
            break

# Function to check if a player has won
def check_winner(board, player):
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical
    for row in range(3):
        for col in range(7):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonals
    for row in range(3):
        for col in range(4):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
            if all(board[row + i][col + 3 - i] == player for i in range(4)):
                return True

    return False

# Command to initiate a Connect 4 game
@commands.command()
async def connect4(ctx, opponent: discord.Member, amount: float):
    # Sender
    sender = ctx.author
    sender_username = sender.name

    # Check if the sender is challenging themselves
    if opponent == sender:
        await ctx.send("You can't challenge yourself.")
        return

    # Check if the amount is positive
    if amount <= 0:
        await ctx.send("Please enter a positive amount.")
        return

    # Sender's information
    sender_id = str(sender.id)
    sender_money_balances = read_money_balances()

    # Load money balances
    sender_money_balances = load_money_data()

    # Check if the sender has enough money
    if sender_id not in sender_money_balances or sender_money_balances[sender_id] < amount:
        await ctx.send("You don't have enough money to challenge.")
        return

    # Opponent's information
    opponent_username = opponent.name
    opponent_id = str(opponent.id)

    if opponent_id == '1175890644191957013':
        await ctx.send("I haven't coded this in yet, and to do it I will have to learn a bunch of stuff like minimax and alpha-beta pruning. I which might do it in the future.")
        return

    # Check if the opponent has enough money
    opponent_money_balances = load_money_data()
    if opponent_id not in opponent_money_balances or opponent_money_balances[opponent_id] < amount:
        await ctx.send(f"{opponent.mention} doesn't have enough money to accept the challenge.")
        return

    # Send challenge message
    await ctx.send(f"{opponent.mention}, {sender_username} has challenged you to a game of Connect 4 for ${amount:.2f}. Do you accept? (Respond with `$connect4 accept` or `$connect4 deny`)")

    # Wait for opponent's response
    def check_acceptance(message):
        return message.author == opponent and message.content.lower() in ["$connect4 accept", "$connect4 deny"]

    try:
        acceptance_message = await ctx.bot.wait_for('message', timeout=30.0, check=check_acceptance)
    except asyncio.TimeoutError:
        await ctx.send(f"{opponent.mention} didn't respond in time. Challenge canceled.")
        return

    if acceptance_message.content.lower() == "$connect4 deny":
        await ctx.send(f"{opponent.mention} has denied the challenge. Challenge canceled.")
        return

    # Initialize the Connect 4 board
    board = initialize_board()

    # Set up the game
    players = [sender, opponent]
    symbols = [1, 2]  # 1 for player 1 (X), 2 for player 2 (O)
    current_player_index = random.randint(0, 1)
    current_player = players[current_player_index]
    current_symbol = symbols[current_player_index]

    thread = await ctx.channel.create_thread(name='Connect 4', type=discord.ChannelType.public_thread)
    game_message = await thread.send(f"{current_player.mention}, it's your turn.\n```\n{print_board(board)}\n```")

    # Play the game
    while True:
        def check_move(msg):
            return msg.author == current_player and msg.content.isdigit() and 1 <= int(msg.content) <= 7 and is_valid_move(board, int(msg.content) - 1)

        try:
            move_message = await ctx.bot.wait_for('message', timeout=60.0, check=check_move)
        except asyncio.TimeoutError:
            await ctx.send("Time's up! Game canceled.")
            return

        column = int(move_message.content) - 1
        drop_piece(board, column, current_symbol)

        await game_message.edit(content=f"{current_player.mention} has placed {current_symbol} in column {column + 1}.\n```\n{print_board(board)}\n```")

        if check_winner(board, current_symbol):
            await ctx.send(f"{current_player.mention} wins!")
            await thread.delete()
            sender_money_balances[sender_id] += amount if current_player == sender else -amount
            sender_money_balances[opponent_id] += amount if current_player == opponent else -amount
            update_money_balance(sender_money_balances)
            return

        if all(cell != 0 for row in board for cell in row):
            await ctx.send("It's a draw!")
            await thread.delete()
            return

        current_player_index = (current_player_index + 1) % 2
        current_player = players[current_player_index]
        current_symbol = symbols[current_player_index]
        await move_message.delete()
        await game_message.edit(content=f"{current_player.mention}, it's your turn.\n```\n{print_board(board)}\n```")
