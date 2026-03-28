import os
import random

from trick_data import DECK_SIZE, GROUP_QTY, GROUP_SIZE
from shepovsky_playing_cards import Deck

def split_cards_into_stacks(card_qty, stack_qty):
    base = card_qty // stack_qty          # floor
    remainder = card_qty % stack_qty      # how many need +1
    return [base + 1] * remainder + [base] * (stack_qty - remainder)

def get_inserts(qty):
    stacks = list(range(GROUP_QTY))
    random.shuffle(stacks)
    inserts_qty = split_cards_into_stacks(qty, GROUP_QTY)
    insert_positions = []
    for stack, insert_qty in zip(stacks, inserts_qty):
        insert_positions = insert_positions + list(random.sample(range(1 + GROUP_SIZE * stack, 1 + GROUP_SIZE * (stack + 1)), insert_qty))
    insert_positions.sort()
    return insert_positions

def clever_shuffle(list_of_cards):
    random.shuffle(list_of_cards)
    insert_positions = get_inserts(len(list_of_cards))
    for position, card in sorted(zip(insert_positions, list_of_cards)): # sorts by insert_positions
        deck.insert_card(card, position)

os.system('cls')
input("Think of a card. Remember it and press Enter.")
deck = Deck(DECK_SIZE)
deck.shuffle()

r = 0
while not r in [1,2,3,4]:
    os.system('cls')
    print("Find your card below, remember it's position and press Enter:\n")
    deck.deal_into_rows(GROUP_QTY)
    input()
    os.system('cls')
    r = input("Enter the number of the row where you saw your card (1-4 or 0 to reshuffle or 'q' to quit) : ")
    if r.lower() == 'q':
        break
    r = int(r)

cards_picked_once = deck[GROUP_SIZE * (r - 1):GROUP_SIZE * r]
clever_shuffle(cards_picked_once)

os.system('cls')
print("Good. Thank you")
input("Let's shuffle the deck and you try finding your card again. Press Enter")
r = 0
while not r in [1,2,3,4]:
    os.system('cls')
    print("Find your card below, remember it's position and press Enter:\n")
    deck.deal_into_rows(GROUP_QTY)
    input()
    os.system('cls')
    r = input("Enter the number of the row where you saw your card (1-4 or 0 to reshuffle or 'q' to quit) : ")
    if r.lower() == 'q':
        break
    r = int(r)

cards_picked_twice = list(set(cards_picked_once) & set(deck[GROUP_SIZE * (r - 1):GROUP_SIZE * r]))
clever_shuffle(cards_picked_twice)

os.system('cls')
print("Thank you")
input("Let's shuffle the deck one last time and see if you can find it this time. Press Enter")
r = 0
while not r in [1,2,3,4]:
    os.system('cls')
    print("Find your card below, remember it's position and press Enter:\n")
    deck.deal_into_rows(GROUP_QTY)
    input()
    os.system('cls')
    r = input("Enter the number of the row where you saw your card (1-4 or 0 to reshuffle or 'q' to quit) : ")
    if r.lower() == 'q':
        break
    r = int(r)

the_card = list(set(cards_picked_twice) & set(deck[GROUP_SIZE * (r - 1):GROUP_SIZE * r]))
if len(the_card) == 1:
    input("I think I know your card. Press Enter")
    print("Your card is:")
    print(the_card[0])
else:
    print("Stop trying to be cheeky.")
