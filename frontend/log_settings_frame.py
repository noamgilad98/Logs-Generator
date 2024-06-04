import ttkbootstrap as ttk
import tkinter as tk

class LogSettingsFrame:
    def __init__(self, parent, config_manager, app):
        self.config_manager = config_manager
        self.app = app

        self.frame = ttk.LabelFrame(parent, text="Log Settings")
        self.frame.grid(padx=10, pady=10, sticky="ew")
        self.frame.columnconfigure(1, weight=1)

        ttk.Label(self.frame, text="Enter number of logs:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.num_logs_entry = ttk.Entry(self.frame)
        self.num_logs_entry.insert(0, str(self.config_manager.get('log_count_default', 100)))
        self.num_logs_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.num_logs_entry.bind("<KeyRelease>", self.update_all_distributions)

        ttk.Label(self.frame, text="Select time span:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.time_span_entry = ttk.Combobox(self.frame, values=list(self.config_manager.get('time_span_options').keys()), state="readonly")
        self.time_span_entry.set('24 hours')
        self.time_span_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def get_entries(self):
        return [
            self.time_span_entry.get(),
            int(self.num_logs_entry.get())
        ]

    def update_all_distributions(self, event):
        self.app.update_all_distributions()
