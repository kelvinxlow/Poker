class Actions:
    def __init__(self, deck):
        self.deck = deck
        self.player_cards = []
        self.community_cards = []
        self.out = False

    def initial_deal(self):
        for i in range(0, 2):
            self.player_cards.append(self.deck[0])
            self.deck.pop(0)

    def get_community(self):
        for i in range(0, 3):
            self.community_cards.append(self.deck[0])
            self.deck.pop(0)

    def get_next_community(self):
        self.community_cards.append(self.deck[0])
        self.deck.pop(0)

    def round_end(self):
        self.community_cards.clear()
        self.player_cards.clear()

    def get_deck(self):
        return self.deck

    def update_deck(self, updated_deck):
        self.deck = updated_deck

    def fold(self):
        self.out = True

    def get_player_cards(self):
        return self.player_cards

    def get_community_cards(self):
        return self.community_cards




