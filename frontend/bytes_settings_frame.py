import ttkbootstrap as ttk

class BytesSettingsFrame:
    def __init__(self, parent, config_manager, app):
        self.config_manager = config_manager
        self.app = app

        self.frame = ttk.LabelFrame(parent, text="Bytes Sent and Received Settings")
        self.frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.frame.columnconfigure(0, weight=1)  # Give full weight to the main frame's column

        # Group for bytes sent settings
        bytes_sent_group = ttk.LabelFrame(self.frame, text="Bytes Sent Settings")
        bytes_sent_group.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        for i in range(3):
            bytes_sent_group.columnconfigure(i, weight=1)  # Give equal weight for alignment

        # Entry for minimum bytes sent
        ttk.Label(bytes_sent_group, text="Min bytes sent:").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.min_sent_entry = ttk.Entry(bytes_sent_group)
        self.min_sent_entry.insert(0, str(self.config_manager.get('bytes_sent_min_default')))
        self.min_sent_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Entry for maximum bytes sent
        ttk.Label(bytes_sent_group, text="Max bytes sent:").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.max_sent_entry = ttk.Entry(bytes_sent_group)
        self.max_sent_entry.insert(0, str(self.config_manager.get('bytes_sent_max_default')))
        self.max_sent_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Entry for average bytes sent
        ttk.Label(bytes_sent_group, text="Avg bytes sent:").grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.avg_sent_entry = ttk.Entry(bytes_sent_group)
        self.avg_sent_entry.insert(0, str(self.config_manager.get('bytes_sent_avg_default')))
        self.avg_sent_entry.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Group for bytes received settings
        bytes_received_group = ttk.LabelFrame(self.frame, text="Bytes Received Settings")
        bytes_received_group.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        for i in range(3):
            bytes_received_group.columnconfigure(i, weight=1)  # Equal weight for alignment

        # Entry for minimum bytes received
        ttk.Label(bytes_received_group, text="Min bytes received:").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.min_received_entry = ttk.Entry(bytes_received_group)
        self.min_received_entry.insert(0, str(self.config_manager.get('bytes_received_min_default')))
        self.min_received_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Entry for maximum bytes received
        ttk.Label(bytes_received_group, text="Max bytes received:").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.max_received_entry = ttk.Entry(bytes_received_group)
        self.max_received_entry.insert(0, str(self.config_manager.get('bytes_received_max_default')))
        self.max_received_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Entry for average bytes received
        ttk.Label(bytes_received_group, text="Avg bytes received:").grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.avg_received_entry = ttk.Entry(bytes_received_group)
        self.avg_received_entry.insert(0, str(self.config_manager.get('bytes_received_avg_default')))
        self.avg_received_entry.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    def get_entries(self):
        return [
            int(self.min_sent_entry.get()),
            int(self.max_sent_entry.get()),
            int(self.avg_sent_entry.get()),
            int(self.min_received_entry.get()),
            int(self.max_received_entry.get()),
            int(self.avg_received_entry.get())
        ]
