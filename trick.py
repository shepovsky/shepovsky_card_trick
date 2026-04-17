import hashlib
import os
import random
import sys

from trick_data import DECK_SIZE, GROUP_QTY, GROUP_SIZE
from shepovsky_playing_cards import Deck
from shepovsky_playing_cards import Player
from shepovsky_playing_cards import Table
from shepovsky_playing_cards import get_split_deck_into_stack_random_sizes


class TrickParticipant(Player):

    def __init__(self, name):
        email = self._generate_dummy_email(name)
        super().__init__(email=email, name=name)
        self._responses = {}
        self._the_card = None

    @property
    def the_card(self):
        return self._the_card

    def set_response(self, step_no: int, response: int):
        self._responses[f"r{step_no}"] = response

    def determine_the_card(self, deck):

        indices = [self._responses[k] for k in ('r1', 'r2', 'r3') if k in self._responses]
        the_card = deck
        for i in indices:
            the_card = the_card[i]

        if isinstance(the_card, list):
            the_card = [card for card in the_card if card is not None]
            if len(the_card) == 1:
                self._the_card = the_card[0]
                return the_card[0]
            else:
                return None
        else:
            self._the_card = the_card
            return the_card

    @staticmethod
    def _generate_dummy_email(name):
        """Generates a dummy email by hashing the participant name"""
        name_cleaned = name.strip().lower()
        local_part = hashlib.md5(name_cleaned.encode()).hexdigest()
        return f"{local_part}@trick.local"


def create_magic_deck(deck: Deck):
    result = []
    deck.shuffle()

    # determine how to split cards in each row into stacks equally. determine the stack sizes
    stacks = get_split_deck_into_stack_random_sizes(GROUP_SIZE, GROUP_QTY, GROUP_QTY)

    # split the cards fron Deck Original into rows and columns using Magic Deck instance:
    for r in range(GROUP_QTY):

        row_of_cards = deck[GROUP_SIZE * r:GROUP_SIZE * (r + 1)]
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


def shuffle_at_step_1(deck_original, magic_deck, row_shuffler):
    magic_deck_child = []

    for r in magic_deck:
        row_of_cards = []
        for c in r:
            row_of_cards += c
        random.shuffle(row_of_cards)
        magic_deck_child += [x for x in row_of_cards if x is not None]

    return update_deck_original(deck_original, magic_deck_child, row_shuffler)


def shuffle_at_step_2(deck_original, magic_deck, row_shuffler):
    magic_deck_child = []

    for c in range(len(magic_deck[0])):
        row_new = []
        for r in range(len(magic_deck)):
            row_new += magic_deck[r][c]
        random.shuffle(row_new)
        magic_deck_child += [x for x in row_new if x is not None]

    return update_deck_original(deck_original, magic_deck_child, row_shuffler)


def shuffle_at_step_3(deck_original, magic_deck, row_shuffler):
    magic_deck_child = []

    for n in range(GROUP_QTY):
        row_new = []
        for c in range(len(magic_deck[0])):
            for r in range(len(magic_deck)):
                row_new.append(magic_deck[r][c][n])
        random.shuffle(row_new)
        magic_deck_child += [x for x in row_new if x is not None]

    return update_deck_original(deck_original, magic_deck_child, row_shuffler)


def update_deck_original(deck_original, magic_deck_child, row_shuffler):
    random.shuffle(row_shuffler)
    deck_original.cards_reorder(magic_deck_child)
    deck_original.cards_sorter([r for r in row_shuffler for _ in range(GROUP_SIZE)])
    return deck_original

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

    prompt: str = f"what {part} is your card in? (1–{qty}, 'r' to reshuffle, 'q' to quit): "

    while True:
        part_number = input(prompt)

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
            prompt = prompt[:1].upper() + prompt[1:]


def finale(current_participant: TrickParticipant):
    if current_participant.the_card:
        os.system('cls')
        print("\nThe Grand Reveal:")
        print(f"\nI know your card, {current_participant.name}!")
        input("Press Enter to reveal.")
        os.system('cls')
        print("\nThe Grand Reveal:")
        print(f"\n{current_participant.name}, you card is:")
        current_participant.the_card.print_pretty()
    else:
        os.system('cls')
        print("\nDear, {current_participant.name}!")
        print("You either trying to be cheeky or you may not have been concentrating on your card well enough. :(")
        print("In any case, something has gone wrong, I am afraid. Try again.")
    input()


def main():

    # get participants to a table
    table = Table(DECK_SIZE)
    while True:
        os.system('cls')
        participant_num = table.players_qty + 1
        print(f'\nParticipant {participant_num}, what is your name?')
        print('(Leave blank and press Enter if there are no {}participants)'.format(
            '' if participant_num == 1 else 'more '
        ))
        participant_name = input(': ')
        if participant_name:
            player = TrickParticipant(participant_name)
            try:
                table.sign_in_player(player)
            except ValueError:
                print(f"There is already a participant with name '{participant_name}'. Could you pick a different name please?")
        else:
            break

    # intro
    os.system('cls')
    if table.players_qty == 0:
        bye()
    elif table.players_qty == 1:
        print(f'Hello, {table.first_player}')
        input("Think of a card, do not tell anyone, and press Enter")
    else:
        print('Dear participants!')
        input("Each of you, think of your own card (don’t tell anyone), then press Enter.")

    # get a deck of cards and shuffle it
    deck_original = table.deck
    # create a list responsible for random shuffle of rows of cards while keeping the same cards in each row
    row_shuffler = list(range(GROUP_QTY))
    # create the Magic Deck list which becomes the master list for guessing the cards
    magic_deck = create_magic_deck(deck_original)
    steps = 3

    # Steps 1-3:
    for step in range(steps):
        participant_response = 'r'
        for participant in table.players:

            while True:
                os.system('cls')
                print(f"\nStep {step + 1} of {steps}:")

                if step == 0:
                    print("Now, find your card below:")
                elif step == 1:
                    print("One more time, please, find your card below:\n")
                elif step == 2:
                    print("Great! Please find your card one last time:\n")
                else:
                    raise ValueError(f"Unexpected step value: {step}")

                if participant_response == 'r':
                    if step == 0:
                        deck_original = shuffle_at_step_1(deck_original, magic_deck, row_shuffler)
                    elif step == 1:
                        deck_original = shuffle_at_step_2(deck_original, magic_deck, row_shuffler)
                    elif step == 2:
                        deck_original = shuffle_at_step_3(deck_original, magic_deck, row_shuffler)
                    else:
                        raise ValueError(f"Unexpected step value: {step}")

                deck_original.deal_into_cols(GROUP_SIZE)
                print(f"\n{participant.name},", end=" ")
                participant_response = request_which_row()
                if participant_response != 'r': break

            participant.set_response(step + 1, row_shuffler.index(participant_response - 1))
            if step > 0 and participant.determine_the_card(magic_deck):
                finale(participant)

    bye()


if __name__ == '__main__':
    main()
