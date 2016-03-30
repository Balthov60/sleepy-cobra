from __future__ import division             # Pour que les divisions retournent des flotants.
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.logger import Logger
import datetime
from PIL import Image
import os


class MapCanvas(Widget):

    def __init__(self, map_file_path, textures, **kwargs):
        """
        Charge et donnes les instructions de constructions de la carte.
        :param map_file_path: {string} chemin vers le fichier de la carte
        :param textures: {dict} dictionnaire des textures
        :param kwargs: Arguments du widget
        """
        super(MapCanvas, self).__init__(**kwargs)
        is_file = os.path.isfile(map_file_path)
        if not is_file:
            raise ValueError("File given does not exist.")
        is_png = map_file_path.lower().endswith('.png')
        if not is_png:
            raise ValueError("File given is not a png image.")

        self.map = Image.open(map_file_path)

        self.map_size = self.map.size
        self.map_width = self.map_size[0]
        self.map_height = self.map_size[1]

        if self.map_width <= 0 or self.map_height <= 0:
            raise ValueError("Image given is not valid for use.")

        self.textures = textures
        self.textures_size = 256
        self.scaling_factor = None
        self.tile_size = None
        self.pixels_matrix = self.map.load()

        self.update_drawing_instructions()

        Window.bind(on_resize=self.update_drawing_instructions)

    def update_drawing_instructions(self, *args):
        """
        Met a jour les instructions de dessins du canvas du widget lorsque la fenetre est change de taille.
        :param args: Window.on_resize arguments
        """
        Logger.info("Adding drawing instructions")
        window_width, window_height = Window.size
        min_window_size = min(Window.size)
        min_map_size = min(self.map_size)
        size_needed = min_map_size * self.textures_size
        self.scaling_factor = size_needed / min_window_size
        self.tile_size = self.textures_size / self.scaling_factor
        self.canvas.clear()
        padding_left = (Window.width - size_needed / self.scaling_factor) / 2
        padding_top = (Window.height - size_needed / self.scaling_factor) / 2

        start_time = datetime.datetime.now()
        for y in range(0, self.map_width):
            for x in range(0, self.map_width):
                rgb = self.pixels_matrix[x, y]
                texture = self.get_texture(rgb)
                x_position = (x * self.tile_size) + padding_left
                # y + 1 car avec y == 0 cela ne s'afficherait pas
                y_position = window_height - ((y + 1) * self.tile_size - padding_top)
                position = (x_position, y_position)
                tile_size = [self.tile_size] * 2
                self.canvas.add(Rectangle(size=tile_size, texture=texture, pos=position))

        end_time = datetime.datetime.now()
        duration = end_time - start_time
        duration_seconds = duration.microseconds * 10**-6
        Logger.info("Drawing instruction added in %fs" % duration_seconds)

    def get_texture(self, rgb):
        """
        Retourne les textures compatible selon le dictionnaire de textures.
        :param rgb: {tuple} rouge, vert, bleu
        :return: {CoreImage.texture} texture
        """
        try:
            texture = self.textures[rgb]
        except KeyError, error:
            raise KeyError("Texture ", rgb, " doesn't exist :", error)

        return texture
