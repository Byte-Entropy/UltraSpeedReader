import json
import os
import hashlib
import time
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial

class SettingsScreen(Screen):
    def get_user_data_dir(self):
        return App.get_running_app().user_data_dir

    def get_config_path(self):
        return os.path.join(self.get_user_data_dir(), 'config.json')

    def get_library_dir(self):
        # Create a 'library' folder if it doesn't exist
        lib_path = os.path.join(self.get_user_data_dir(), 'library')
        if not os.path.exists(lib_path):
            os.makedirs(lib_path)
        return lib_path

    def load_settings(self):
        # Load config or return default structure
        path = self.get_config_path()
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {'wpm': 260, 'history': []}

    def save_to_history(self, text, wpm, index=0):
        # 1. Load current history
        settings = self.load_settings()
        history = settings.get('history', [])
        
        # 2. Generate a unique ID for this text (hash of content) to detect duplicates
        text_id = hashlib.md5(text.encode('utf-8')).hexdigest()
        
        # 3. Save the actual text content to a .txt file
        filename = f"{text_id}.txt"
        file_path = os.path.join(self.get_library_dir(), filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)

        # 4. Update or Add entry in JSON
        # Check if this text already exists in history
        existing_entry = next((item for item in history if item['id'] == text_id), None)
        
        if existing_entry:
            # Update existing
            existing_entry['index'] = int(index)
            existing_entry['wpm'] = int(wpm)
            existing_entry['timestamp'] = time.time() # Update 'last read' time
            # Move to top of list
            history.remove(existing_entry)
            history.insert(0, existing_entry)
        else:
            # Create new
            new_entry = {
                'id': text_id,
                'filename': filename,
                'snippet': text[:30] + "...", # For display in menu
                'index': int(index),
                'wpm': int(wpm),
                'timestamp': time.time()
            }
            history.insert(0, new_entry)
            
        # 5. Trim history to N items (e.g., 5)
        MAX_HISTORY = 5
        if len(history) > MAX_HISTORY:
            # Optional: Delete the file of the removed item? 
            # For now, let's just remove from the list
            history = history[:MAX_HISTORY]

        settings['history'] = history
        settings['wpm'] = int(wpm) # Save global WPM preference too

        with open(self.get_config_path(), 'w') as f:
            json.dump(settings, f)
            
        return text_id

    def delete_history_item(self, item_id):
        settings = self.load_settings()
        history = settings.get('history', [])
        
        # Find item to remove file
        item = next((i for i in history if i['id'] == item_id), None)
        if item:
            # Try to delete the .txt file
            try:
                os.remove(os.path.join(self.get_library_dir(), item['filename']))
            except OSError:
                pass # File might already be gone
            
            history.remove(item)
            settings['history'] = history
            with open(self.get_config_path(), 'w') as f:
                json.dump(settings, f)
            
            # Refresh the UI list
            self.populate_history_list()

    def on_start_button(self):
        text = self.ids.user_input.text
        if not text.strip():
            return 

        try:
            wpm = self.ids.wpm_input.text
        except:
            wpm = 260
            
        # 1. Check if text exists to get resume index
        current_index = 0
        text_id = hashlib.md5(text.encode('utf-8')).hexdigest()
        settings = self.load_settings()
        history = settings.get('history', [])
        # Check if already in history
        existing = next((i for i in history if i['id'] == text_id), None)
        
        if existing:
            current_index = existing['index']
            # Only update WPM in the record
            self.save_to_history(text, wpm, current_index)
        else:
            # New entry
            self.save_to_history(text, wpm, 0)

        # Pass control to main app
        app = App.get_running_app()
        app.root.get_screen('reader').setup_reader(text, wpm, start_index=current_index)
        app.root.current = 'reader'

    def on_enter(self):
        # Called when screen is displayed
        self.populate_history_list()

    def populate_history_list(self):
        # Clear existing widgets in the scrollview container
        container = self.ids.history_container
        container.clear_widgets()
        
        settings = self.load_settings()
        history = settings.get('history', [])
        
        for item in history:
            # Create a row for each item
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            
            # Button to load the text
            lbl = f"{item['snippet']} (idx: {item['index']})"
            btn = Button(text=lbl, size_hint_x=0.8)
            btn.bind(on_release=partial(self.load_history_item, item))
            
            # Button to delete
            del_btn = Button(text="X", size_hint_x=0.2, background_color=(1, 0, 0, 1))
            del_btn.bind(on_release=partial(self.lambda_delete, item['id']))

            row.add_widget(btn)
            row.add_widget(del_btn)
            container.add_widget(row)

    def lambda_delete(self, item_id, instance):
        self.delete_history_item(item_id)

    def load_history_item(self, item, instance):
        # Load text from file
        try:
            with open(os.path.join(self.get_library_dir(), item['filename']), 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.ids.user_input.text = content
            self.ids.wpm_input.text = str(item['wpm'])
        except FileNotFoundError:
            # Handle error
            pass
            
    # Keep default create/exit methods...
    def create_default_config(self):
        default_config = {'wpm': 260, 'history': []}
        with open(self.get_config_path(), 'w') as f:
            json.dump(default_config, f)
            
    def on_exit_button(self):
        App.get_running_app().stop()