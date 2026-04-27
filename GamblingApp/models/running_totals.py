from decimal import Decimal


class RunningTotals:

    def __init__(self, initial_balance):
        self.initial_balance = Decimal(str(initial_balance))
        self.current_balance = self.initial_balance
        self.total_wins = Decimal("0")
        self.total_losses = Decimal("0")
        self.history = []

    def update(self, result):
        self.current_balance = result.stake_after
        self.history.append(self.current_balance)

        if result.outcome == "WIN":
            self.total_wins += result.winnings
        else:
            self.total_losses += result.loss

    def net_profit(self):
        return self.current_balance - self.initial_balance