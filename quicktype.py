from pynput import keyboard
from config_loader import ConfigLoader
import clipboard
import sys

# Note that Claude Code (Gemini) changed many variable and function names for clarity.
# However, no functionality has changed since before the reformatting - if AI generated a new block of code,
# I will add a comment as so.

class QuickType:
    ## Initializes all variables to start
    def __init__(self):
        self.__buffer = ""
        self.__config_loader = ConfigLoader()
        self.__trigger_character = self.__config_loader.get_trigger_char()
        self.__reload_character = self.__config_loader.get_reload_char()
        self.__shortcuts = self.__config_loader.get_shortcuts()
        self.__is_listening = False
        self.__keyboard_controller = keyboard.Controller()
        self.__cancel_keys = {keyboard.Key.tab, keyboard.Key.esc}

        with keyboard.Listener(on_press=self.handle_press) as listener:
            listener.join()

    ## Runs every keystroke, runs other methods depending on key pressed
    def handle_press(self, key):
        # hasattr() suggested by Gemini instead of using .isalpha() and .isalnum()
        if hasattr(key, 'char') and key.char == self.__trigger_character:
            self.toggle_listening()
        elif hasattr(key, 'char') and key.char == self.__reload_character:
            # Reload all entries from config.json
            self.__config_loader.load()
            self.__trigger_character = self.__config_loader.get_trigger_char()
            self.__reload_character = self.__config_loader.get_reload_char()
            self.__shortcuts = self.__config_loader.get_shortcuts()
        elif self.__is_listening:
            self.process_input(key)

    ## Toggles listening state - expand the shortcut if it was previously listening and now not listening
    def toggle_listening(self):
        if self.__is_listening:
            self.expand_shortcut()
        else:
            self.__is_listening = True
            self.__buffer = self.__trigger_character

    ## Runs every keystroke ONLY when app is listening
    def process_input(self, key):
        if hasattr(key, 'char'):
            self.__buffer += key.char
        elif key == keyboard.Key.backspace:
            self.__buffer = self.__buffer[:-1]
        elif key in self.__cancel_keys:
            self.reset_state()

    ## Turns off listening without triggering shortcut completion checks
    def reset_state(self):
        self.__buffer = ""
        self.__is_listening = False

    def expand_shortcut(self):
        self.__buffer += self.__trigger_character
        shortcut_name = self.__buffer[1:-1]

        # Cancel method if current input was not found in config.json
        if shortcut_name not in self.__shortcuts:
            self.reset_state()
            return

        # Fetches output text from the shortcuts dict
        expansion_text = self.__shortcuts[shortcut_name]

        # Delete all input so far
        for _ in range(len(self.__buffer)):
            self.__keyboard_controller.tap(keyboard.Key.backspace)

        # Releases all shift keys so that the output is not all in caps
        self.__keyboard_controller.release(keyboard.Key.shift)
        self.__keyboard_controller.release(keyboard.Key.shift_r)

        clipboard.copy(expansion_text)

        # sys.platform check found on the internet - checks if OS is mac or windows and
        # presses diff keys respectively
        if sys.platform == "darwin":
            self.keyboard_controller.press(keyboard.Key.cmd)
        else:
            self.__keyboard_controller.press(keyboard.Key.ctrl)
        
        self.__keyboard_controller.press("v")
        self.__keyboard_controller.release("v")
        
        if sys.platform == "darwin":
            self.__keyboard_controller.release(keyboard.Key.cmd)
        else:
            self.__keyboard_controller.release(keyboard.Key.ctrl)

        self.reset_state()


if __name__ == "__main__":
    # Create a QuickType class, initiating everything
    quick_type = QuickType()
