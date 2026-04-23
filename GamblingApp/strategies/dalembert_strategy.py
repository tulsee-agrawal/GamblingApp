from strategies.base_strategy import BettingStrategy

class DAlembertStrategy(BettingStrategy):

    def __init__(self, base_amount, step=10):
        self.base_amount = base_amount
        self.step = step
        self.current_amount = base_amount

    def get_bet_amount(self, current_stake):
        return self.current_amount

    def update_after_result(self, outcome):
        if outcome == "LOSS":
            self.current_amount += self.step
        else:
            self.current_amount = max(self.base_amount, self.current_amount - self.step)