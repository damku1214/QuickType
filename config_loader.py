import json
import os
from pathlib import Path

class ConfigLoader:
    def __init__(self, config_file_path):
        self.app_data_path = Path(os.environ.get('LOCALAPPDATA', '.')) / 'QuickType' / 'config.json'

        if os.path.exists(config_file_path):
            self.config_file_path = config_file_path
        else:
            self.app_data_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_file_path = str(self.app_data_path)
            if not os.path.exists(self.config_file_path):
                # Copy existing or create default
                with open(self.config_file_path, "w", encoding='utf-8') as f:
                    json.dump({"trigger_character": ":", "shortcuts": {}}, f, indent=4)

        self.trigger_character = ":"
        self.shortcuts = {}
        self.load()

    def load(self):
        with open(self.config_file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
            self.trigger_character = data.get("trigger_character", ":")
            self.shortcuts = data.get("shortcuts", {})

    def save(self):
        with open(self.config_file_path, "w", encoding='utf-8') as file:
            json.dump({
                "trigger_character": self.trigger_character,
                "shortcuts": self.shortcuts
            }, file, indent=4)
