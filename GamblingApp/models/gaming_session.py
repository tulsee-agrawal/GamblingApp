from datetime import datetime
import random

from models.session_status import SessionStatus
from models.session_end_reason import SessionEndReason
from models.game_record import GameRecord
from models.pause_record import PauseRecord


class GamingSession:

    def __init__(self, session_id, gambler_id, initial_stake, params):
        self.session_id = session_id
        self.gambler_id = gambler_id

        self.initial_stake = initial_stake
        self.current_stake = initial_stake

        self.params = params

        self.status = SessionStatus.INITIALIZED
        self.end_reason = None

        self.games = []
        self.pauses = []
        self.current_pause = None

        self.win_streak = 0
        self.loss_streak = 0

        self.started_at = None
        self.ended_at = None

    def start(self):
        self.status = SessionStatus.ACTIVE
        self.started_at = datetime.now()

    def play_game(self, bet):

        if self.status != SessionStatus.ACTIVE:
            raise Exception("Session not active")

   
        if bet.bet_amount < self.params.min_bet or bet.bet_amount > self.params.max_bet:
            raise Exception("Bet out of bounds")

        stake_before = self.current_stake

     
        outcome = bet.outcome

        if outcome == "WIN":
            payout = bet.bet_amount
            loss = 0
            self.current_stake += bet.bet_amount

            self.win_streak += 1
            self.loss_streak = 0

        else:
            payout = 0
            loss = bet.bet_amount
            self.current_stake -= bet.bet_amount

            self.loss_streak += 1
            self.win_streak = 0

        record = GameRecord(
            self.session_id,
            bet.bet_id,
            outcome,
            payout,
            loss,
            stake_before,
            self.current_stake,
            self.win_streak,
            self.loss_streak
        )

        self.games.append(record)

        self.check_end_conditions()

        return record

    def check_end_conditions(self):

        if self.current_stake >= self.params.upper_limit:
            self.end(SessionEndReason.UPPER_LIMIT, SessionStatus.ENDED_WIN)

        elif self.current_stake <= self.params.lower_limit:
            self.end(SessionEndReason.LOWER_LIMIT, SessionStatus.ENDED_LOSS)

        elif len(self.games) >= self.params.max_games:
            self.end(SessionEndReason.TIMEOUT, SessionStatus.ENDED_MANUAL)

        elif (datetime.now() - self.started_at).seconds >= self.params.max_duration_sec:
            self.end(SessionEndReason.TIMEOUT, SessionStatus.ENDED_MANUAL)

    def pause(self, reason):
        if self.status != SessionStatus.ACTIVE:
            raise Exception("Only active session can be paused")

        pause = PauseRecord(self.session_id, reason)
        self.current_pause = pause
        self.pauses.append(pause)

        self.status = SessionStatus.PAUSED

    def resume(self):
        if self.status != SessionStatus.PAUSED:
            raise Exception("Session not paused")

        self.current_pause.resume()
        self.status = SessionStatus.ACTIVE

    def end(self, reason, status):
        self.status = status
        self.end_reason = reason
        self.ended_at = datetime.now()

    def summary(self):
        wins = sum(1 for g in self.games if g.outcome == "WIN")

        total_pause = sum(p.duration_ms() for p in self.pauses)

        return {
            "games_played": len(self.games),
            "wins": wins,
            "losses": len(self.games) - wins,
            "profit_loss": self.current_stake - self.initial_stake,
            "final_stake": self.current_stake,
            "status": self.status.value,
            "end_reason": self.end_reason.value if self.end_reason else None,
            "pause_time_ms": total_pause
        }