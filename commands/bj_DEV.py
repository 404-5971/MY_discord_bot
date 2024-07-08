from discord.ext import commands
import discord
import asyncio
import random
import time
from money_bals import *

import random

@commands.command()
async def bj(ctx, bet=None):
    if ctx.channel.id != 1259895236931620954:
        await ctx.send("This command can only be used in the <#1259895236931620954> channel.")
        return
    
    try:
        bet = int(bet)
    except:
        bet = None

    if bet == None or bet == 0 or type(bet) != int:
        await ctx.send("Please enter a valid intger bet.")
        return
    if bet < 0:
        await ctx.send("Please enter a positive bet.")
        return
    
    # Sender
    player = ctx.author
    #player_username = player.name
    player_id = str(player.id)

    # Load money balances
    player_money_balance = load_money_data()

    # Check if the sender has enough money
    if player_id not in player_money_balance or player_money_balance[player_id] < bet:
        await ctx.send("You don't have enough money to bet that amount.")
        return
    
    # Deduct the bet from the player's balance
    player_money_balance[player_id] -= bet

    # Save the new balance
    save_money_data(player_money_balance)

    # Run the game
    try:
        if deck:
            deck = split_and_shuffle_deck(deck)
    except:
        deck = shuffle_deck()
    await deal_hand(ctx, deck, bet)

# Main function
def main():
    #bet = int(input('Enter your bet: '))
    bet = 100
    deck = shuffle_deck()
    deck = split_and_shuffle_deck(deck)
    deal_hand(deck, bet)

# Function to shuffle the deck
def shuffle_deck():
    deck = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'] * 4 * 6
    random.shuffle(deck)
    return deck

# Function to split and shuffle the deck further
def split_and_shuffle_deck(deck):
    split_index = random.randint(146, 166)
    deck1 = deck[:split_index]
    deck2 = deck[split_index:]
    shuffled_deck = []

    while deck1 or deck2:
        if deck1:
            shuffled_deck.append(deck1.pop(0))
        if deck2:
            shuffled_deck.append(deck2.pop(0))

    return shuffled_deck

# Function to deal the initial hands
async def deal_hand(ctx, deck, bet):
    player_hand = [deck.pop(0), deck.pop(0)]
    dealer_hand = [deck.pop(0), deck.pop(0)]
    player_total = get_hand_value(player_hand)
    await ctx.send(f'\nDealer card: {dealer_hand[0]}\nPlayer hand: {player_hand}\nPlayer total: {player_total}')
    await player_turn(ctx, player_total, player_hand, dealer_hand, deck, bet)


async def player_turn(ctx, current_total, player_hand, dealer_hand, deck, bet, split_hands=None, FirstHand=True):
    if split_hands is None:
        split_hands = []      

    if current_total == 21 and FirstHand == True:
        await dealer_turn(ctx, bet, dealer_hand, deck, player_hand, FirstHand)
        return

    if current_total > 21:
        await ctx.send('Bust! You lose.')
        print(current_total)
        return
    
    if current_total == 21:
        await dealer_turn(ctx, bet, dealer_hand, deck, player_hand, False)
        return

    view = discord.ui.View()

    # Button 1
    button1 = discord.ui.Button(
        label='Stand',
        style=discord.ButtonStyle.red
    )
    async def button1_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await stand(ctx, player_hand, dealer_hand, deck, bet, split_hands)
    button1.callback = button1_callback

    # Button 2
    button2 = discord.ui.Button(
        label='Split',
        style=discord.ButtonStyle.secondary
    )
    async def button2_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await split(ctx, current_total, player_hand, dealer_hand, deck, bet, split_hands)
    button2.callback = button2_callback

    # Button 3
    button3 = discord.ui.Button(
        label='Double',
        style=discord.ButtonStyle.blurple
    )
    async def button3_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await double(ctx, current_total, player_hand, dealer_hand, deck, bet, split_hands)
    button3.callback = button3_callback

    # Button 4
    button4 = discord.ui.Button(
        label='Hit',
        style=discord.ButtonStyle.green
    )
    async def button4_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await hit(ctx, player_hand, dealer_hand, deck, bet, split_hands)
    button4.callback = button4_callback

    # Add buttons to the view
    view.add_item(button1)
    view.add_item(button3)
    view.add_item(button4)

    if len(player_hand) == 2 and get_card_value(player_hand[0]) == get_card_value(player_hand[1]):
        view.add_item(button2)
        await ctx.send(content='What would you like to do?', view=view)
    else:
        await ctx.send(content='What would you like to do?', view=view)

