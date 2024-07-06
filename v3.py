import discord
from discord.ext import commands
import csv
import asyncio
from PIL import Image, ImageDraw, ImageFont
import os
import random
import openai
import time
import traceback

from money_bals import *
from commands.cf import cf
from commands.sudo import sudo
from commands.ttt import ttt
from commands.lichess import *
from commands.chess import chess
from commands.buy import buy
from commands.sell import sell
from commands.leaderboard import *
from commands.connect4 import connect4
from commands.stock import stock

from stocks.graph import draw_graph
from stocks.RNG import stock1
from stocks.NVDA import get_stock_price
from stocks.DOGE import *
from stocks.UP import *
from stocks.DOWN import DOWN
from stocks.GAY import get_gayness

from const import CACHE_DIR, TIMEOUT_COUNT_DIR, EXCEPTION_MESSAGE, STOCK_GRAPH_PIC

from write_exception import write_exception

openai.api_key = 'sk-krazykai-bot-vtzun36Z4wPOp524MQp3T3BlbkFJAwOW7RkfZrjZIr3YVu5y'
UNSPLASH_ACCESS_KEY = 'Hml8JmR7UZk1bxjqVnac99UdBRGId69CUbtdHmC2aW0'

# Record the start time
start_time = time.time()

NVDA_stock_price = get_stock_price('NVDA')
RNG_stock_price = stock1()
DOGE_stock_price = get_doge_price()
UP_stock_price = generate_stock_price()
DOWN_stock_price = DOWN()
GAY_stock_price = get_gayness()

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

# Override the default help command
bot.remove_command('help')  # Remove the default help command

# Event listener for when the bot is ready
@bot.event
async def on_ready():
    global start_time
    print(f'{bot.user} has connected to Discord!')
    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    print("Time to start up", round(elapsed_time, 2), "seconds")
    await asyncio.gather(async_timer1())

@bot.event
async def on_message(message):
    try:
        print(f'User: {message.author.name}, Message: {message.content}, Channel: {message.channel.name}')
    except:
        print(f'User: {message.author.name}, Message: {message.content}, Channel: DM')
    # Reload money data from JSON
    money_data = load_money_data()

    user_id = str(message.author.id)

    # Increment user's money by 1
    money_data.setdefault(user_id, 0)  # Set default value to 0 if user ID doesn't exist
    money_data[user_id] += 1

    save_money_data(money_data)

    await bot.process_commands(message)

@bot.command()
async def money(ctx):
    # Reload money data from JSON
    money_data = load_money_data()

    user_id = str(ctx.author.id)
    money = money_data.get(user_id, 0)
    formatted_balance = "{:,.2f}".format(money)  # Adding commas to the money balance
    await ctx.send(f'You have ${formatted_balance}')

