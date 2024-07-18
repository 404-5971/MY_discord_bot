from discord.ext import commands
import discord
import random
import json
import os

from money_bals import *
from const import ROOT_DIR

DEALER_ID = "1175890644191957013"

hand_totals = []

'''def check_and_create_json(file_path='bj.json', player_id=None):
    if not os.path.exists(file_path):
        initial_data = {}
        with open(file_path, 'w') as json_file:
            json.dump(initial_data, json_file, indent=4)
        print(f"{file_path} created with initial data.")
    else:
        print(f"{file_path} already exists.")

    # Load existing data from the JSON file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    # Check if the player ID is in the data
    if player_id not in data:
        data[player_id] = {'num_loses_in_a_row': 0, 'net_worth': 0}

        # Save the updated data back to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Added player ID {player_id} with a default value of 0.")
    else:
        print(f"Player ID {player_id} already exists in the JSON file.")

def update_bj_json(player_id, bet, opperator):
    with open(ROOT_DIR + '/bj.json', 'r') as json_file:
        data = json.load(json_file)
        if player_id in data:
            if opperator == '+':
                if data[player_id]['net_worth'] >= 0:
                    data[player_id]['net_worth'] += bet
                else:
                    data[player_id]['net_worth'] = 0
                data[player_id]['num_loses_in_a_row'] = 0
            elif opperator == '-':
                data[player_id]['net_worth'] -= bet
                data[player_id]['num_loses_in_a_row'] += 1
            with open(ROOT_DIR + '/bj.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)'''

@commands.command()
async def bj(ctx, bet=None):
    # Sender
    player = ctx.author
    #player_username = player.name
    player_id = str(player.id)

    # Load money balances
    player_money_balance = load_money_data()

    #check_and_create_json(ROOT_DIR + '/bj.json', player_id)
    
    try:
        bet = int(bet)
    except:
        bet = None

    if bet == None or bet == 0 or type(bet) != int:
        await player.send("Please enter a valid intger bet.")
        return
    if bet < 0:
        await player.send("Please enter a positive bet.")
        return
    

    # Check if the sender has enough money
    if player_id not in player_money_balance or player_money_balance[player_id] < bet:
        await player.send("You don't have enough money to bet that amount.")
        return
    
    # Deduct the bet from the player's balance
    player_money_balance[player_id] -= bet

    #add to the dealers balance
    player_money_balance[DEALER_ID] += bet

    # Save the new balance
    save_money_data(player_money_balance)

    #update_bj_json(player_id, bet, '-')  

    # Run the game
    try:
        if deck:
            deck = cut_and_shuffle_deck(deck)
    except:
        deck = shuffle_deck()
    await deal_hand(ctx, deck, bet)

# Function to split and shuffle the deck further
def cut_and_shuffle_deck(deck):
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

# Function to shuffle the deck
def shuffle_deck():
    deck = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King'] * 4 * 6
    random.shuffle(deck)
    return deck

# Function to deal the initial hands
async def deal_hand(ctx, deck, bet):
    global hand_totals
    hand_totals = []
    player_hands = [[deck.pop(0)]]
    dealer_hand = [deck.pop(0)]
    player_hands[0].append(deck.pop(0))
    dealer_hand.append(deck.pop(0))
    #player_hands = [['Queen', 'Jack']]
    
    #player_hands = [['9', '3', 'Ace', '10', 'Ace', '7']]
    
    #player_hands = [['Queen', 'Jack', '4']]
    #dealer_hand = ['Jack', 'Jack', '9']

    #player_hands = [['Jack', 'Ace']]

    #player_hands = [['Ace', 'Ace']]
    
    #player_hands = [['Jack', 'Jack', 'Jack']]
    await player_turn(ctx, player_hands, dealer_hand, deck, bet)

async def player_turn(ctx, player_hands, dealer_hand, deck, bet, FirstHand=True):
    global hand_totals
    player = ctx.author

    player_total = get_hand_value(player_hands[0])

    await player.send(f'\nDealer card: {dealer_hand[0]}\nPlayer hand: {player_hands[0]}\nPlayer total: {player_total}')

    if player_total == 21:
        await stand(ctx, player_hands, dealer_hand, deck, bet, FirstHand)
        return

    elif player_total > 21:
        await stand(ctx, player_hands, dealer_hand, deck, bet, FirstHand=False)
        return

    #calling this function does the same thing as all the code up there no?

    #turns out it doesn't. So I'm just going to stick with the code up there

    #check_win_lose(ctx, bet, dealer_hand, FirstHand)

    view = discord.ui.View()

    # Button 1
    button1 = discord.ui.Button(
        label='Stand',
        style=discord.ButtonStyle.red
    )
    async def button1_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await stand(ctx, player_hands, dealer_hand, deck, bet, FirstHand=False)
    button1.callback = button1_callback

    # Button 2
    button2 = discord.ui.Button(
        label='Split',
        style=discord.ButtonStyle.secondary
    )
    async def button2_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await split(ctx, player_hands, dealer_hand, deck, bet)
    button2.callback = button2_callback

    # Button 3
    button3 = discord.ui.Button(
        label='Double',
        style=discord.ButtonStyle.blurple
    )
    async def button3_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await double(ctx, player_hands, dealer_hand, deck, bet)
    button3.callback = button3_callback

    # Button 4
    button4 = discord.ui.Button(
        label='Hit',
        style=discord.ButtonStyle.green
    )
    async def button4_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await hit(ctx, player_hands, dealer_hand, deck, bet)
    button4.callback = button4_callback

    # Add buttons to the view
    view.add_item(button1)
    view.add_item(button3)
    view.add_item(button4)

    if len(player_hands[0]) == 2 and get_card_value(player_hands[0][0]) == get_card_value(player_hands[0][1]):
        view.add_item(button2)
        await player.send(content='What would you like to do?', view=view)
    else:
        await player.send(content='What would you like to do?', view=view)