async def hit(ctx, player_hand, dealer_hand, deck, bet, split_hands):
    player_hand.append(deck.pop(0))
    current_total = get_hand_value(player_hand)
    await ctx.send(f'Player hand: {player_hand}\nPlayer total: {current_total}')
    await player_turn(ctx, current_total, player_hand, dealer_hand, deck, bet, split_hands, False)

async def stand(ctx, player_hand, dealer_hand, deck, bet, split_hands):
    if split_hands:
        next_hand = split_hands.pop(0)
        await player_turn(ctx, get_hand_value(next_hand), next_hand, dealer_hand, deck, bet, split_hands, False)
    else:
        await dealer_turn(ctx, bet, dealer_hand, deck, player_hand, False)

async def double(ctx, current_total, player_hand, dealer_hand, deck, bet, split_hands):
    #check if the user has enough money to double
    player = ctx.author
    player_id = str(player.id) 
    player_money_balance = load_money_data()
    if bet * 2 > player_money_balance[player_id]:
        await ctx.send("You don't have enough money to double.")
        return
    bet += bet
    player_hand.append(deck.pop(0))
    current_total = get_hand_value(player_hand)
    await ctx.send(f'Player hand: {player_hand}\nPlayer total: {current_total}')
    await dealer_turn(ctx, bet, dealer_hand, deck, player_hand, False)

async def split(ctx, current_total, player_hand, dealer_hand, deck, bet, split_hands):
    if len(player_hand) == 2 and get_card_value(player_hand[0]) == get_card_value(player_hand[1]):
            hand1 = [player_hand[0]]
            hand2 = [player_hand[1]]
            split_hands = [hand2]
            await ctx.send(f'First hand: {hand1}')
            await player_turn(ctx, get_hand_value(hand1), hand1, dealer_hand, deck, bet, split_hands, False)
    else:
        await ctx.send('You cannot split this hand.')
        await player_turn(ctx, current_total, player_hand, dealer_hand, deck, bet, split_hands, False)
#    else:
#        await ctx.send('You cannot split this hand.')
#        print('Invalid input')
#        player_turn(ctx, current_total, player_hand, dealer_hand, deck, bet, split_hands, False)


async def dealer_turn(ctx, bet, dealer_hand, deck, player_hand, FirstHand):
    dealer_total = get_hand_value(dealer_hand)
    while dealer_total < 17:
        dealer_hand.append(deck.pop(0))
        dealer_total = 0
        dealer_total = get_hand_value(dealer_hand)
    await ctx.send(f'\nDealer hand: {dealer_hand}\nDealer total: {dealer_total}')
    await check_win_lose(ctx, bet, dealer_hand, player_hand, FirstHand)

# Function to get the card value
def get_hand_value(hand, current_total=0):
    for card in hand:            
        if card == 'Ace':
            # Determine the value of the Ace based on the current total
            if current_total + 11 <= 21:
                current_total += 11
            else:
                current_total += 1
        elif card in ['Jack', 'Queen', 'King']:
            current_total += 10
        else:
            current_total += int(card)
    if current_total > 21:
        for card in hand:
            if card == 'Ace':
                current_total -= 10
                if current_total <= 21:
                    break
    return current_total

def get_card_value(card, current_total=0):
    if card == 'Ace':
        # Determine the value of the Ace based on the current total
        if current_total + 11 <= 21:
            return 11
        else:
            return 1
    elif card in ['Jack', 'Queen', 'King']:
        return 10
    else:
        return int(card)

# Function to check win/lose conditions
async def check_win_lose(ctx, bet, dealer_hand, player_hand, FirstHand):
    player = ctx.author
    player_id = str(player.id)
    player_money_balance = load_money_data()

    dealer_sum = get_hand_value(dealer_hand)
    player_sum = get_hand_value(player_hand)
    if player_sum > 21:
        await ctx.send('Bust! You lose.')
    elif dealer_sum > 21:
        await ctx.send('Dealer bust! You win!')
        player_money_balance[player_id] += bet * 2
    elif player_sum > dealer_sum:
        if FirstHand == True:
            await ctx.send('Blackjack! You win!')
            player_money_balance[player_id] += bet * 2.5
        await ctx.send('You win!')
        player_money_balance[player_id] += bet * 2
    elif player_sum < dealer_sum:
        await ctx.send('Dealer wins!')
    else:
        await ctx.send('Push!')
        player_money_balance[player_id] += bet
    save_money_data(player_money_balance)

# Run the game
if  __name__ == "__main__":
    main()