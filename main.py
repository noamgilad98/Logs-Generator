import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logs_generator.frontend.application_gui import ApplicationGUI
from logs_generator.backend.config_manager import ConfigManager
from logs_generator.backend.log_generator import LogGenerator
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    config_manager = ConfigManager("config.json")
    config = config_manager.config
    log_generator = LogGenerator(config)
    app = ApplicationGUI(root, config_manager, log_generator)
    root.mainloop()
