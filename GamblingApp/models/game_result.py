from decimal import Decimal


class GameResult:

    def __init__(self, bet_amount, outcome, odds, stake_before):
        self.bet_amount = Decimal(str(bet_amount))
        self.outcome = outcome
        self.odds = Decimal(str(odds))
        self.stake_before = Decimal(str(stake_before))
        self.stake_after = self.stake_before
        self.winnings = Decimal("0")
        self.loss = Decimal("0")
        self.calculate()

    def calculate(self):
        if self.outcome == "WIN":
            self.winnings = self.bet_amount * self.odds
            self.stake_after += self.winnings
        else:
            self.loss = self.bet_amount
            self.stake_after -= self.loss