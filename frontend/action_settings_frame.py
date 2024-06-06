import ttkbootstrap as ttk

class ActionSettingsFrame:
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Action Settings")
        self.frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.frame.columnconfigure(0, weight=1)  # Make sure the first column expands to take up space

        self.actions = {
            'Allow': ttk.BooleanVar(value=True),
            'Block': ttk.BooleanVar(value=True)
        }

        ttk.Label(self.frame, text="Select actions:").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Placing each check button in a new row
        row = 1  # Start at the next row
        for action, var in self.actions.items():
            ttk.Checkbutton(self.frame, text=action, variable=var).grid(row=row, column=0, padx=10, pady=2, sticky="w")
            row += 1  # Increment row for each new checkbutton

    def get_actions(self):
        return [var.get() for var in self.actions.values()]
