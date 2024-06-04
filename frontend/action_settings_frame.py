import ttkbootstrap as ttk

class ActionSettingsFrame:
    def __init__(self, parent):
        self.action_group = ttk.LabelFrame(parent, text="Action Settings")
        self.action_group.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.action_group.columnconfigure(1, weight=1)

        self.actions = {
            'Allow': ttk.BooleanVar(value=True),
            'Block': ttk.BooleanVar(value=True)
        }

        ttk.Label(self.action_group, text="Select actions:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        col = 1
        for action, var in self.actions.items():
            ttk.Checkbutton(self.action_group, text=action, variable=var).grid(row=0, column=col, padx=10, pady=10, sticky="w")
            col += 1

    def get_actions(self):
        return [var.get() for var in self.actions.values()]