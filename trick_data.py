DECK_SIZE = 52
GROUP_QTY = 4   # the deck will be split during the trick into this number of groups
if DECK_SIZE % GROUP_QTY > 0:
    # make sure that number of cards in each group (GROUP_SIZE) is the same:
    raise ValueError("The quantity of groups (GROUP_QTY) must be chosen so that there is equal number of cards in each row")
else:
    GROUP_SIZE = DECK_SIZE // GROUP_QTY