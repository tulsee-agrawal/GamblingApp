class StakeMonitor:
    def __init__(self,initial_stake):
        self.initial_stake = initial_stake
        self.current_stake = initial_stake
        self.peak = initial_stake
        self.lowest = initial_stake
        self.history = [initial_stake]

    def update(self,new_stake):
        self.current_stake=new_stake
        self.history.append(new_stake)
        if new_stake>self.peak:
            self.peak = new_stake
        if new_stake<self.peak:
            self.lowest = new_stake
    def volatility(self):
        if len(self.history)<2:
            return 0
        return max(self.history)-min(self.history)
