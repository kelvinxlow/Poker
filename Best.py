class Best:
    def __init__(self):
        self.player_five_oak = None
        self.player_best = None
        self.flush_suit = None
        self.player_cards = []
        self.comm_cards = []
        self.player_hand = []
        self.high = None
        self.tie_break_one = None
        self.tie_break_two = None


    def sort_hand(self):
        for i in range(1, len(self.player_cards)):
            replacement = self.player_cards[i]
            j = i - 1
            while j >= 0 and int(self.player_cards[j][:-1]) > int(replacement[:-1]):
                self.player_cards[j + 1] = self.player_cards[j]
                j -= 1
            self.player_cards[j + 1] = replacement

    def suit_sets(self):
        splits = [0, 0, 0, 0]
        for i in range(0, len(self.player_cards)):
            if (self.player_cards[i])[-1] == 'D':
                splits[0] += 1
            elif (self.player_cards[i])[-1] == 'C':
                splits[1] += 1
            elif (self.player_cards[i])[-1] == 'H':
                splits[2] += 1
            else:
                splits[3] += 1

        for j in range(0, 4):
            if splits[j] >= 5:
                self.player_five_oak = j

    def get_flush_suit(self):
        if self.player_five_oak == 0:
            self.flush_suit = 'D'
        elif self.player_five_oak == 1:
            self.flush_suit = 'C'
        elif self.player_five_oak == 2:
            self.flush_suit = 'H'
        else:
            self.flush_suit = 'S'

    def royal_flush(self):
        if self.player_five_oak is not None:
            self.get_flush_suit()
            current_check = 0
            search = 13
            while int(self.player_cards[current_check][:-1]) == 1:
                if self.player_cards[current_check][-1] == self.flush_suit:
                    current_check = len(self.player_cards) - 1
                else:
                    current_check += 1
            if current_check == len(self.player_cards) - 1:
                if current_check >= 1:
                    while int(self.player_cards[current_check][:-1]) == search:
                        if self.player_cards[current_check][-1] == self.flush_suit:
                            current_check -= 1
                            search -= 1
                        else:
                            current_check -= 1
            if search == 9:
                print("check")
                self.player_best = "Royal Flush"
                self.tie_break_one = 0
                self.tie_break_two = None

    def straight_flush(self):
        if self.player_five_oak is not None:
            current_check = 0
            chain = 1
            while self.player_cards[current_check][-1] != self.flush_suit:
                current_check += 1
            card_rank = int(self.player_cards[current_check][:-1])
            current_check += 1
            while int(self.player_cards[current_check][:-1]) == card_rank:
                current_check += 1
            while current_check < len(self.player_cards):
                if int(self.player_cards[current_check][:-1]) == (card_rank + 1) and self.player_cards[current_check][-1] == self.flush_suit:
                    chain += 1
                    card_rank += 1
                    if chain >= 5:
                        self.player_best = "Straight Flush"
                        self.tie_break_one = card_rank
                        self.tie_break_two = None
                elif int(self.player_cards[current_check][:-1]) > card_rank + 1:
                    chain = 0
                    card_rank = int(self.player_cards[current_check][:-1])
                current_check += 1

    def four_oak(self):
        current_check = 1
        same_rank = 1
        current_rank = int(self.player_cards[0][:-1])
        while current_check < len(self.player_cards):
            if current_rank == int(self.player_cards[current_check][:-1]):
                same_rank += 1
                if same_rank == 4:
                    self.player_best = "Four of a Kind"
                    self.tie_break_one = current_rank
                    self.tie_break_two = None
                    break
            else:
                current_rank = int(self.player_cards[current_check][:-1])
                same_rank = 1
            current_check += 1

    def full_house(self):
        current_check = len(self.player_cards)-2
        current_rank = int(self.player_cards[len(self.player_cards)-1][:-1])
        three = 0
        two = 0
        same_rank = 1
        while current_check >= 0:
            if current_rank == int(self.player_cards[current_check][:-1]):
                same_rank += 1
                if same_rank == 3 and three == 0:
                    three = current_rank
                    if two is current_rank:
                        two = 0
                elif same_rank == 3:
                    two = current_rank
                    break
                elif same_rank == 2 and two == 0:
                    two = current_rank
            else:
                current_rank = int(self.player_cards[current_check][:-1])
                same_rank = 1
            current_check -= 1
        if three > 0 and two > 0:
            self.player_best = "Full House"
            self.tie_break_one = three
            self.tie_break_two = two

    def flush(self):
        if self.player_five_oak is not None:
            self.player_best = "Flush"
            flush_high = len(self.player_cards)
            while True:
                flush_high -= 1
                if self.player_cards[flush_high][-1] == self.flush_suit:
                    self.tie_break_one = int(self.player_cards[flush_high][:-1])
                    break


    def straight(self):
        current_check = 1
        chain = 1
        card_rank = int(self.player_cards[0][:-1])
        while current_check < len(self.player_cards):
            if int(self.player_cards[current_check][:-1]) == (card_rank + 1):
                chain += 1
                card_rank += 1
                if chain >= 5:
                    self.player_best = "Straight"
                    self.tie_break_one = card_rank
                    self.tie_break_two = None
            elif int(self.player_cards[current_check][:-1]) > card_rank + 1:
                chain = 1
                card_rank = int(self.player_cards[current_check][:-1])
            current_check += 1

    def three_oak(self):
        current_check = len(self.player_cards) - 2
        current_rank = int(self.player_cards[len(self.player_cards) - 1][:-1])
        same_rank = 1
        while current_check >= 0:
            if current_rank == int(self.player_cards[current_check][:-1]):
                same_rank += 1
                if same_rank == 3:
                    self.player_best = "Three of a Kind"
                    self.tie_break_one = current_rank
                    self.tie_break_two = None
            else:
                current_rank = int(self.player_cards[current_check][:-1])
                same_rank = 1
            current_check -= 1

    def two_pair(self):
        current_check = len(self.player_cards) - 2
        current_rank = int(self.player_cards[len(self.player_cards) - 1][:-1])
        pair_one = 0
        pair_two = 0
        same_rank = 1
        while current_check >= 0:
            if current_rank == int(self.player_cards[current_check][:-1]):
                same_rank += 1
                if same_rank == 2 and pair_one == 0:
                    pair_one = current_rank
                elif same_rank == 2 and pair_two == 0:
                    pair_two = current_rank
                    self.player_best = "Two Pair"
                    self.tie_break_one = pair_one
                    self.tie_break_two = pair_two
                #error when there is a pair ace because of its placement
            else:
                current_rank = int(self.player_cards[current_check][:-1])
                same_rank = 1
            current_check -= 1

    def one_pair(self):
        current_check = len(self.player_cards) - 2
        current_rank = int(self.player_cards[len(self.player_cards) - 1][:-1])
        same_rank = 1
        while current_check >= 0:
            if current_rank == int(self.player_cards[current_check][:-1]):
                same_rank += 1
                if same_rank == 2:
                    self.player_best = "Pair"
                    self.tie_break_one = current_rank
                    self.tie_break_two = None
            else:
                current_rank = int(self.player_cards[current_check][:-1])
                same_rank = 1
            current_check -= 1

    def high_card(self):
        if int(self.player_cards[0][:-1]) == 1:
            self.high = 14
        else:
            self.high = int(self.player_cards[len(self.player_cards) - 1][:-1])
        self.player_best = "High Card"
        self.tie_break_one = self.high
        self.tie_break_two = None

    def get_player_cards(self):
        self.player_cards = self.player_hand + self.comm_cards

    def get_community_card(self, community_cards):
        self.comm_cards = community_cards

    def get_player_hand(self, player_cards):
        self.player_hand = player_cards

    def reset_best(self):
        self.player_best = None