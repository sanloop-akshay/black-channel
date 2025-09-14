from kivy.uix.boxlayout import BoxLayout
from widgets.buttons import AppActionButton  
from core.actions import PopupAction, SocketConnectAction

class HomeScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=20, **kwargs)

        kill_action = PopupAction("Info", "Kill OS button pressed (placeholder).")
        self.add_widget(AppActionButton("Kill OS", kill_action))

        socket_action = SocketConnectAction("127.0.0.1", 8080, "Connection Test from Black Channel")
        self.add_widget(AppActionButton("Socket Connect", socket_action))
