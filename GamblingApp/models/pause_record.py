from datetime import datetime

class PauseRecord:

    def __init__(self, session_id, reason):
        self.session_id = session_id
        self.reason = reason

        self.paused_at = datetime.now()
        self.resumed_at = None

    def resume(self):
        self.resumed_at = datetime.now()

    def duration_ms(self):
        if not self.resumed_at:
            return 0
        return int((self.resumed_at - self.paused_at).total_seconds() * 1000)