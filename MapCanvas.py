"""
MapCanvas
"""
from __future__ import division  # So that diving return floating

from datetime import datetime
import re
import os

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.logger import Logger

from Configurations import TEXTURES


class MapCanvas(Widget):
    """
    Interpret config for map and put the maps in a canvas
    """

    textures = TEXTURES
    textures_size = 256

    def __init__(self, map_file_path, **kwargs):
        """
        Charge et donne les instructions de constructions de la carte.

        :param map_file_path: {string} chemin vers le fichier de la carte
        :param textures: {dict} dictionnaire des textures
        :param kwargs: Arguments du widget
        :rtype: void
        """
        super(MapCanvas, self).__init__(**kwargs)

        self.points = list()
        self.map_height = int
        self.map_width = int
        self.map_size = tuple
        self.map_matrix = list

        self.points = list()
        self.window = Window
        self.tile_size = int
        self.vertical_padding = int
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
        """
        Interpreter for file configuration.

        :param map_file_path:
        :rtype: void
        """

        map_file = None

        try:
            map_file = open(map_file_path)

            pipe = "|"
            start_and_stop = re.compile(r',*', re.UNICODE)
            comment = re.compile(r'#.*', re.UNICODE)

            self.map_matrix = []

            y_coord = 0
            for line in map_file:
                cleaned_line = comment.sub('', line).strip()
                if cleaned_line:
                    self.map_matrix.append([])
                    x_coord_values = cleaned_line.split(pipe)
                    x_coord = 0
                    for x_coord_value in x_coord_values:
                        texture = self.get_texture(x_coord_value)
                        self.map_matrix[y_coord].append({'texture': texture, 'type': x_coord_value})
                        x_coord += 1
                    self.map_width = x_coord
                    y_coord += 1
                    if x_coord > self.map_width:
                        self.map_width = x_coord
                indication = start_and_stop.split(line.replace('#', ''))
                if len(indication) == 2:
                    self.points.append((int(indication[1]), int(indication[0])))

            self.map_height = y_coord

            self.map_size = (self.map_width, self.map_height)

            if self.map_width <= 0 or self.map_height <= 0 or not self.points:
                raise ValueError("Pipe delimited file given is not valid for use.")

        finally:
            map_file.close()

    def update_drawing_instructions(self, *_):
        """
        Update drawing instructions.

        :rtype: void
        """
        Logger.info("Adding drawing instructions")
        window_width, window_height = self.window.size
        window_height -= 50                 # It's needed to display the level bar correctly.
        min_window_size = min((window_width, window_height))
        size_needed_width = self.map_width * self.textures_size
        size_needed_height = self.map_height * self.textures_size
        size_needed_max = max(size_needed_width, size_needed_height)
        scaling_factor = size_needed_max / min_window_size
        self.tile_size = self.textures_size / scaling_factor
        self.vertical_padding = (window_width - size_needed_width / scaling_factor) / 2
        self.horizontal_padding = (window_height - size_needed_height / scaling_factor) / 2

        self.canvas.before.clear()
        self.canvas.clear()
        self.canvas.after.clear()

        start_time = datetime.now()

        self.canvas.add(Color(None))
        self.canvas.before.add(
            Rectangle(size=self.window.size, texture=self.textures['background'])
        )

        point_texture = self.textures['point']
        block_texture = self.textures['block']

        for y_coord in range(0, len(self.map_matrix)):
            for x_coord in range(0, len(self.map_matrix[y_coord])):
                x_position = (x_coord * self.tile_size) + self.vertical_padding
                # y_coord + 1 because with y_pos == 0 it would not display
                y_position = window_height - \
                            ((y_coord + 1) * self.tile_size) - \
                            self.horizontal_padding

                position = (x_position, y_position)
                tile_size_tuple = [self.tile_size] * 2
                texture = self.map_matrix[y_coord][x_coord]['texture']

                self.canvas.before.add(
                    Color(0.37, 0.69, 0.73, 1)
                    if (x_coord + y_coord) % 2
                    else Color(0.19, 0.19, 0.19, 1)
                )
                self.canvas.before.add(
                    Rectangle(size=tile_size_tuple, texture=block_texture, pos=position)
                )
                self.canvas.add(Color(None))

                if (y_coord, x_coord) in self.points:
                    self.canvas.add(
                        Rectangle(size=tile_size_tuple, texture=point_texture, pos=position)
                    )

                self.canvas.add(Rectangle(size=tile_size_tuple, texture=texture, pos=position))

        end_time = datetime.now()
        duration = end_time - start_time
        duration_seconds = duration.microseconds * 10 ** -6
        Logger.info("Drawing instruction added in %fs" % duration_seconds)
