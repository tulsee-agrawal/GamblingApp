class GamblerStatistics:

    def __init__(self, total_bets=0, total_wins=0, total_losses=0, net_profit=0):
        self.total_bets = total_bets
        self.total_wins = total_wins
        self.total_losses = total_losses
        self.net_profit = net_profit

    def win_rate(self):
        if self.total_bets == 0:
            return 0
        return (self.total_wins / self.total_bets) * 100