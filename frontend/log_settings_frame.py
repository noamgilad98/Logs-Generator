import ttkbootstrap as ttk

class LogSettingsFrame:
    def __init__(self, parent, config_manager, app):
        self.config_manager = config_manager
        self.parent = parent
        self.app = app

        self.log_group = ttk.LabelFrame(parent, text="Log Settings")
        self.log_group.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.log_group.columnconfigure(1, weight=1)

        ttk.Label(self.log_group, text="Enter number of logs:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.num_logs_entry = ttk.Entry(self.log_group)
        self.num_logs_entry.insert(0, str(self.config_manager.get('log_count_default')))
        self.num_logs_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.num_logs_entry.bind("<KeyRelease>", self.update_all_distributions)

        ttk.Label(self.log_group, text="Select time span:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.time_span_entry = ttk.Combobox(self.log_group, values=list(self.config_manager.get('time_span_options').keys()), state="readonly")
        self.time_span_entry.set('24 hours')
        self.time_span_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def get_entries(self):
        return [
            self.time_span_entry.get(),
            int(self.num_logs_entry.get())
        ]

    def update_all_distributions(self, event=None):
        self.app.update_all_distributions()
