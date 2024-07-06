import random

bet = 100

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
def deal_hand(deck):
    player_hand = [deck.pop(0), deck.pop(0)]
    dealer_hand = [deck.pop(0), deck.pop(0)]
    print(f'\nDealer card: {dealer_hand[0]}')
    print(f'Player hand: {player_hand}')
    player_total = sum(get_card_value(card) for card in player_hand)
    print(f'Player total: {player_total}')
    player_turn(player_total, player_hand, dealer_hand, deck)

# Function to get the card value
def get_card_value(card, current_total=0):
    if card == 'Ace':
        # Determine the value of the Ace based on the current total
        return 1 if current_total + 11 > 21 else 11
    elif card in ['Jack', 'Queen', 'King']:
        return 10
    else:
        return int(card)
# Function to check win/lose conditions
def check_win_lose(dealer_hand, player_hand):
    dealer_sum = sum(get_card_value(card) for card in dealer_hand)
    player_sum = sum(get_card_value(card) for card in player_hand)
    if player_sum > 21:
        print('Bust! You lose.')
    elif dealer_sum > 21 or player_sum > dealer_sum:
        print('You win!')
    elif player_sum < dealer_sum:
        print('Dealer wins!')
    else:
        print('Push!')

# Player's turn function
def player_turn(current_total, player_hand, dealer_hand, deck):
    if current_total == 21:
        print('Blackjack! You win!')
        return
    elif current_total > 21:
        print('Bust! You lose.')
        return
    
    if player_hand[0] == player_hand[1]:
        action = input('Hit, Stand, Double, or Split: ').lower()
    else:
        action = input('Hit, Stand, or Double: ').lower()

    if action == 'hit':
        player_hand.append(deck.pop(0))
        current_total = sum(get_card_value(card) for card in player_hand)
        print(f'Player hand: {player_hand}')
        print(f'Player total: {current_total}')
        player_turn(current_total, player_hand, dealer_hand, deck)
    elif action == 'stand':
        dealer_turn(dealer_hand, deck, player_hand)
    elif action == 'double':
        # Double the bet and deal one more card
        player_hand.append(deck.pop(0))
        current_total = sum(get_card_value(card) for card in player_hand)
        print(f'Player hand: {player_hand}')
        print(f'Player total: {current_total}')
        if current_total <= 21:
            dealer_turn(dealer_hand, deck, player_hand)
        else:
            print('Bust! You lose.')
    elif action == 'split':
        # Handle the split scenario
        pass
    else:
        print('Invalid input')
        player_turn(current_total, player_hand, dealer_hand, deck)

# Dealer's turn function
def dealer_turn(dealer_hand, deck, player_hand):
    dealer_total = sum(get_card_value(card) for card in dealer_hand)
    while dealer_total < 17:
        dealer_hand.append(deck.pop(0))
        dealer_total = sum(get_card_value(card) for card in dealer_hand)
    print(f'Dealer hand: {dealer_hand}')
    print(f'Dealer total: {dealer_total}')
    check_win_lose(dealer_hand, player_hand)

# Main function
def main():
    deck = shuffle_deck()
    deck = split_and_shuffle_deck(deck)
    deal_hand(deck)

# Run the game
main()


#type stuff asjflksajflsdjflksdjfklsdj f