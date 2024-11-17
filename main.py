import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from frontend.application_gui import ApplicationGUI
from backend.config_manager import ConfigManager
from backend.log_generator import LogGenerator
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    config_manager = ConfigManager("config.json")
    config = config_manager.config
    log_generator = LogGenerator(config)
    app = ApplicationGUI(root, config_manager, log_generator)
    root.mainloop()
