from __future__ import division             # Pour que les divisions retournent des flotants.

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.logger import Logger

import datetime
import re
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
        self.map_height = int
        self.map_width = int
        self.map_size = int
        self.map_matrix = list

        self.points = list()

        self.textures = textures
        self.textures_size = 256
        self.window = Window

        self.tile_size = int
        self.vectical_padding = int
        self.horizontal_padding = int

        is_file = os.path.isfile(map_file_path)
        if not is_file:
            raise ValueError("File given does not exist.")

        is_cfg = map_file_path.lower().endswith('.cfg')

        if is_cfg:
            self.parse_pipe_delimited_file(map_file_path)

        else:
           raise ValueError("File given is not valid for use.")

        self.update_drawing_instructions()

        Window.bind(on_resize=self.update_drawing_instructions)

    def get_texture(self, token):
        """
        Retourne les textures compatible selon le dictionnaire de textures.
        :param token: {str} lettre
        :return: {CoreImage.texture} texture
        """
        try:
            texture = self.textures[token]
        except KeyError as error:
            raise KeyError("Texture ", token, " doesn't exist :", error)

        return texture

    def parse_pipe_delimited_file(self, map_file_path):

        map_file = str

        try:
            map_file = open(map_file_path)

            pipe = "|"
            start_and_stop = re.compile(r',*', re.UNICODE)
            comment = re.compile(r'#.*', re.UNICODE)

            self.map_matrix = []

            y = 0
            for line in map_file:
                cleaned_line = comment.sub('', line).strip()
                if cleaned_line:
                    self.map_matrix.append([])
                    x_values = cleaned_line.split(pipe)
                    x = 0
                    for x_value in x_values:
                        texture = self.get_texture(x_value)
                        self.map_matrix[y].append({'texture': texture, 'type': x_value})
                        x += 1
                    self.map_width = x
                    y += 1
                    if x > self.map_width:
                        self.map_width = x
                indication = start_and_stop.split(line.replace('#', ''))
                if len(indication) == 2:
                    self.points.append((int(indication[1]), int(indication[0])))

            self.map_height = y

            self.map_size = (self.map_width, self.map_height)

            if self.map_width <= 0 or self.map_height <= 0 or not self.points:
                raise ValueError("Pipe delimited file given is not valid for use.")

        finally:
            map_file.close()

    def update_drawing_instructions(self, *args):
        """
        Met a jour les instructions de dessins du canvas du widget lorsque la fenetre est change de taille.
        :param args: Window.on_resize arguments
        """
        Logger.info("Adding drawing instructions")
        window_width, window_height = Window.size
        min_window_size = min(Window.size)
        size_needed_width = self.map_width * self.textures_size
        size_needed_height = self.map_height * self.textures_size
        size_needed_max = max(size_needed_width, size_needed_height)
        scaling_factor = size_needed_max / min_window_size
        self.tile_size = self.textures_size / scaling_factor
        self.vectical_padding = (window_width - size_needed_width / scaling_factor) / 2
        self.horizontal_padding = (window_height - size_needed_height / scaling_factor) / 2

        self.canvas.before.clear()
        self.canvas.clear()
        self.canvas.after.clear()

        start_time = datetime.datetime.now()

        for y in range(0, len(self.map_matrix)):
            for x in range(0, len(self.map_matrix[y])):
                x_position = (x * self.tile_size) + self.vectical_padding
                # y + 1 car avec y == 0 cela ne s'afficherait pas
                y_position = window_height - ((y + 1) * self.tile_size) - self.horizontal_padding
                position = (x_position, y_position)
                tile_size_tuple = [self.tile_size] * 2
                texture = self.map_matrix[y][x]['texture']

                self.canvas.before.add(Color(0.37, 0.37, 0.37, 1) if (x + y) % 2 else Color(0.19, 0.19, 0.19, 1))
                self.canvas.before.add(Rectangle(size=tile_size_tuple, pos=position))
                self.canvas.add(Color(None))

                if (y, x) in self.points:
                    point_texture = self.textures['point']
                    self.canvas.add(Rectangle(size=tile_size_tuple, texture=point_texture, pos=position))
                self.canvas.add(Rectangle(size=tile_size_tuple, texture=texture, pos=position))

        end_time = datetime.datetime.now()
        duration = end_time - start_time
        duration_seconds = duration.microseconds * 10**-6
        Logger.info("Drawing instruction added in %fs" % duration_seconds)
