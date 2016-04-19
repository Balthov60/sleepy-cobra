# coding: utf8

from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Point
from MapCanvas import MapCanvas


class Level(FloatLayout):
    def __init__(self, map_file_path, textures, **kwargs):
        """
        Charge la carte dans un layout.
        Charge les données et la matrix de tile et de touch
        :param map_file_path: Chemin de la carte
        :param textures: dictionnaire de textures
        :param kwargs: Argumens du layout
        """
        super(Level, self).__init__(**kwargs)
        self.map_canvas = MapCanvas(map_file_path, textures)
        self.add_widget(self.map_canvas)

        # charge les informations de touch et de tile
        self.touch_width = int
        self.touch_scaling_factor = 6

        self.level_size = list
        self.tile_size = list

        self.xmax = int
        self.ymax = int
        self.matrix = None

        self.color = (1, 1, 1)
        self.old_point = list
        self.point = list

        self.define_level_properties()

    """
    level properties for initialisation
    """

    def define_level_properties(self):
        # defini l'épaisseur de trait de touch
        self.touch_width = self.map_canvas.tile_size / self.touch_scaling_factor

        # defini la taille reel des tile
        self.level_size = [self.map_canvas.window.size[0] - self.map_canvas.vectical_padding * 2,
                           self.map_canvas.window.size[1] - self.map_canvas.horizontal_padding * 2]
        self.tile_size = [self.level_size[0] / self.map_canvas.map_size[0],
                          self.level_size[1] / self.map_canvas.map_size[1]]

        # initialise la matrice
        self.xmax = self.map_canvas.map_size[0]
        self.ymax = self.map_canvas.map_size[1]
        self.matrix = [[0 for _ in xrange(self.xmax)] for _ in xrange(self.ymax)]

        # rempli la matrice avec les coordonnées
        x = self.map_canvas.vectical_padding
        y = self.map_canvas.window.size[1] - self.map_canvas.horizontal_padding

        for indx in range(self.ymax):
            for indy in range(self.xmax):
                self.matrix[indy][indx] = [x, y, x + self.tile_size[0], y - self.tile_size[1]]
                y -= self.tile_size[1]
            x += self.tile_size[0]
            y = self.map_canvas.window.size[1]

    """
    Tiles methods
    """

    def get_touch_auth(self, tile_type):
        """
        test the current tile to get authorizations
        :param tile_type: string (key of the texture)
        :rtype: boolean
        """
        if tile_type == "A":
            return True
        elif tile_type == "W":
            return False

    def get_tile_properties(self):
        """
        find the current tile
        :rtype: string (key of the texture)
        """
        for indx in range(self.ymax):
            for indy in range(self.xmax):
                horizontal_location = self.matrix[indy][indx][0] <= self.point[0] < self.matrix[indy][indx][2]
                vertical_location = self.matrix[indy][indx][1] >= self.point[1] > self.matrix[indy][indx][3]
                if horizontal_location and vertical_location:
                    tile_type = self.map_canvas.map_matrix[indy][indx]['type']
                    return tile_type

    def test_win_conditions(self):
        """
        test if players win
        :rtype: boolean
        """
        return True

    """"
    Touch methods
    """""

    def on_touch_down(self, touch):

        # sauvegarde le touch
        ud = touch.ud
        ud['identifier'] = str(touch.uid)
        self.point = [touch.x, touch.y]

        # dessine le point si l'emplacement est valide sinon supprime le dessin.
        tile_type = self.get_tile_properties()
        if self.get_touch_auth(tile_type):
            with self.canvas:
                Color(self.color)
                ud['points'] = [Point(points=self.point, pointsize=self.touch_width, group=ud['identifier'])]
        else:
            touch.ungrab(self)
            self.canvas.remove_group(ud['identifier'])
            return

        # sauvegarde les differentes coordonnées
        self.old_point = ud['points'][0].points[:]
        self.point = ud['points'][0].points[:]

        # lance le touch
        touch.grab(self)

    def on_touch_move(self, touch):

        # si le touch est lancé
        if touch.grab_current is not self:
            return

        # sauvegarde le touch
        ud = touch.ud
        ud['identifier'] = str(touch.uid)
        self.point = [touch.x, touch.y]

        """
        enlever le commentaire pour reimplementer le touch guider.

        # recupere la distance relative entre les deux états du touch
        x_dif = touch.x - self.old_point[0]
        y_dif = touch.y - self.old_point[1]

        # trouve la direction du touch guidé et sauvegarde les valeurs
        if abs(x_dif) > abs(y_dif):
            self.point[0] += x_dif
        else:
            self.point[1] += y_dif
        """

        # dessine le point si l'emplacement est valide sinon supprime le dessin.
        tile_type = self.get_tile_properties()
        if self.get_touch_auth(tile_type):
            with self.canvas:
                Color(self.color)
                ud['points'] = [Point(points=self.point, pointsize=self.touch_width, group=ud['identifier'])]
        else:
            touch.ungrab(self)
            self.canvas.remove_group(ud['identifier'])
            return

        # recupere les coordonnées
        self.old_point = [touch.x, touch.y]

    def on_touch_up(self, touch):

        # si le touch est lancé
        if touch.grab_current is not self:
            return

        if self.test_win_conditions():
            print("win")
            return;

        # supprime le touch UD en question
        touch.ungrab(self)
        ud = touch.ud
        self.canvas.remove_group(ud['identifier'])
