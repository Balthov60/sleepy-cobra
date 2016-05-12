from kivy.event import EventDispatcher


class LevelEventDispatcher(EventDispatcher):
    """
    Dispatch Level Event (Level completed).
    """
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
    """
    Dispatch Menu Event (Change screen).
    """
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


def propagate_event(value, current_class, set_id=None):
    """
    Propagate change screen event.

    :param value: screen's name.
    :param current_class: Current active class.
    :param set_id: current ID set.
    :rtype: void
    """
    current_class.event_dispatcher.dispatch('on_change_screen', value, set_id)
