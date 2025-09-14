from kivy.uix.button import Button
from core.interfaces import IAction

class AppActionButton(Button):   

    def __init__(self, action_name: str, action: IAction, **kwargs):
        super().__init__(**kwargs)
        self.text = action_name
        self.size_hint = (0.5, 0.2)
        self.pos_hint = {"center_x": 0.5}
        self._action = action
        self.bind(on_press=self._on_press)

    def _on_press(self, instance):
        if isinstance(self._action, IAction):
            self._action.execute()
