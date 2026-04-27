from models.game_result import GameResult
from models.running_totals import RunningTotals
from models.win_loss_statistics import WinLossStatistics


class WinLossCalculator:

    def __init__(self, initial_balance, outcome_strategy):
        self.totals = RunningTotals(initial_balance)
        self.stats = WinLossStatistics()
        self.strategy = outcome_strategy

    def process_game(self, bet_amount, probability):

        outcome = self.strategy.determine(probability)

        result = GameResult(
            bet_amount=bet_amount,
            outcome=outcome,
            odds=2, 
            stake_before=self.totals.current_balance
        )

        self.totals.update(result) #calulate win
        self.stats.update(result) #streak

        return result

    def summary(self):

        return {
            "balance": float(self.totals.current_balance),
            "profit": float(self.totals.net_profit()),
            "wins": self.stats.wins,
            "losses": self.stats.losses,
            "win_rate": self.stats.win_rate(),
            "max_win_streak": self.stats.max_win_streak,
            "max_loss_streak": self.stats.max_loss_streak
        }