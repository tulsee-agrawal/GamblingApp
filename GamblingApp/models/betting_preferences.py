class BettingPreferences:

    def __init__(self, min_bet, max_bet, game_type,
                 auto_play=False, auto_games=0,
                 session_loss_limit=None,
                 session_win_target=None):

        self.min_bet = min_bet
        self.max_bet = max_bet
        self.preferred_game_type = game_type
        self.auto_play_enabled = auto_play
        self.auto_play_max_games = auto_games
        self.session_loss_limit = session_loss_limit
        self.session_win_target = session_win_target
        self.validate()

    def validate(self):
        if self.min_bet <= 0:
            raise Exception("Min bet must be > 0")

        if self.max_bet < self.min_bet:
            raise Exception("Max bet must be >= min bet")

        if self.session_loss_limit is not None and self.session_loss_limit < 0:
            raise Exception("Session loss limit cannot be negative")

        if self.session_win_target is not None and self.session_win_target < 0:
            raise Exception("Session win target cannot be negative")