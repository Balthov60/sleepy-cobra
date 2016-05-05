from kivy._event import EventDispatcher


class MenusEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        """

        :param kwargs:
        :rtype: void
        """
        self.register_event_type('on_change_screen')
        super(MenusEventDispatcher, self).__init__(**kwargs)

    def on_change_screen(self, *args):
        """

        :param args:
        :rtype: void
        """
        pass
