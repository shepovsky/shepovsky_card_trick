import os
import random

from trick_data import DECK_SIZE, GROUP_QTY, GROUP_SIZE
from shepovsky_playing_cards import Deck

def get_clever_shuffle_insert_positions(stacks=GROUP_QTY, stack_sizes=GROUP_SIZE):
    return random.sample(range(1,DECK_SIZE+1),DECK_SIZE)

def shuffle_clever():
    insert_positions = get_clever_shuffle_insert_positions()
    print(insert_positions)
    for position, card in sorted(zip(insert_positions, deck)): # sorts by insert_positions
        deck.insert_card(card, position)

os.system('cls')
deck = Deck(DECK_SIZE)
deck.shuffle()

print()
deck.deal_into_cols(GROUP_SIZE)
print()

shuffle_clever()
print()
deck.deal_into_cols(GROUP_SIZE)



