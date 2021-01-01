class Money:


    def __init__(self):
        self.total = 100
        self.big_blind = 10

    def set_start(self, total, big_blind):
        self.total = total
        self.big_blind = big_blind

    def bet(self, amount):
        self.total -= amount

    def win(self, amount):
        self.total += amount

    def get_total(self):
        return self.total
