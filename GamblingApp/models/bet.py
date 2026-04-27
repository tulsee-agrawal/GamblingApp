import random
from datetime import datetime

class Bet:

    def __init__(self, session_id, gambler_id, strategy_id,
                 game_index, bet_amount, win_probability, stake_before):

        self.session_id = session_id
        self.gambler_id = gambler_id
        self.strategy_id = strategy_id
        self.game_index = game_index
        self.bet_amount = bet_amount
        self.win_probability = win_probability
        self.odds_type = "PROBABILITY"
        self.odds_value = 1 / win_probability if win_probability > 0 else 0 #easytowin->low reward
        self.potential_win = bet_amount * self.odds_value
        self.stake_before = stake_before
        self.stake_after = None
        self.outcome = None  # WIN / LOSS
        self.is_settled = False
        self.placed_at = datetime.now()
# if random falls in the range of win probability it is win
    def determine_outcome(self):
        rand = random.random()
        self.outcome = "WIN" if rand < self.win_probability else "LOSS"
        return self.outcome

    def settle(self):
        if self.outcome == "WIN":
            self.stake_after = self.stake_before + self.bet_amount
        else:
            self.stake_after = self.stake_before - self.bet_amount

        self.is_settled = True
        return self.stake_after