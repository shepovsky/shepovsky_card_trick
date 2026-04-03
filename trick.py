import os
import random
import sys

from trick_data import DECK_SIZE, GROUP_QTY, GROUP_SIZE
from shepovsky_playing_cards import Player
from shepovsky_playing_cards import Deck
from shepovsky_playing_cards import get_split_deck_into_stack_random_sizes

def shuffle_at_step_1():
    deck_magic = []
    for r in magic_deck:
        row_of_cards = []
        for c in r:
            row_of_cards += c
        random.shuffle(row_of_cards)
        deck_magic += [x for x in row_of_cards if x is not None]

    update_deck_original(deck_magic)

def shuffle_at_step_2():
    deck_magic = []

    for c in range(len(magic_deck[0])):
        row_new = []
        for r in range(len(magic_deck)):
            row_new += magic_deck[r][c]
        random.shuffle(row_new)
        deck_magic += [x for x in row_new if x is not None]

    update_deck_original(deck_magic)

def shuffle_at_step_3():
    deck_magic = []

    for n in range(GROUP_QTY):
        row_new = []
        for c in range(len(magic_deck[0])):
            for r in range(len(magic_deck)):
                row_new.append(magic_deck[r][c][n])
        random.shuffle(row_new)
        deck_magic += [x for x in row_new if x is not None]

    update_deck_original(deck_magic)

def update_deck_original(deck_newly_ordered):
    random.shuffle(row_shuffler)
    deck_original.cards_reorder(deck_newly_ordered)
    deck_original.cards_sorter([r for r in row_shuffler for _ in range(GROUP_SIZE)])

def create_magic_deck():
    result = []

    # split the cards fron Deck Original into rows and columns using Magic Deck instance:
    for r in range(GROUP_QTY):

        row_of_cards = deck_original[GROUP_SIZE * r:GROUP_SIZE * (r + 1)]
        random.shuffle(row_of_cards)
        # split each row of cards into stacks
        row_of_cards = split_cards_into_stacks(row_of_cards, stacks)
        # when stacks have unequal sizes, make them equal by adding None values in specific places
        for index, col in enumerate(row_of_cards):
            if len(col) < GROUP_QTY:
                for i in range(GROUP_QTY - len(col)):
                    if len(col) < index:
                        col.insert(0, None)
                    else:
                        col.insert(index, None)
        # switch stack sizes for the next row in case the stack sizes are not equal
        stacks.append(stacks.pop(0))
        # append new Magic row of cards to the Magic Deck
        result.append(row_of_cards)

    return result

def split_cards_into_stacks(cards, stack_sizes):
    result = []
    i = 0
    for size in stack_sizes:
        result.append(cards[i:i+size])
        i += size
    return result

def bye():
    print('\nBye!')
    sys.exit()

def request_which_row():
    return request_which('row')

def request_which_col():
    return request_which('column')

def request_which(part: str, qty = GROUP_QTY):
    while True:
        part_number = input(f"\nWhat {part} is it in? (1–{qty}, 'r' to reshuffle, 'q' to quit): ")

        if part_number.lower().strip() == 'q':
            bye()

        if part_number.lower().strip() == 'r':
            return 'r'

        try:
            part_number = int(part_number)
            if part_number in range(1, GROUP_QTY + 1):
                return part_number
            else:
                raise ValueError
        except ValueError:
            print(f"Unexpected input! Please check and try again")

# initiate variables for user responses
r1 = r2 = r3 = 'r'

# Step 1:
os.system('cls')
print("\nStep 1 of 3:")
input("Think of a card and press Enter")
# create a new deck of cards and shuffle it
deck_original = Deck(DECK_SIZE)
deck_original.shuffle()
# determine how to split cards in each row into stacks equally. determine the stack sizes
stacks = get_split_deck_into_stack_random_sizes(GROUP_SIZE, GROUP_QTY, GROUP_QTY)
# create a list responsible for random shuffle of rows of cards while keeping the same cards in each row
row_shuffler = list(range(GROUP_QTY))
# create the Magic Deck list which becomes the master list for guessing the cards
magic_deck = create_magic_deck()

while r1 == 'r':
    os.system('cls')
    print("\nStep 1 of 3:")
    print("Find your card below:\n")

    shuffle_at_step_1()
    deck_original.deal_into_cols(GROUP_SIZE)
    r1 = request_which_row()

r1 = row_shuffler.index(r1 - 1)

# Step 2:
os.system('cls')
print("\nStep 2 of 3:")
input("Thank you! Press Enter to shuffle the deck\n")

while r2 == 'r':
    os.system('cls')
    print("\nStep 2 of 3:")
    print("Once again, please, find your card below:\n")

    # populate the Magic Deck with cards from the Original Deck and shuffle them cleverly
    shuffle_at_step_2()
    deck_original.deal_into_cols(GROUP_SIZE)
    r2 = request_which_row()

r2 = row_shuffler.index(r2 - 1)

# Step 3:
if len([card for card in magic_deck[r1][r2] if card is not None]) > 1:

    os.system('cls')
    print("\nStep 3 of 3:")
    input("Great! Thank you. Press Enter to shuffle the deck for the final time\n")

    while r3 == 'r':
        os.system('cls')
        print("\nStep 3 of 3:")
        print("For the last time find your card below:\n")
        shuffle_at_step_3()
        deck_original.deal_into_cols(GROUP_SIZE)

        r3 = request_which_row()

    r3 = row_shuffler.index(r3 - 1)
    the_card = magic_deck[r1][r2][r3]

else:
    the_card = magic_deck[r1][r2]

# Finale
if the_card:
    os.system('cls')
    print("\nThe Grand Reveal:")
    input("I know your card! Press Enter to reveal")
    os.system('cls')
    print("\nThe Grand Reveal:")
    print(f"You card is:")
    the_card.print_pretty()
else:
    os.system('cls')
    print("\nYou either trying to be cheeky or you may not have been concentrating on your card well enough. :(")
    print("In any case, something has gone wrong, I am afraid. Try again.")

bye()