# Command to send money to another user
@bot.command()
async def send(ctx, recipient: discord.Member, amount: float):
    sender_id = str(ctx.author.id)
    recipient_id = str(recipient.id)
    
    # Load money balances
    money_balances = load_money_data()

    if amount < 0:  # Check if amount is negative
        await ctx.send("You cannot send a negative amount of money.")
        return

    if sender_id not in money_balances:
        await ctx.send("You don't have any money balance yet.")
        return

    if money_balances[sender_id] < amount:
        await ctx.send("You don't have enough money to send.")
        return

    await ctx.send(f"To continue with your transaction of ${amount:.2f} to {recipient.name}, type `$confirm` or `$deny`.")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['$confirm', '$deny']

    try:
        confirmation = await bot.wait_for('message', check=check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.send("Timed out. Transaction canceled.")
        return

    if confirmation.content.lower() == '$deny':
        await ctx.send("Transaction canceled.")
        return

    money_balances[sender_id] -= amount
    money_balances[recipient_id] = money_balances.get(recipient_id, 0) + amount
    update_money_balance(money_balances)
    await ctx.send(f"You've sent ${amount:.2f} to {recipient.name}.")


timeout_counts = {}

# Function to read timeout_counts from the CSV file
def read_timeout_counts(filename):
    timeout_counts = {}
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                timeout_counts[int(row['user_id'])] = int(row['count'])
    except FileNotFoundError:
        write_exception(traceback.format_exc())
        pass
    return timeout_counts

# Function to update timeout_counts in the CSV file
def update_timeout_counts(filename, counts):
    with open(filename, 'w', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=['user_id', 'count'])
        csv_writer.writeheader()
        for user_id, count in counts.items():
            csv_writer.writerow({'user_id': user_id, 'count': count})

# Load timeout_counts when the bot starts up
timeout_counts = read_timeout_counts(TIMEOUT_COUNT_DIR)

@bot.command()
async def bug(ctx, *, message):
    # Replace 'hard_coded_user_id' with the user ID you want to DM
    user = await bot.fetch_user(746842205347381338)
    # Send a DM to the hardcoded user
    await user.send(f"Bug report from {ctx.author.display_name}: {message}")
    await ctx.message.add_reaction("✅")

@bot.event
async def on_member_update(before, after):
    global timeout_counts
    if before.timed_out_until is None:
        if after.timed_out_until is not None:
            print(f"****Member {after} was timed out!****")
            if after.id in timeout_counts:
                timeout_counts[after.id] += 1
            else:
                timeout_counts[after.id] = 1
            
            if timeout_counts[after.id] == 5:
                print(f'{after} has been timed out 5 times.')
                # Give the user a role here
                role = discord.utils.get(after.guild.roles, name="Gay🏳️‍🌈Baby👶Jail⛓️")
                if role:
                    await after.add_roles(role)
                    timeout_counts[after.id] = 0
                else:
                    print("We couldn't find the role")

            # Save timeout_counts to the CSV file after each update
            update_timeout_counts(TIMEOUT_COUNT_DIR, timeout_counts)

@bot.event
async def on_user_update(before, after):
    # Check if the user has updated their profile picture
    if before.avatar != after.avatar:
        # Check if the user has a new avatar
        if after.avatar:
            # Download the new profile picture
            profile_picture_response = requests.get(after.avatar.url, stream=True)
            profile_picture_response.raise_for_status()
            profile_picture = Image.open(profile_picture_response.raw)
            
            # Save the new profile picture to the cache directory
            profile_picture_path = os.path.join(CACHE_DIR, f"{after.id}.png")
            profile_picture.save(profile_picture_path)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency is {latency}ms')

# Command to display help
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="List of available commands", color=discord.Color.blue())
    embed.add_field(name="`$money`", value="This command allows you to check your balance.", inline=False)
    embed.add_field(name="`$send @username amount`", value="This command allows you to send money to other users.", inline=False)
    embed.add_field(name="`$cf @username amount`", value="This command allows you to challenge another user to a coinflip. You can ping Eli Bot, and play against him!", inline=False)
    embed.add_field(name="`$shop`", value="This command allows you to see all the items you can buy!", inline=False)
    embed.add_field(name="`$games`", value="This command allows you to see the list of available games.", inline=False)
    embed.add_field(name="`$bug your_message`", value="This command allows you to report any bugs you find to me. When the bot adds the check mark reaction that means that your message got sent.", inline=False)
    embed.add_field(name="`$utilitys`", value="This command allows you to see the list of available utility's", inline=False)
    embed.add_field(name="Additional Information", value="Please note this bot is in beta, if you find any bugs or glitches please use the `$bug message` command.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def utilitys(ctx):
    embed = discord.Embed(title="Utility's", description="List of available utility's", color=discord.Color.blue())
    embed.add_field(name="`$ping`", value="This command allows you to check the latency of the bot.", inline=False)
    embed.add_field(name="`$ip`", value="This command allows you to check your IP address.", inline=False)
    embed.add_field(name="`$roll number`", value="This command allows you to roll a number between 1 and the number you provide.", inline=False)
    embed.add_field(name="`$picture`", value="This command allows you to see a random picture.", inline=False)
    embed.add_field(name="`$ai question`", value="This command allows you to ask AI a question.", inline=False)
    embed.add_field(name="Additional Information", value="Please note this bot is in beta, if you find any bugs or glitches please use the `$bug message` command.", inline=False)
    await ctx.send(embed=embed)

bot.add_command(sudo)

bot.add_command(cf)

@bot.command()
async def games(ctx):
    embed = discord.Embed(title="Games", description="List of available games", color=discord.Color.blue())
    embed.add_field(name="`$cf @username amount`", value="In this game you challenge another user to a coinflip.", inline=False)
    embed.add_field(name="`$chess time increment amount`", value="In this game you challenge another user to a game of chess.", inline=False)
    embed.add_field(name="`$bj amount`", value="This game is black jack. (Coming soon!)", inline=False)
    embed.add_field(name="`$ttt @username amount`", value="In this game you challenge another user to a game of Tic Tac Toe.", inline=False)
    embed.add_field(name="`$connent4 @username amount`", value="In this game you challenge another user to a game of connect 4. (Coming soon!)", inline=False)
    embed.add_field(name="Additional Information", value="All games can be played with Eli Bot! Just ping him in the @username section of the command.", inline=False)
    await ctx.send(embed=embed)

bot.add_command(ttt)

bot.add_command(lichess)

bot.add_command(chess)

bot.add_command(connect4)

@bot.command()
async def shop(ctx):
    embed = discord.Embed(title="Shop", description="List of items for purchase.", color=discord.Color.blue())
    embed.add_field(name="`$buy role_1k`", value="This item gives you a cosmetic role, and access to a private channel! $1000.00", inline=False)
    embed.add_field(name="`$buy role_10k`", value="This item gives you a cosmetic role, and access to a private channel! $10,000.00", inline=False)
    embed.add_field(name="`$buy role_100k`", value="This item gives you a cosmetic role, and access to a private channel! $100,000.00", inline=False)
    embed.add_field(name="`$buy role_1m`", value="This item gives you a cosmetic role, and access to a private channel! $1,000,000.00", inline=False)
    embed.add_field(name="`$buy role_1b`", value="This item gives you a cosmetic role, and access to a private channel! $1,000,000,000.00", inline=False)
    embed.add_field(name="`$buy role_1t`", value="This item gives you a cosmetic role, and access to a private channel! $1,000,000,000,000.00", inline=False)
    await ctx.send(embed=embed)

bot.add_command(buy)

bot.add_command(sell)

bot.add_command(leaderboard)

@bot.command()
async def ip(ctx):
    random_int_1 = random.randint(1, 255)
    random_int_2 = random.randint(1, 255)
    await ctx.send(f"Your IP is 192.168.{random_int_1}.{random_int_2}")

@bot.command()
async def roll(ctx, number=10):
    random_int = random.randint(1, number)
    await ctx.send(f"You rolled a {random_int}!")

@bot.command()
async def picture(ctx):
    headers = {
            "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
        }
    response = requests.get("https://api.unsplash.com/photos/random", headers=headers)
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']
        await ctx.send(image_url)
    else:
        await ctx.send('Sorry, I couldn\'t fetch an image right now.')

@bot.command()
async def ai(ctx, *, question: str):
    if ctx.author.guild_permissions.administrator:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        
        # Get the response text
        gpt_response = response['choices'][0]['message']['content']

        # Write some code that checks if the message is longer than 1k chars and if it is, split it into multiple messages
        if len(gpt_response) > 1000:
            await ctx.send('The message was too long so I sent it to your in your dms.')
            message_chunks = [gpt_response[i:i+1000] for i in range(0, len(gpt_response), 1000)]
            for chunk in message_chunks:
                if chunk.strip():  # Check if the message is not empty or only contains whitespace
                    await ctx.author.send(chunk)
        else:
            if gpt_response.strip():  # Check if the message is not empty or only contains whitespace
                await ctx.send(gpt_response)
    else:
        await ctx.send("Sorry this command is for admins only. I pay money to use ChatGPT, and I don't want a bunch of random people spending my money.")

@bot.command()
async def stockmarket(ctx, *stock_names):
    if not stock_names:
        stock_names = None  # Pass None to plot all stocks
    else:
        stock_names = list(stock_names)  # Convert tuple to list
    draw_graph(stock_names)
    await ctx.send(file=discord.File(STOCK_GRAPH_PIC))

bot.add_command(stock)

async def async_timer1():
    global RNG_stock_price, NVDA_stock_price, DOGE_stock_price, UP_stock_price, DOWN_stock_price, GAY_stock_price
    while True:
        # Wait for the specified duration
        await asyncio.sleep(60)
        RNG_stock_price = stock1()
        NVDA_stock_price = get_stock_price('NVDA')
        DOGE_stock_price = get_doge_price()
        UP_stock_price = generate_stock_price()
        DOWN_stock_price = DOWN()
        GAY_stock_price = get_gayness()

#damn brit
bot.run("MTIzMDk2MjI2OTc0ODQ2NTY2Ng.G99PQ1.04Ch0VvwZbQqS0ZnbPKMjjAra8t2dHv38M9BQ0")

#eli bot
#bot.run('MTE3NTg5MDY0NDE5MTk1NzAxMw.GZtdjv.4039BrLsym-_rBJd1OV8W7GdSVysVomGA9xHC4')