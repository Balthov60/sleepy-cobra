from __future__ import division             # Pour que les divisions retournent des flotants.

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.logger import Logger

import datetime
import Image
import os


class MapCanvas(Widget):

    def __init__(self, map_file_path, textures, **kwargs):
        """
        Charge et donne les instructions de constructions de la carte.
        :param map_file_path: {string} chemin vers le fichier de la carte
        :param textures: {dict} dictionnaire des textures
        :param kwargs: Arguments du widget
        """
        super(MapCanvas, self).__init__(**kwargs)
        self.map_height = None
        self.map_width = None
        self.map_size = None
        self.map_matrix = None
        self.textures = textures
        self.textures_size = 256

        is_file = os.path.isfile(map_file_path)
        if not is_file:
            raise ValueError("File given does not exist.")
        is_png = map_file_path.lower().endswith('.png')
        is_cfg = map_file_path.lower().endswith('.cfg')
        if is_png:
            self.parse_png_map(map_file_path)
        elif is_cfg:
            self.parse_pipe_delimited_file(map_file_path)
        else:
            raise ValueError("Image given is not valid for use.")

        self.update_drawing_instructions()

        Window.bind(on_resize=self.update_drawing_instructions)

    def get_texture(self, token):
        """
        Retourne les textures compatible selon le dictionnaire de textures.
        :param token: {tuple} rouge, vert, bleu ou {str} lettre
        :return: {CoreImage.texture} texture
        """
        try:
            texture = self.textures[token]
        except KeyError, error:
            raise KeyError("Texture ", token, " doesn't exist :", error)

        return texture

    def parse_png_map(self, map_file_path):
        map_file = Image.open(map_file_path)

        self.map_size = map_file.size
        self.map_width = self.map_size[0]
        self.map_height = self.map_size[1]

        if self.map_width <= 0 or self.map_height <= 0:
            raise ValueError("Image given is not valid for use.")

        self.map_matrix = [[0 for _ in range(0, self.map_width)] for _ in range(0, self.map_height)]

        pixels_matrix = map_file.load()

        for y in range(0, self.map_width):
            for x in range(0, self.map_width):
                rgb = pixels_matrix[x, y]
                texture = self.get_texture(rgb)
                self.map_matrix[y][x] = texture

    def parse_pipe_delimited_file(self, map_file_path):

        pipe = '|'

        map_file = open(map_file_path)
        self.map_width = map_file.readline().count(pipe) + 1
        map_file.seek(0)  # Revient a la premiere ligne du fichier.
        self.map_height = sum(1 for line in map_file if line)
        self.map_size = (self.map_width, self.map_height)

        if self.map_width <= 0 or self.map_height <= 0:
            raise ValueError("Pipe delimited file given is not valid for use.")

        self.map_matrix = [[0 for _ in range(0, self.map_width)] for _ in range(0, self.map_height)]

        map_file.seek(0)                # Get to the first line of file.

        y_index = 0
        for line in map_file:
            x_values = line.split(pipe)
            x_index = 0
            for x_value in x_values:
                texture = self.get_texture(x_value.strip())
                self.map_matrix[y_index][x_index] = texture
                x_index += 1
            y_index += 1

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
        scaling_factor = size_needed / min_window_size
        tile_size = self.textures_size / scaling_factor
        padding_left = (window_width - size_needed / scaling_factor) / 2
        padding_top = (window_height - size_needed / scaling_factor) / 2

        self.canvas.clear()

        start_time = datetime.datetime.now()

        for y in range(0, len(self.map_matrix)):
            for x in range(0, len(self.map_matrix[y])):
                x_position = (x * tile_size) + padding_left
                # y + 1 car avec y == 0 cela ne s'afficherait pas
                y_position = window_height - ((y + 1) * tile_size) - padding_top
                position = (x_position, y_position)
                tile_size_tuple = [tile_size] * 2
                texture = self.map_matrix[y][x]
                self.canvas.add(Rectangle(size=tile_size_tuple, texture=texture, pos=position))

        end_time = datetime.datetime.now()
        duration = end_time - start_time
        duration_seconds = duration.microseconds * 10**-6
        Logger.info("Drawing instruction added in %fs" % duration_seconds)
