import ttkbootstrap as ttk
from tkinter import Canvas
import numpy as np
from logs_generator.utils.distribution_util import generate_distribution
import tkinter as tk

class DistributionSettingsFrame:
    def __init__(self, parent, config_manager, app, title, default_count_key, row):
        self.config_manager = config_manager
        self.app = app

        self.group = ttk.LabelFrame(parent, text=title)
        self.group.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
        self.group.columnconfigure(1, weight=1)

        ttk.Label(self.group, text=f"Number of distinct {title.lower()}:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.num_entry = ttk.Entry(self.group)
        self.num_entry.insert(0, str(self.config_manager.get(default_count_key)))
        self.num_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.num_entry.bind("<KeyRelease>", self.update_distribution)

        ttk.Label(self.group, text=f"Select {title} Distribution Type:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.distribution_type = ttk.Combobox(self.group, values=["Uniform", "Normal", "Exponential"], state="readonly")
        self.distribution_type.set("Normal")
        self.distribution_type.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.distribution_type.bind("<<ComboboxSelected>>", self.update_distribution)

        self.dist_canvas = Canvas(self.group, width=400, height=150, bg="#ffffff", highlightthickness=0)
        self.dist_canvas.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.update_distribution(None)

    def get_entries(self):
        return [
            int(self.num_entry.get()),
            self.distribution_type.get()
        ]

    def update_distribution(self, event=None):
        log_count = int(self.app.log_settings_frame.num_logs_entry.get())
        num_entries = int(self.num_entry.get())

        if num_entries > log_count:
            self.num_entry.delete(0, tk.END)
            self.num_entry.insert(0, str(log_count))
            num_entries = log_count

        dist_type = self.distribution_type.get()
        values = generate_distribution(log_count, dist_type)

        hist, bins = np.histogram(values, bins=num_entries, range=(0, num_entries))
        self.redraw_canvas(hist, num_entries, log_count)

    def redraw_canvas(self, hist, num_entries, log_count):
        self.dist_canvas.delete("all")
        canvas_width = int(self.dist_canvas.cget("width"))
        canvas_height = int(self.dist_canvas.cget("height"))
        max_height = max(hist) if max(hist) > 0 else 1
        bar_width = canvas_width / num_entries

        for i, h in enumerate(hist):
            left = i * bar_width
            right = left + bar_width
            top = canvas_height - (h / max_height) * canvas_height
            self.dist_canvas.create_rectangle(left, top, right, canvas_height, fill="#0078d7")

        for i in range(0, max_height + 1, max(1, max_height // 10)):
            y = canvas_height - (i / max_height) * canvas_height
            self.dist_canvas.create_text(-10, y, anchor="e", text=str(i), font=("Segoe UI", 8), fill="#333333")
        
        self.dist_canvas.create_line(0, canvas_height, 0, 0, fill="#ff0000", dash=(4, 2))
        self.dist_canvas.create_text(-10, 0, anchor="e", text=str(log_count), font=("Segoe UI", 8), fill="#ff0000")

        self.dist_canvas.update()
