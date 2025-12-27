import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext  # Import this
from XPTracker.core.session import GameSession


class XPTrackerApp:
    def __init__(self, session: GameSession):
        self.session = session

        self.root = tk.Tk()
        self.root.title("Olmran XP Tracker")
        self.root.geometry("400x300")  # Made it slightly bigger
        self.root.attributes("-topmost", True)

        self.var_total_xp = tk.StringVar(value="Total XP: 0")
        self.var_xp_hr = tk.StringVar(value="XP/Hr: 0")
        self.var_duration = tk.StringVar(value="Time: 00:00:00")  # NEW

        self.setup_ui()
        self.update_gui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top Stats Row
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        # Column 1: Totals
        col1 = ttk.Frame(stats_frame)
        col1.pack(side=tk.LEFT, padx=10)
        ttk.Label(col1, textvariable=self.var_total_xp, font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(col1, textvariable=self.var_xp_hr).pack(anchor="w")

        # Column 2: Time & Reset
        col2 = ttk.Frame(stats_frame)
        col2.pack(side=tk.RIGHT, padx=10)
        ttk.Label(col2, textvariable=self.var_duration, font=("Consolas", 10)).pack(anchor="e")
        ttk.Button(col2, text="Reset", command=self.reset_stats, width=6).pack(pady=2)

        # Log Area (NEW)
        lbl_log = ttk.Label(main_frame, text="Recent Events:")
        lbl_log.pack(anchor="w")

        self.log_widget = scrolledtext.ScrolledText(main_frame, height=10, state='disabled', font=("Consolas", 9))
        self.log_widget.pack(fill=tk.BOTH, expand=True)
        # Add a tag to color the XP numbers green later if we want
        self.log_widget.tag_config("green", foreground="#006400")

    def reset_stats(self):
        self.session.reset()
        self.log_widget.configure(state='normal')
        self.log_widget.delete(1.0, tk.END)  # Clear the text box
        self.log_widget.configure(state='disabled')

    def update_gui(self):
        # 1. Get logs from session
        new_logs = self.session.process_queue()

        # 2. Update Text Widget if there are new logs
        if new_logs:
            self.log_widget.configure(state='normal')  # Unlock to write
            for entry in new_logs:
                self.log_widget.insert(tk.END, entry + "\n")
            self.log_widget.see(tk.END)  # Auto-scroll to bottom
            self.log_widget.configure(state='disabled')  # Lock again

        # 3. Update Variables
        current_xp = self.session.total_xp
        current_rate = self.session.get_xp_per_hour()

        self.var_total_xp.set(f"Total: {current_xp:,}")
        self.var_xp_hr.set(f"{current_rate:,} /hr")
        self.var_duration.set(self.session.get_duration_str())

        self.root.after(100, self.update_gui)

    def run(self):
        self.root.mainloop()