import json
import os
from kivy.app import App
from kivy.uix.screenmanager import Screen

class SettingsScreen(Screen):
    def get_config_path(self):
        # Gets the writable path for this app (Android/Win compatible)
        app_dir = App.get_running_app().user_data_dir
        return os.path.join(app_dir, 'config.json')

    def save_settings(self, wpm_value):
        config_data = {'wpm': int(wpm_value)}
        with open(self.get_config_path(), 'w') as f:
            json.dump(config_data, f)

    def load_settings(self):
        path = self.get_config_path()
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {'wpm': 300} # Default fallback

    def on_start_button(self):
        try:
            wpm = self.ids.wpm_input.text
            self.save_settings(wpm)
        except (ValueError, TypeError):
            wpm = 260  # Fallback to default if conversion fails

        if not wpm.isdigit() or int(wpm) <= 0:
            wpm = 260  # Fallback to default if invalid input

        # Pass control to the main app to switch screens
        app = App.get_running_app()
        app.root.get_screen('reader').setup_reader(self.ids.user_input.text, wpm)
        app.root.current = 'reader'

    def on_exit_button(self):
        App.get_running_app().stop()
