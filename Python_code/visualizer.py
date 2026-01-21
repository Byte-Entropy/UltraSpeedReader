from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty

class ReaderScreen(Screen):
    display_text = StringProperty("")
    pause_button_text = StringProperty("Pause")
    is_paused = BooleanProperty(False)

    def setup_reader(self, text, wpm):
        # Stop any existing clocks
        Clock.unschedule(self.update_text)
        Clock.unschedule(self.start_loop)

        # Cast wpm string to int and calculate delay
        delay = 60.0 / int(wpm)
        self.words = text.split()
        self.index = 0
        
        # Reset display and start the clock
        self.display_text = "Get Ready..."
        
        # Change after UserSettings json save/load fix
        countdown_time = 3
        Clock.schedule_once(self.start_loop, countdown_time) # 3 sec buffer with countdown
        for i in range(countdown_time, 0, -1):
            self.display_text = f"Starting in {i}..."
            Clock.schedule_once(lambda dt: None, 1)  # Wait 1 second

        self.wpm_delay = delay

    def start_loop(self, dt):
        Clock.schedule_interval(self.update_text, self.wpm_delay)

    def update_text(self, dt):
        if self.index < len(self.words):
            self.display_text = self.words[self.index]
            self.index += 1
        else:
            self.display_text = "Done!"
            return False  # Stop the clock

    def on_exit_button(self):
        App.get_running_app().stop()

    def on_pause_button(self):
        if not self.is_paused:
            Clock.unschedule(self.update_text)
            self.display_text = "Paused. Press Start to continue."
            self.is_paused = True
            self.pause_button_text = "Start"

        elif self.is_paused:
            self.is_paused = False
            Clock.schedule_interval(self.update_text, self.wpm_delay)
            self.pause_button_text = "Pause"
        else:
            pass  # Should not reach here

    def on_stop_button(self):
        Clock.unschedule(self.update_text)
        Clock.unschedule(self.start_loop)
        
    def on_speed_change(self, new_wpm):
        # Adjust speed on the fly
        Clock.unschedule(self.update_text)
        self.wpm_delay = 60.0 / int(new_wpm)
        Clock.schedule_interval(self.update_text, self.wpm_delay)