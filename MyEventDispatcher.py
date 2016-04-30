from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy._event import EventDispatcher




class MyEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_change_screen')
        super(MyEventDispatcher, self).__init__(**kwargs)

    def on_change_screen(self, *args):
        pass