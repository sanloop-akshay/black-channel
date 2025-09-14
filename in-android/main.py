from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.home import HomeScreen

class Home(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HomeScreen())

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Home(name="home"))
        return sm

if __name__ == "__main__":
    MyApp().run()
