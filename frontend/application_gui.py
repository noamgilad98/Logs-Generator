import tkinter as tk
from tkinter import filedialog, Canvas
import ttkbootstrap as ttk
from logs_generator.backend.config_manager import ConfigManager
from logs_generator.backend.log_generator import LogGenerator
from logs_generator.frontend.log_settings_frame import LogSettingsFrame
from logs_generator.frontend.bytes_settings_frame import BytesSettingsFrame
from logs_generator.frontend.service_type_frame import ServiceTypeFrame
from logs_generator.frontend.action_settings_frame import ActionSettingsFrame
from logs_generator.utils.distribution_settings_frame import DistributionSettingsFrame

class ApplicationGUI:
    def __init__(self, root, config_manager, log_generator):
        self.root = root
        self.config_manager = config_manager
        self.log_generator = log_generator
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Advanced Log Generator")
        self.root.geometry("660x700")
        self.root.configure(bg="#ffffff")

        style = ttk.Style(theme='litera')
        style.configure('TLabel', font=('Segoe UI', 12))
        style.configure('TButton', font=('Segoe UI', 12))
        style.configure('TEntry', font=('Segoe UI', 12))
        style.configure('TCheckbutton', font=('Segoe UI', 12))
        style.configure('TCombobox', font=('Segoe UI', 12))
        style.configure('TFrame')
        style.configure('TLabelFrame', font=('Segoe UI', 12), relief=tk.GROOVE)

        self.canvas = Canvas(self.root, background="#ffffff")
        self.scroll_y = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.log_settings_frame = LogSettingsFrame(self.frame, self.config_manager, self)
        self.bytes_settings_frame = BytesSettingsFrame(self.frame, self.config_manager, self)
        self.service_type_frame = ServiceTypeFrame(self.frame)
        self.action_settings_frame = ActionSettingsFrame(self.frame)
        self.destinations_settings_frame = DistributionSettingsFrame(self.frame, self.config_manager, self, "Destinations", 'distinct_destinations_default', 5)
        self.users_settings_frame = DistributionSettingsFrame(self.frame, self.config_manager, self, "Users", 'distinct_users_default', 100)
        self.devices_settings_frame = DistributionSettingsFrame(self.frame, self.config_manager, self, "Devices", 'distinct_devices_default', 50)
        self.categories_settings_frame = DistributionSettingsFrame(self.frame, self.config_manager, self, "Categories", 'distinct_categories_default', 10)

        self.log_settings_frame.frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.bytes_settings_frame.frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.service_type_frame.frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.action_settings_frame.frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.destinations_settings_frame.frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.users_settings_frame.frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        self.devices_settings_frame.frame.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
        self.categories_settings_frame.frame.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        generate_button = ttk.Button(self.frame, text="Generate Logs", command=self.generate_logs, style='primary.TButton')
        generate_button.grid(row=10, column=0, padx=10, pady=20, sticky="ew")

        change_dir_button = ttk.Button(self.frame, text="Save Logs In", command=self.set_directory, style='primary.TButton')
        change_dir_button.grid(row=11, column=0, padx=10, pady=20, sticky="ew")

    def set_directory(self):
        directory = filedialog.askdirectory(initialdir=self.config_manager.get('default_directory'), title="Select Folder")
        if directory:
            self.log_generator.config['default_directory'] = directory

    def generate_logs(self):
        entries = self.log_settings_frame.get_entries()
        entries += self.bytes_settings_frame.get_entries()
        service_types = self.service_type_frame.get_service_types()
        actions = self.action_settings_frame.get_actions()
        num_destinations, dist_type_dest = self.destinations_settings_frame.get_entries()
        num_users, dist_type_user = self.users_settings_frame.get_entries()
        num_devices, dist_type_device = self.devices_settings_frame.get_entries()
        num_categories, dist_type_category = self.categories_settings_frame.get_entries()

        self.log_generator.generate_logs(entries, service_types, actions, num_destinations, dist_type_dest, num_users, dist_type_user, num_devices, dist_type_device, num_categories, dist_type_category)

    def update_all_distributions(self):
        self.destinations_settings_frame.update_distribution(None)
        self.users_settings_frame.update_distribution(None)
        self.devices_settings_frame.update_distribution(None)
        self.categories_settings_frame.update_distribution(None)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

if __name__ == "__main__":
    root = tk.Tk()
    config_manager = ConfigManager("config.json")
    config = config_manager.config
    log_generator = LogGenerator(config)
    app = ApplicationGUI(root, config_manager, log_generator)
    root.mainloop()
