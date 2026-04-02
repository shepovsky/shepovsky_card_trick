import os
import random
import sys

from trick_data import DECK_SIZE, GROUP_QTY, GROUP_SIZE
from shepovsky_playing_cards import Deck
from shepovsky_playing_cards import split_cards_into_stacks

def shuffle_at_step_1():
    deck_original.shuffle()

def shuffle_at_step_2():
    # determine how to split cards in each row into stacks equally. determine the stack sizes
    stacks = split_cards_into_stacks(GROUP_SIZE, GROUP_QTY)
    # in case the stacks are not equal (as in case with 13 cards being split into 4 groups as [4, 3, 3, 3], shuffle them randomly
    random.shuffle(stacks)

    # split each row of cards into stacks
    for c in range(GROUP_QTY):
        placeholders = list(range(GROUP_SIZE * c + 1, GROUP_SIZE * (c + 1) + 1))
        random.shuffle(placeholders)
        it = iter(placeholders)
        placeholders = [list(next(it) for _ in range(stack)) for stack in stacks]
        card_positions.append(placeholders)
        stacks.append(stacks.pop(0))

    for row in card_positions:
        for index, col in enumerate(row):
            if len(col) < GROUP_QTY:
                col.insert(index, None)
    print(card_positions)

    # rearrange the card positions so that each group of cards from each row move into its own row. remove Nones. do this in two steps:
    # 1) flatten column-wise
    card_positions_new = [
        [card_position for stack in stacks for card_position in stack if card_position is not None]
        for stacks in zip(*card_positions)
    ]

    # 2) shuffle each new row of card placeholders in-place
    for row in card_positions_new:
        random.shuffle(row)

    card_positions_new = [card_position for row in card_positions_new for card_position in row]
    shuffle_clever(card_positions_new, deck_magic)

    return card_positions

def shuffle_at_step_3():
    print(f"card positions [m]: {card_positions}")
    # rearrange the card positions so that each row contains positions relevant to the order of the position in each stack. remove Nones. do this in two steps:
    # 1) flatten
    card_positions_new = []
    for index in range(GROUP_QTY):
        row_new = []
        for r in range(len(card_positions)):
            for c in range(len(card_positions[0])):
                row_new.append(card_positions[r][c][index])
        card_positions_new.append([x for x in row_new if x is not None]) # removes None values

    # 2) shuffle each new row of card placeholders in-place
    for row in card_positions_new:
        random.shuffle(row)

    card_positions_new = [card_position for row in card_positions_new for card_position in row]
    print(card_positions_new)
    shuffle_clever(card_positions_new, deck_double)

def shuffle_clever(insert_positions, deck):
    if len(deck) != len (insert_positions):
        raise ValueError("Number of insert positions does not match the number of cards in the deck.")
    for position, card in sorted(zip(insert_positions, deck)): # sorts by insert_positions
        deck.insert_card(card, position)

def bye():
    os.system('cls')
    print('Bye!')
    sys.exit()

def request_which_row():
    return request_which('row')

def request_which_col():
    return request_which('column')

def request_which(part: str, qty = GROUP_QTY):
    while True:
        part_number = input(f"\nWhat {part} is it in? (1-{qty} or 'q' to quit): ")

        if part_number.lower().strip() == 'q':
            bye()

        try:
            part_number = int(part_number)
            if part_number in range(1, GROUP_QTY + 1):
                return part_number
            else:
                raise ValueError
        except ValueError:
            print(f"Invalid input! Please enter a number between 1 and {qty}, or 'q' to quit.")

os.system('cls')
print("\nStep 1 of 3:")
input("Think of a card and press Enter")

os.system('cls')
print("\nStep 1 of 3:")
print("Find your card below:\n")

deck_original = Deck(DECK_SIZE)
shuffle_at_step_1()
deck_original.deal_into_cols(GROUP_SIZE)
r1 = request_which_row()


os.system('cls')
print("\nStep 2 of 3:")
print("Find your card below:\n")

deck_magic = Deck(deck_original)
card_positions = []
shuffle_at_step_2()
deck_magic.deal_into_cols(GROUP_SIZE)
r2 = request_which_row()

print(card_positions[r2 - 1][r1 - 1])
for i in card_positions[r2 - 1][r1 - 1]:
    if i:
        print(f'{i}: {deck_magic[i-1]}')


os.system('cls')
print("\nStep 3 of 3:")
print("For the last time find your card below:\n")
deck_double = Deck(deck_original)
shuffle_at_step_3()
deck_double.deal_into_cols(GROUP_SIZE)

#
# r3 = request_which_row()
#
# print(deck_magic[card_positions[r2 - 1][r1 - 1][r3 - 1]])


