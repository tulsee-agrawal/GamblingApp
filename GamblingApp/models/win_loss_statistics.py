class WinLossStatistics:

    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.current_win_streak = 0
        self.current_loss_streak = 0
        self.max_win_streak = 0
        self.max_loss_streak = 0

    def update(self, result):

        if result.outcome == "WIN":
            self.wins += 1
            self.current_win_streak += 1
            self.current_loss_streak = 0

            self.max_win_streak = max(self.max_win_streak, self.current_win_streak)

        else:
            self.losses += 1
            self.current_loss_streak += 1
            self.current_win_streak = 0

            self.max_loss_streak = max(self.max_loss_streak, self.current_loss_streak)

    def win_rate(self):
        total = self.wins + self.losses
        return (self.wins / total) if total else 0