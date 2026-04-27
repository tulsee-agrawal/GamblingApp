from decimal import Decimal

from db.connection import get_connection

class GamblerProfileService:
    def create_gambler(self, profile, preferences):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM gamblers WHERE username=%s", (profile.username,))
        if cursor.fetchone():
            raise Exception("Username already exists")

        cursor.execute("""
            INSERT INTO gamblers
            (username, full_name, email, is_active,
             initial_stake, current_stake,
             win_threshold, loss_threshold, min_required_stake)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            profile.username,
            profile.full_name,
            profile.email,
            profile.is_active,
            profile.initial_stake,
            profile.current_stake,
            profile.win_threshold,
            profile.loss_threshold,
            profile.min_required_stake
        ))

        gambler_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO betting_preferences
            (gambler_id, min_bet, max_bet, preferred_game_type,
             auto_play_enabled, auto_play_max_games,
             session_loss_limit, session_win_target)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            gambler_id,
            preferences.min_bet,
            preferences.max_bet,
            preferences.preferred_game_type,
            preferences.auto_play_enabled,
            preferences.auto_play_max_games,
            preferences.session_loss_limit,
            preferences.session_win_target
        ))

        conn.commit()
        conn.close()
    def update_gambler(self, username, profile_data=None, pref_data=None):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT gambler_id FROM gamblers WHERE username=%s", (username,))
        result = cursor.fetchone()

        if not result:
            raise Exception("Gambler not found")

        gambler_id = result[0]

        if profile_data:
            for key, value in profile_data.items():
                query = f"UPDATE gamblers SET {key}=%s WHERE gambler_id=%s"
                cursor.execute(query, (value, gambler_id))
                # print(f"Updated gamblers: {key} = {value}")

        if pref_data:
            for key, value in pref_data.items():
                query = f"UPDATE betting_preferences SET {key}=%s WHERE gambler_id=%s"
                cursor.execute(query, (value, gambler_id))
                # print(f"Updated preferences: {key} = {value}")

        conn.commit()
        conn.close()

        print("Update completed")
    def get_gambler(self, username):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM gamblers WHERE username=%s", (username,))
        gambler = cursor.fetchone()

        if not gambler:
            return None

        cursor.execute("SELECT * FROM betting_preferences WHERE gambler_id=%s",
                       (gambler["gambler_id"],))
        prefs = cursor.fetchone()

        conn.close()

        return {
            "profile": gambler,
            "preferences": prefs
        }
    def validate_eligibility(self, username):
        data = self.get_gambler(username)

        if not data:
            return "Gambler not found"

        g = data["profile"]

        if g["current_stake"] < g["min_required_stake"]:
            return "Below minimum stake"

        if not g["is_active"]:
            return "Account inactive"

        return "Eligible"
    def reset_profile(self, username):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM gamblers WHERE username=%s", (username,))
        gambler = cursor.fetchone()

        if not gambler:
            raise Exception("Gambler not found")

        initial = gambler["initial_stake"]
       
        new_win = initial * Decimal("1.5")
        new_loss = initial * Decimal("0.5")

        cursor.execute("""
            UPDATE gamblers
            SET current_stake=%s,
                win_threshold=%s,
                loss_threshold=%s
            WHERE username=%s
        """, (initial, new_win, new_loss, username))

        conn.commit()
        conn.close()