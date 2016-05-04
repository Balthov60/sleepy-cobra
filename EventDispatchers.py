from kivy.event import EventDispatcher


class LevelEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        """
        Instantiate the level event dispatcher with its custom property.
        :param kwargs:
        """
        self.register_event_type('on_level_completed')
        super(EventDispatcher, self).__init__(**kwargs)

    def on_level_completed(self, *args):
        """
        Required method.
        """
        pass
