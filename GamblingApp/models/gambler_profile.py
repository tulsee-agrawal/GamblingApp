class GamblerProfile:

    def __init__(self, username, full_name, email,
                 initial_stake, win_threshold, loss_threshold,
                 min_required_stake):

        self.username = username
        self.full_name = full_name
        self.email = email
        self.is_active = True
        self.initial_stake = initial_stake
        self.current_stake = initial_stake
        self.win_threshold = win_threshold
        self.loss_threshold = loss_threshold
        self.min_required_stake = min_required_stake
        self.validate()

    def validate(self):
        if self.initial_stake <= 0:
            raise Exception("Initial stake must be > 0")

        if self.win_threshold <= self.initial_stake:
            raise Exception("Win threshold must be greater than initial stake")

        if self.loss_threshold >= self.initial_stake:
            raise Exception("Loss threshold must be less than initial stake")