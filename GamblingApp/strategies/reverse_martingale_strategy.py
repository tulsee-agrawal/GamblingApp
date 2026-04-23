from strategies.base_strategy import BettingStrategy

class ReverseMartingaleStrategy(BettingStrategy):

    def __init__(self, base_amount):
        self.base_amount = base_amount
        self.current_amount = base_amount

    def get_bet_amount(self, current_stake):
        return self.current_amount

    def update_after_result(self, outcome):
        if outcome == "WIN":
            self.current_amount *= 2
        else:
            self.current_amount = self.base_amount