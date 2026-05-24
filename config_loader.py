import json

class ConfigLoader:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
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
