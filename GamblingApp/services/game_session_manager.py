from db.connection import get_connection
from models.gaming_session import GamingSession

def save_game_record(record):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO game_records
        (session_id, bet_id, odds_config_id,
         outcome, payout_amount, loss_amount, net_change,
         stake_before, stake_after,
         consecutive_win_streak, consecutive_loss_streak,
         game_duration_ms, resolved_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        record.session_id,
        record.bet_id,
        record.odds_config_id,
        record.outcome,
        record.payout_amount,
        record.loss_amount,
        record.net_change,
        record.stake_before,
        record.stake_after,
        record.consecutive_win_streak,
        record.consecutive_loss_streak,
        record.game_duration_ms,
        record.resolved_at
    ))

    conn.commit()
    conn.close()

class GameSessionManager:

    def __init__(self):
        self.active_sessions = {}
        self.completed_sessions = {}

   
    def start_new_session(self, session_id, gambler_id, initial_stake, params):

        if gambler_id in self.active_sessions:
            raise Exception("Active session already exists")

        session = GamingSession(session_id, gambler_id, initial_stake, params)
        session.start()

        self.active_sessions[gambler_id] = session
        return session

    def continue_session(self, gambler_id, betting_service, strategy):

        session = self.active_sessions[gambler_id]

        game_index = 1

        while session.status == session.status.ACTIVE:

            bet = betting_service.place_bet_with_strategy(
                session.session_id,
                gambler_id,
                strategy,
                game_index,
                session.params.win_probability
            )

            record = session.play_game(bet)
            save_game_record(record)
            game_index += 1

        self.completed_sessions[gambler_id] = session
        del self.active_sessions[gambler_id]

        return session.summary()

    def pause_session(self, gambler_id, reason):
        self.active_sessions[gambler_id].pause(reason)

    def resume_session(self, gambler_id):
        self.active_sessions[gambler_id].resume()
    
    