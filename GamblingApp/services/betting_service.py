from db.connection import get_connection
from models.bet import Bet
from models.betting_session import BettingSession


class BettingService:

    def __init__(self):
        self.sessions = {}

    def start_session(self, session_id, gambler_id, starting_stake):
        session = BettingSession(session_id, gambler_id, starting_stake)
        self.sessions[session_id] = session
        return session

    def place_bet(self, session_id, gambler_id, strategy_id,
                  game_index, bet_amount, win_probability):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT current_stake FROM gamblers WHERE gambler_id=%s", (gambler_id,))
        gambler = cursor.fetchone()

        if not gambler:
            raise Exception("Gambler not found")

        stake_before = gambler["current_stake"]

        if bet_amount > stake_before:
            raise Exception("Insufficient stake")

        bet = Bet(session_id, gambler_id, strategy_id,
                  game_index, bet_amount, win_probability, stake_before)

        bet.determine_outcome()
        new_stake = bet.settle()

        cursor.execute(
            "UPDATE gamblers SET current_stake=%s WHERE gambler_id=%s",
            (new_stake, gambler_id)
        )

        cursor.execute("""
            INSERT INTO bets
            (session_id, gambler_id, strategy_id, game_index,
             bet_amount, win_probability, odds_type, odds_value,
             potential_win, stake_before, stake_after, is_settled, placed_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            bet.session_id,
            bet.gambler_id,
            bet.strategy_id,
            bet.game_index,
            bet.bet_amount,
            bet.win_probability,
            bet.odds_type,
            bet.odds_value,
            bet.potential_win,
            bet.stake_before,
            bet.stake_after,
            bet.is_settled,
            bet.placed_at
        ))
        bet.bet_id = cursor.lastrowid
        conn.commit()
        conn.close()

        session = self.sessions.get(session_id)
        if session:
            session.add_bet(bet)

        return bet

    def place_bet_with_strategy(self, session_id, gambler_id,
                                strategy, game_index, win_probability):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT current_stake FROM gamblers WHERE gambler_id=%s", (gambler_id,))
        stake = cursor.fetchone()["current_stake"]
        conn.close()

        amount = strategy.get_bet_amount(stake)

        bet = self.place_bet(
            session_id,
            gambler_id,
            None,
            game_index,
            amount,
            win_probability
        )

        if hasattr(strategy, "update_after_result"):
            strategy.update_after_result(bet.outcome)

        return bet

    def place_consecutive_bets(self, session_id, gambler_id,
                               strategy, rounds, win_probability):

        results = []

        for i in range(1, rounds + 1):
            bet = self.place_bet_with_strategy(
                session_id, gambler_id, strategy, i, win_probability
            )
            results.append(bet)

        return results

    def end_session(self, session_id):
        session = self.sessions.get(session_id)
        if not session:
            raise Exception("Session not found")

        session.end_session()
        return session.summary()