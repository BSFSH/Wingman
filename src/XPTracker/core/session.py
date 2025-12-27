import time
from XPTracker.core.input_receiver import InputReceiver
from XPTracker.core.xp_parser import parse_xp_message


class GameSession:
    def __init__(self, receiver: InputReceiver):
        self.receiver = receiver
        self.total_xp = 0
        self.start_time = time.time()

    def get_xp_per_hour(self):
        if self.total_xp == 0: return 0
        elapsed_seconds = time.time() - self.start_time
        if elapsed_seconds < 1: return 0
        hours = elapsed_seconds / 3600
        return int(self.total_xp / hours)

    def reset(self):
        self.total_xp = 0
        self.start_time = time.time()

    def get_duration_str(self):
        elapsed = int(time.time() - self.start_time)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def process_queue(self):
        """
        Pops items, calculates XP, and returns a list of text logs for the GUI.
        """
        logs = []

        # Process everything currently in the stack
        while True:
            line = self.receiver.remove_from_top()
            if line is None:
                break

            # DEBUG: Uncomment this to see what the session actually receives
            # print(f"DEBUG Popped: {line.strip()}")

            xp_gain = parse_xp_message(line)

            if xp_gain > 0:
                print(f"DEBUG: XP FOUND: {xp_gain}")  # Keep this visible
                self.total_xp += xp_gain
                timestamp = time.strftime("%H:%M:%S", time.localtime())
                log_entry = f"[{timestamp}] +{xp_gain:,} XP"
                logs.append(log_entry)

        return logs