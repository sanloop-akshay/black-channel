from kivy.uix.popup import Popup
from kivy.uix.label import Label
import socket
from .interfaces import IAction

class PopupAction(IAction):

    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message

    def execute(self):
        popup = Popup(
            title=self.title,
            content=Label(text=self.message),
            size_hint=(0.6, 0.4)
        )
        popup.open()


class SocketConnectAction(IAction):

    def __init__(self, host: str, port: int, message: str):
        self.host = host
        self.port = port
        self.message = message

    def execute(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.sendall(self.message.encode("utf-8"))
            s.close()
            PopupAction("Success", f"Connected to {self.host}:{self.port}").execute()
        except Exception as e:
            PopupAction("Error", f"Connection failed: {e}").execute()
