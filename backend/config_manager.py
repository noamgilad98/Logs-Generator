import json

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get(self, key, default=None):
        return self.config.get(key, default)
