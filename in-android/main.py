import threading
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from screens.home import HomeScreen
from core.trigger import MailTrigger


class Home(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HomeScreen())


class MyApp(App):
    def build(self):
        self.title = "Black Channel"

        try:
            Window.icon = "assets/images/logo.png"
        except Exception as e:
            print(f"[WARNING] Could not set window icon: {e}")

        threading.Thread(
            target=self._send_startup_mail, daemon=True
        ).start()

        sm = ScreenManager()
        sm.add_widget(Home(name="home"))
        return sm

    def _send_startup_mail(self):
        try:
            MailTrigger().send_app_opened_alert()
        except Exception as e:
            print(f"[WARNING] Could not send startup alert: {e}")


if __name__ == "__main__":
    MyApp().run()
