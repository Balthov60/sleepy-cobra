from kivy.uix.widget import Widget

from Level import Level
from LevelService import LevelService
from EventDispatchers import LevelEventDispatcher


class LevelManager(Widget):

    def __init__(self, **kwargs):
        """
        Instantiate the LevelManager with event listener.
        :param kwargs:
        """
        super(LevelManager, self).__init__(**kwargs)
        self.level_service = LevelService()
        self.level_event_dispatcher = LevelEventDispatcher()
        self.level_event_dispatcher.bind(on_level_completed=self.do_level_up)

    def add_widget(self, widget, index=0):
        """
        Add widget only after removing any widget previously present.
        :param widget:
        :param index:
        :return:
        """
        self.clear_widgets()
        super(LevelManager, self).add_widget(widget, index)

    def do_level_up(self, instance, completion_details, *args):
        """
        Save advancement and level up the player loading next level.
        :param instance:
        :param completion_details:
        :param args:
        :return:
        """
        self.level_service.save_completion(completion_details)
        self.load_level(self.level_service.get_next_level_id(completion_details['level_id']))

    def load_resuming_level(self):
        """
        Load resuming level.
        :return:
        """
        level_id = self.level_service.get_resuming_level()
        self.add_widget(Level(self.level_event_dispatcher, level_id))

    def load_level(self, level_id=None):
        """
        Load given level with checking.
        :param level_id:
        :return:
        """

        if not level_id:
            return self.load_resuming_level()

        if not self.level_service.is_level_playable(level_id):
            return

        if not self.level_service.does_level_exist(level_id):
            return

        return self.add_widget(Level(self.level_event_dispatcher, level_id))