async def hit(ctx, player_hands, dealer_hand, deck, bet):
    player_hands[0].append(deck.pop(0))
    await player_turn(ctx, player_hands, dealer_hand, deck, bet, False)

async def stand(ctx, player_hands, dealer_hand, deck, bet, FirstHand):
    global hand_totals

    # Get the current hand total
    hand_total = get_hand_value(player_hands[0])
    
    # Append the current hand total to hand_totals
    hand_totals.append(hand_total)
    
    # Remove the hand that the player has stood on
    player_hands.pop(0)
    
    # If there are more hands to be played

    if player_hands:
        print('More hands to be played')
        await player_turn(ctx, player_hands, dealer_hand, deck, bet, False)
    else:
        await dealer_turn(ctx, bet, dealer_hand, deck, FirstHand)


async def double(ctx, player_hands, dealer_hand, deck, bet):
    #check if the user has enough money to double
    player = ctx.author
    player_id = str(player.id) 
    player_money_balance = load_money_data()
    if bet * 2 > player_money_balance[player_id]:
        await player.send("You don't have enough money to double.")
        return
    bet += bet
    player_hands[0].append(deck.pop(0))
    await dealer_turn(ctx, bet, dealer_hand, deck, False)

async def split(ctx, player_hands, dealer_hand, deck, bet):
    player = ctx.author
    player_id = str(player.id)
    player_money_balance = load_money_data()

    if bet * 2 > player_money_balance[player_id]:
        await player.send("You don't have enough money to split.")
        return
    if get_card_value(player_hands[0][0]) != get_card_value(player_hands[0][1]):
        await player.send("You can only split if you have two cards of the same value.")
        return

    player_hands.append([player_hands[0][1]])
    player_hands[0].pop(1)

    await player_turn(ctx, player_hands, dealer_hand, deck, bet, False)

async def dealer_turn(ctx, bet, dealer_hand, deck, FirstHand):
    player = ctx.author

    dealer_total = get_hand_value(dealer_hand)
    while dealer_total < 17:
        dealer_hand.append(deck.pop(0))
        dealer_total = get_hand_value(dealer_hand)
    await player.send(f'\nDealer hand: {dealer_hand}\nDealer total: {dealer_total}')
    await check_win_lose(ctx, bet, dealer_hand, FirstHand)

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
async def check_win_lose(ctx, bet, dealer_hand, FirstHand):
    global hand_totals
    player = ctx.author
    player_id = str(player.id)
    player_money_balance = load_money_data()

    dealer_sum = get_hand_value(dealer_hand)

    #check_and_create_json(ROOT_DIR + '/bj.json', player_id)

    net_change = 0

    print(f'\n{hand_totals}\n')

    for total in hand_totals:
        player_sum = total

        if player_sum > 21:
            await player.send('Bust! You lose.')
            net_change -= bet

        elif dealer_sum > 21:
            await player.send('Dealer bust! You win!')
            player_money_balance[player_id] += bet * 2
            player_money_balance[DEALER_ID] -= bet
            net_change += bet
            #update_bj_json(player_id, bet * 2, '+')

        elif player_sum > dealer_sum:
            if FirstHand == True:
                await player.send('Blackjack! You win!')
                player_money_balance[player_id] += bet * 2.5
                player_money_balance[DEALER_ID] -= bet * 1.5
                net_change += bet * 1.5
                #update_bj_json(player_id, bet * 2.5, '+')

            else:
                await player.send('You win!')
                player_money_balance[player_id] += bet * 2
                player_money_balance[DEALER_ID] -= bet
                net_change += bet
                #update_bj_json(player_id, bet * 2, '+')

        elif player_sum < dealer_sum:
            await player.send('Dealer wins!')
            net_change -= bet

        else:
            await player.send('Push!')
            player_money_balance[player_id] += bet
            player_money_balance[DEALER_ID] -= bet
            #update_bj_json(player_id, bet, '+')

    if net_change > 0:
        await player.send(f'```diff\n+ Net change: +${int(net_change)}\n```')
    elif net_change < 0:
        #what is abs?
        #abs is a function that returns the absolute value.
        await player.send(f'```diff\n- Net change: -${abs(net_change)}\n```')
    else:
        await player.send('```Net change: $0```')
    '''
    with open(ROOT_DIR + '/bj.json', 'r') as json_file:
        data = json.load(json_file)

    if data[player_id]['num_loses_in_a_row'] >= 5 and net_change < 0:
        amount = abs(data[player_id]['net_worth']) * 0.45
        update_bj_json(player_id, amount, '+')
        print(f'\n{amount}\n')
        player_money_balance[player_id] += amount
        player_money_balance[DEALER_ID] -= amount'''

    save_money_data(player_money_balance)
    return