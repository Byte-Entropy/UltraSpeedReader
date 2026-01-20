from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import StringProperty

class ReaderScreen(Screen):
    display_text = StringProperty("")

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

        Clock.schedule_once(self.start_loop, 3) # 3 sec buffer
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