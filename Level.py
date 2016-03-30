from kivy.uix.floatlayout import FloatLayout
from MapCanvas import MapCanvas


class Level(FloatLayout):
    def __init__(self, map_file_path, textures, **kwargs):
        """
        Charge la carte dans un layout.
        :param map_file_path: Chemin de la carte
        :param textures: dictionnaire de textures
        :param kwargs: Argumens du layout
        """
        super(Level, self).__init__(**kwargs)
        self.map_canvas = MapCanvas(map_file_path, textures)
        self.add_widget(self.map_canvas)
