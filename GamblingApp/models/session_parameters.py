class SessionParameters:

    def __init__(self, upper_limit, lower_limit,
                 min_bet, max_bet,
                 max_games=100,
                 max_duration_sec=3600,
                 win_probability=0.5):

        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

        self.min_bet = min_bet
        self.max_bet = max_bet

        self.max_games = max_games
        self.max_duration_sec = max_duration_sec

        self.win_probability = win_probability