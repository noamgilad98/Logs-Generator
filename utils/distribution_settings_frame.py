import ttkbootstrap as ttk
from tkinter import Canvas
import numpy as np
import tkinter as tk

class DistributionSettingsFrame:
    def __init__(self, parent, config_manager, app, name, default_key, default_value):
        self.config_manager = config_manager
        self.app = app
        self.name = name
        self.default_key = default_key
        self.default_value = default_value

        self.frame = ttk.LabelFrame(parent, text=f"{name} Settings")
        self.frame.grid(padx=10, pady=10, sticky="ew")
        self.frame.columnconfigure(1, weight=1)

        ttk.Label(self.frame, text=f"Number of distinct {name.lower()}:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.num_entry = ttk.Entry(self.frame)
        self.num_entry.insert(0, str(self.config_manager.get(self.default_key, self.default_value)))
        self.num_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.num_entry.bind("<KeyRelease>", self.update_distribution_on_entry_change)

        ttk.Label(self.frame, text=f"Select {name} Distribution Type:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.dist_type = ttk.Combobox(self.frame, values=["Uniform", "Normal", "Exponential", "Linear"], state="readonly")
        self.dist_type.set("Normal")
        self.dist_type.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.dist_type.bind("<<ComboboxSelected>>", self.update_distribution)

        self.dist_canvas = Canvas(self.frame, width=400, height=150, bg="#ffffff", highlightthickness=0)
        self.dist_canvas.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.update_distribution(None)

    def get_entries(self):
        return [
            int(self.num_entry.get()),
            self.dist_type.get()
        ]

    def update_distribution_on_entry_change(self, event):
        self.app.update_all_distributions()

    def update_distribution(self, event):
        dist_type = self.dist_type.get()
        num_elements = int(self.num_entry.get())
        log_count = int(self.app.log_settings_frame.num_logs_entry.get())
        values = np.linspace(0, num_elements, num=log_count)

        if dist_type == "Normal":
            mean = num_elements / 2
            std_dev = mean / 3
            values = np.random.normal(loc=mean, scale=std_dev, size=log_count)
        elif dist_type == "Uniform":
            values = np.random.uniform(low=0, high=num_elements, size=log_count)
        elif dist_type == "Exponential":
            values = np.random.exponential(scale=num_elements / 5, size=log_count)
        elif dist_type == "Linear":
            values = np.linspace(0, num_elements - 1, num=log_count)

        hist, bins = np.histogram(values, bins=num_elements, range=(0, num_elements))
        self.redraw_canvas(hist, num_elements, log_count)

    def redraw_canvas(self, hist, num_elements, log_count):
        self.dist_canvas.delete("all")
        canvas_width = int(self.dist_canvas.cget("width"))
        canvas_height = int(self.dist_canvas.cget("height"))
        max_height = max(hist) if max(hist) > 0 else 1
        bar_width = canvas_width / num_elements

        for i, h in enumerate(hist):
            left = i * bar_width
            right = left + bar_width
            top = canvas_height - (h / max_height) * canvas_height
            self.dist_canvas.create_rectangle(left, top, right, canvas_height, fill="#0078d7")

        # Add horizontal lines for perspective
        for i in range(0, max_height + 1, max(1, max_height // 10)):
            y = canvas_height - (i / max_height) * canvas_height
            self.dist_canvas.create_line(0, y, canvas_width, y, fill="#dddddd", dash=(2, 2))
            self.dist_canvas.create_text(5, y, anchor="nw", text=str(i), font=("Segoe UI", 8), fill="#333333")

        self.dist_canvas.update()
