import random


class Deck:
    def __init__(self):
        self.deck = []

    def generate_deck(self):
        suits = ['D', 'C', 'H', 'S']
        for s in suits:
            for r in range(1, 14):
                self.deck.append(str(r) + s)

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def get_deck(self):
        return self.deck