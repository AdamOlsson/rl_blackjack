
class Hand():
    def __init__(self, hand=[]):
        self.hand = hand
        self.sum = sum(self.hand)
        self.no_usable_aces = 0
        self.has_usable_ace = False
        self.bust = False

    def add_card(self, card):

        def is_bust():
            return self.sum > 21 and self.no_usable_aces <= 0

        self.hand.append(card)

        if card == 11:
            self.no_usable_aces += 1

        if self.no_usable_aces > 0 and self.sum + card > 21:
            self.sum -= 10
            self.no_usable_aces -= 1

        self.sum += card
        self.has_usable_ace = self.no_usable_aces > 0

        self.bust = is_bust()

    

