from datetime import datetime

class StakeTransaction:
    def __init__(self, session_id, gambler_id, amount,
                 transaction_type, balance_before, balance_after,
                 bet_id=None, game_id=None):

        self.session_id = session_id
        self.gambler_id = gambler_id
        self.bet_id = bet_id
        self.game_id = game_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_before = balance_before
        self.balance_after = balance_after
        self.created_at = datetime.now()