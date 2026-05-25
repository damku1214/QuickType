import logging
from pynput import keyboard
from config_loader import ConfigLoader
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)

class ShortcutExpander:
    def __init__(self):
        self.buffer = ""
        self.config_loader = ConfigLoader(str(Path(os.environ.get('LOCALAPPDATA', '.')) / 'QuickType' / 'config.json'))
        self.trigger_character = self.config_loader.trigger_character
        self.shortcuts = self.config_loader.shortcuts
        self.is_listening = False
        self.keyboard_controller = keyboard.Controller()
        self.cancel_keys = {keyboard.Key.tab, keyboard.Key.esc}

        with keyboard.Listener(on_press=self.handle_press) as listener:
            listener.join()

    def handle_press(self, key):
        try:
            if hasattr(key, 'char') and key.char == self.trigger_character:
                self.toggle_listening()
            elif self.is_listening:
                self.process_input(key)
        except Exception as e:
            logging.error(f"Error handling key press: {e}")

    def toggle_listening(self):
        if self.is_listening:
            self.expand_shortcut()
        else:
            self.is_listening = True
            self.buffer = self.trigger_character

    def process_input(self, key):
        if hasattr(key, 'char'):
            self.buffer += key.char
        elif key == keyboard.Key.backspace:
            self.buffer = self.buffer[:-1]
        elif key in self.cancel_keys:
            self.reset_state()

    def reset_state(self):
        self.buffer = ""
        self.is_listening = False

    def expand_shortcut(self):
        self.buffer += self.trigger_character
        shortcut_name = self.buffer[1:-1]

        if shortcut_name not in self.shortcuts:
            self.reset_state()
            return

        expansion_text = self.shortcuts[shortcut_name]

        for _ in range(len(self.buffer)):
            self.keyboard_controller.tap(keyboard.Key.backspace)

        self.keyboard_controller.release(keyboard.Key.shift)
        self.keyboard_controller.release(keyboard.Key.shift_r)

        self.keyboard_controller.type(expansion_text)

        self.reset_state()

if __name__ == "__main__":
    ShortcutExpander()
