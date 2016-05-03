from kivy.event import EventDispatcher


class LevelEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_level_completed')
        super(EventDispatcher, self).__init__(**kwargs)

    def on_level_completed(self, *args):
        pass
