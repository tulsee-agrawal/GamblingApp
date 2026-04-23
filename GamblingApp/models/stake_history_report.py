class StakeHistoryReport:
    def __init__(self,transactions):
        self.transactions = transactions
    def total_transactions(self):
        return len(self.transactions)
    def net_profit(self):
        return sum(t.amount for t in self.transactions)
    def breakdown(self):
        result ={}
        for t in self.transactions:
            result[t.transaction_type] = result.get(t.transaction_type,0)+1
        return result