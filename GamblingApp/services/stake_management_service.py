from db.connection import get_connection
from models.transaction_type import TransactionType
from models.stake_transaction import StakeTransaction
from models.stake_monitor import StakeMonitor
from models.stake_boundary import StakeBoundary


class StakeManagementService:

    def initialize_stake(self, session_id, gambler_id, initial_amount):
        conn = get_connection()
        cursor = conn.cursor()

        # update gambler current stake
        cursor.execute("""
            UPDATE gamblers
            SET current_stake=%s
            WHERE gambler_id=%s
        """, (initial_amount, gambler_id))

        # record transaction
        cursor.execute("""
            INSERT INTO stake_transactions
            (session_id, gambler_id, transaction_type, amount,
             balance_before, balance_after, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,NOW())
        """, (
            session_id,
            gambler_id,
            TransactionType.INITIAL_STAKE.value,
            initial_amount,
            0,
            initial_amount
        ))

        conn.commit()
        conn.close()

        return StakeMonitor(initial_amount)

    #BET PROCESSING
    def process_bet(self, gambler_id, session_id, bet_amount, is_win):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT current_stake FROM gamblers WHERE gambler_id=%s", (gambler_id,))
        gambler = cursor.fetchone()

        current = gambler["current_stake"]

        if current < bet_amount:
            raise Exception("Insufficient balance")

        new_balance = current + bet_amount if is_win else current - bet_amount

        # update stake
        cursor.execute("""
            UPDATE gamblers SET current_stake=%s WHERE gambler_id=%s
        """, (new_balance, gambler_id))

        # record transaction
        cursor.execute("""
            INSERT INTO stake_transactions
            (session_id, gambler_id, transaction_type, amount,
             balance_before, balance_after, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,NOW())
        """, (
            session_id,
            gambler_id,
            TransactionType.BET_WIN.value if is_win else TransactionType.BET_LOSS.value,
            bet_amount,
            current,
            new_balance
        ))

        conn.commit()
        conn.close()

        return new_balance

    def get_history(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM stake_transactions WHERE gambler_id=%s
        """, (gambler_id,))

        data = cursor.fetchall()
        conn.close()

        return data
    
    