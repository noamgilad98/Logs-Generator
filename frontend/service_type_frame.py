import ttkbootstrap as ttk

class ServiceTypeFrame:
    def __init__(self, parent):
        self.service_type_group = ttk.LabelFrame(parent, text="Service Type Settings")
        self.service_type_group.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.service_type_group.columnconfigure(1, weight=1)

        self.service_types = {
            'Private': ttk.BooleanVar(value=True),
            'M365': ttk.BooleanVar(value=True),
            'Internet': ttk.BooleanVar(value=True)
        }

        ttk.Label(self.service_type_group, text="Select service types:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        col = 1
        for service, var in self.service_types.items():
            ttk.Checkbutton(self.service_type_group, text=service, variable=var).grid(row=0, column=col, padx=10, pady=10, sticky="w")
            col += 1

    def get_service_types(self):
        return [var.get() for var in self.service_types.values()]
