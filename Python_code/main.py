from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from UserSettings import SettingsScreen
from visualizer import ReaderScreen

class SpeedReadApp(App):
    def build(self):
        #Builder.load_file('speedread.kv')
        
        sm = ScreenManager()
        
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(ReaderScreen(name='reader'))
        
        return sm

if __name__ == '__main__':
    SpeedReadApp().run()