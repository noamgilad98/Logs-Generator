import tkinter as tk
from tkinter import filedialog, Canvas
import ttkbootstrap as ttk
from logs_generator.backend.config_manager import ConfigManager
from logs_generator.backend.log_generator import LogGenerator
from logs_generator.frontend.log_settings_frame import LogSettingsFrame
from logs_generator.frontend.bytes_settings_frame import BytesSettingsFrame
from logs_generator.frontend.service_type_frame import ServiceTypeFrame
from logs_generator.frontend.action_settings_frame import ActionSettingsFrame
from logs_generator.frontend.destinations_settings_frame import DestinationsSettingsFrame
from logs_generator.frontend.users_settings_frame import UsersSettingsFrame
from logs_generator.frontend.devices_settings_frame import DevicesSettingsFrame
from logs_generator.frontend.categories_settings_frame import CategoriesSettingsFrame

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
        self.destinations_settings_frame = DestinationsSettingsFrame(self.frame, self.config_manager, self)
        self.users_settings_frame = UsersSettingsFrame(self.frame, self.config_manager, self)
        self.devices_settings_frame = DevicesSettingsFrame(self.frame, self.config_manager, self)
        self.categories_settings_frame = CategoriesSettingsFrame(self.frame, self.config_manager, self)

        generate_button = ttk.Button(self.frame, text="Generate Logs", command=self.generate_logs, style='primary.TButton')
        generate_button.grid(row=8, column=0, padx=10, pady=20, sticky="ew")

        change_dir_button = ttk.Button(self.frame, text="Save Logs In", command=self.set_directory, style='primary.TButton')
        change_dir_button.grid(row=9, column=0, padx=10, pady=20, sticky="ew")

    def set_directory(self):
        directory = filedialog.askdirectory(initialdir=self.config_manager.get('default_directory'), title="Select Folder")
        if directory:
            self.log_generator.config['default_directory'] = directory

    def generate_logs(self):
        entries = self.log_settings_frame.get_entries()
        log_count = entries[1]

        def validate_and_update(entry):
            val = int(entry.get())
            if val > log_count:
                entry.delete(0, tk.END)
                entry.insert(0, str(log_count))
            return int(entry.get())

        num_destinations = validate_and_update(self.destinations_settings_frame.num_entry)
        num_users = validate_and_update(self.users_settings_frame.num_entry)
        num_devices = validate_and_update(self.devices_settings_frame.num_entry)
        num_categories = validate_and_update(self.categories_settings_frame.num_entry)

        entries += self.bytes_settings_frame.get_entries()
        entries += [num_destinations] + self.destinations_settings_frame.get_entries()[1:]
        entries += [num_users] + self.users_settings_frame.get_entries()[1:]
        entries += [num_devices] + self.devices_settings_frame.get_entries()[1:]
        entries += [num_categories] + self.categories_settings_frame.get_entries()[1:]

        service_types = self.service_type_frame.get_service_types()
        actions = self.action_settings_frame.get_actions()

        self.log_generator.generate_logs(entries, service_types, actions)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_all_distributions(self):
        self.destinations_settings_frame.update_distribution()
        self.users_settings_frame.update_distribution()
        self.devices_settings_frame.update_distribution()
        self.categories_settings_frame.update_distribution()
