from datetime import datetime

class GameRecord:

    def __init__(self, session_id, bet_id,
                 outcome, payout_amount, loss_amount,
                 stake_before, stake_after,
                 win_streak, loss_streak,
                 duration_ms=0):

        self.session_id = session_id
        self.bet_id = bet_id
        self.odds_config_id = None  # optional

        self.outcome = outcome

        self.payout_amount = payout_amount
        self.loss_amount = loss_amount

        self.net_change = payout_amount - loss_amount

        self.stake_before = stake_before
        self.stake_after = stake_after

        self.consecutive_win_streak = win_streak
        self.consecutive_loss_streak = loss_streak

        self.game_duration_ms = duration_ms
        self.resolved_at = datetime.now()