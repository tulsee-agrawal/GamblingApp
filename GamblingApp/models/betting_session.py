from datetime import datetime

class BettingSession:

    def __init__(self, session_id, gambler_id, starting_stake):
        self.session_id = session_id
        self.gambler_id = gambler_id
        self.starting_stake = starting_stake
        self.ending_stake = starting_stake
        self.peak = starting_stake
        self.lowest = starting_stake
        self.bets = []
        self.started_at = datetime.now()
        self.ended_at = None
        
    def add_bet(self, bet):
        self.bets.append(bet)
        self.ending_stake = bet.stake_after
        self.peak = max(self.peak, bet.stake_after)
        self.lowest = min(self.lowest, bet.stake_after)

    def end_session(self):
        self.ended_at = datetime.now()

    def summary(self):
        wins = 0
        for b in self.bets:
            if b.outcome == "WIN":
                wins += 1
        losses = len(self.bets) - wins
        return {
            "total_bets": len(self.bets),
            "wins": wins,
            "losses": losses,
            "profit_loss": self.ending_stake - self.starting_stake,
            "peak": self.peak,
            "lowest": self.lowest
        }