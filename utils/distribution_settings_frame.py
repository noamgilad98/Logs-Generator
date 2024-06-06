import ttkbootstrap as ttk
from tkinter import Canvas
import numpy as np

class DistributionSettingsFrame:
    def __init__(self, parent, config_manager, app, title, config_key, default_value):
        self.config_manager = config_manager
        self.app = app
        self.title = title
        self.config_key = config_key
        self.default_value = default_value

        self.frame = ttk.LabelFrame(parent, text=f"{title} Settings")
        self.frame.grid(padx=10, pady=10, sticky="ew")
        self.frame.columnconfigure(1, weight=1)

        ttk.Label(self.frame, text=f"Number of distinct {title.lower()}:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.num_distinct_entry = ttk.Entry(self.frame)
        self.num_distinct_entry.insert(0, str(self.config_manager.get(self.config_key, self.default_value)))
        self.num_distinct_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.num_distinct_entry.bind("<FocusOut>", self.update_distribution)
        self.num_distinct_entry.bind("<Return>", self.update_distribution)
        self.num_distinct_entry.bind("<KeyRelease>", self.update_distribution)  # Update on key release

        ttk.Label(self.frame, text=f"Select {title} Distribution Type:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.distribution_type = ttk.Combobox(self.frame, values=["Uniform", "Normal", "Exponential"], state="readonly")
        self.distribution_type.set("Uniform")
        self.distribution_type.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.distribution_type.bind("<<ComboboxSelected>>", self.update_distribution)

        self.dist_canvas = Canvas(self.frame, width=450, height=150, bg="#ffffff", highlightthickness=0)
        self.dist_canvas.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.update_distribution(None)

    def get_entries(self):
        return [int(self.num_distinct_entry.get()), self.distribution_type.get()]

    def update_distribution(self, event):
        num_logs = int(self.app.log_settings_frame.num_logs_entry.get())
        num_distinct = int(self.num_distinct_entry.get())
        
        if num_distinct > num_logs:
            num_distinct = num_logs
            self.num_distinct_entry.delete(0, "end")
            self.num_distinct_entry.insert(0, str(num_logs))

        values = self.generate_distribution(num_logs, num_distinct)
        hist, _ = np.histogram(values, bins=num_distinct, range=(0, num_distinct))

        if self.distribution_type.get() == "Exponential":
            hist = sorted(hist, reverse=True)
        elif self.distribution_type.get() == "Normal":
            hist = sorted(hist[:len(hist)//2]) + sorted(hist[len(hist)//2:], reverse=True)

        self.redraw_canvas(hist, num_logs)

    def generate_distribution(self, num_logs, num_distinct):
        dist_type = self.distribution_type.get()
        if dist_type == "Normal":
            mean = num_distinct / 2
            std_dev = mean / 3
            values = np.random.normal(loc=mean, scale=std_dev, size=num_logs)
        elif dist_type == "Exponential":
            values = np.random.exponential(scale=num_distinct / 5, size=num_logs)
        else:  # Uniform
            values = np.tile(np.arange(num_distinct), num_logs // num_distinct + 1)[:num_logs]
        return values
    
    def redraw_canvas(self, hist, num_logs):
        self.dist_canvas.delete("all")
        canvas_width = int(self.dist_canvas.cget("width"))
        canvas_height = int(self.dist_canvas.cget("height"))
        max_height = max(hist) if max(hist) > 0 else 1
        max_height_with_padding = max_height * 1.2  # Add more padding at the top
        bar_width = canvas_width / (len(hist) + 1)  # Add space for the y-axis labels

        for i, h in enumerate(hist):
            left = (i + 1) * bar_width  # Shift bars to the right
            right = left + bar_width
            top = canvas_height - (h / max_height_with_padding) * canvas_height  # Adjusted to use max_height_with_padding
            self.dist_canvas.create_rectangle(left, top, right, canvas_height, fill="#0078d7")

        self.draw_y_axis(canvas_height, max_height_with_padding)

    def draw_y_axis(self, canvas_height, max_height_with_padding):
        step = max(1, round(max_height_with_padding / 5))
        for i in range(0, int(max_height_with_padding) + step, step):
            y = canvas_height - (i / max_height_with_padding) * canvas_height  # Adjusted to use max_height_with_padding
            self.dist_canvas.create_text(30, y, text=f"{i:,}", anchor="w", font=("Segoe UI", 8), fill="#333333")

        # Ensure the top and bottom labels fit within the canvas
        self.dist_canvas.create_text(30, canvas_height, text="0", anchor="w", font=("Segoe UI", 8), fill="#333333")
        self.dist_canvas.create_text(30, canvas_height - (max_height_with_padding / max_height_with_padding) * canvas_height, text=f"{int(max_height_with_padding):,}", anchor="w", font=("Segoe UI", 8), fill="#333333")
