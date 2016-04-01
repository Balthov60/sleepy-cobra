from kivy.uix.relativelayout import RelativeLayout


class Menu(RelativeLayout):
    def __init__(self, **kwargs):
        """
        Le menu.
        :param kwargs: Arguments du Layout
        """
        super(Menu, self).__init__(**kwargs)
