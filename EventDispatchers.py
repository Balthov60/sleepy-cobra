from kivy.event import EventDispatcher


class LevelEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        """
        Instantiate the level event dispatcher with its custom property.

        :param kwargs:
        :rtype: void
        """
        self.register_event_type('on_level_completed')
        super(EventDispatcher, self).__init__(**kwargs)

    @staticmethod
    def on_level_completed(*args):
        """
        Required method.
        """
        pass


class MenusEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        """
        Instantiate the Menu event dispatcher with its custom property.

        :param kwargs:
        :rtype: void
        """
        self.register_event_type('on_change_screen')
        super(MenusEventDispatcher, self).__init__(**kwargs)

    @staticmethod
    def on_change_screen(*args):
        """
        Required method
        """
        pass
