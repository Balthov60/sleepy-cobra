# coding: utf8

from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Point
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

        self.touch_width = None
        self.matrix = None
        self.tile_size = None
        self.xmax = self.map_canvas.map_size[0]
        self.ymax = self.map_canvas.map_size[1]
        self.define_level_properties()

        self.old_point = None
        self.point = None

    def define_level_properties(self):
        # defini l'épaisseur de trait de touch
        self.touch_width = self.map_canvas.tile_size / 6

        # defini la taille reel des tile
        self.tile_size = [(self.map_canvas.window.size[0] - self.map_canvas.vectical_padding * 2) / self.map_canvas.map_size[0],
                          (self.map_canvas.window.size[1] - self.map_canvas.horizontal_padding * 2) / self.map_canvas.map_size[1]]

        # initialise la matrice
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

        print(self.matrix)
        print(self.map_canvas.window.size)
        print(self.map_canvas.map_size)
        print(self.tile_size)

    def get_touch_auth(self):
        for indx in range(self.ymax):
            for indy in range(self.xmax):
                if (self.matrix[indy][indx][0] <= self.point[0] < self.matrix[indy][indx][2]) and (
                                self.matrix[indy][indx][1] >= self.point[1] > self.matrix[indy][indx][3]):
                    print(indy, indx, "ok")
                    print(self.map_canvas.map_matrix[indy][indx])
                    print(self.map_canvas.get_texture("A"))
                    if self.map_canvas.map_matrix[indy][indx] == self.map_canvas.get_texture("A"):
                        return True
                    return False

    def on_touch_down(self, touch):

        # sauvegarde le touch
        ud = touch.ud
        ud['identifier'] = str(touch.uid)

        self.point = [touch.x, touch.y]

        # dessine le premier point si l'emplacement est valide
        if self.get_touch_auth():
            with self.canvas:
                Color(0, 0, 1)
                ud['points'] = [Point(points=(touch.x, touch.y), pointsize=self.touch_width, group=ud['identifier'])]
        else:
            return

        # sauvegarde les differentes coordonnées
        self.old_point = ud['points'][0].points[:]
        self.point = ud['points'][0].points[:]
        print(self.point)

        touch.grab(self)

    def on_touch_move(self, touch):

        if touch.grab_current is not self:
            return

        # sauvegarde le touch
        ud = touch.ud
        ud['identifier'] = str(touch.uid)

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

        self.point[0] = touch.x
        self.point[1] = touch.y

        # dessine le point si l'emplacement est valide
        if self.get_touch_auth():
            with self.canvas:
                Color(0, 0, 1)
                ud['points'].append(
                    Point(points=(self.point), pointsize=self.touch_width, group=ud['identifier']))

        # recupere les ancienne coordonnées
        self.old_point[0] = touch.x
        self.old_point[1] = touch.y

    def on_touch_up(self, touch):

        # supprime le touch UD en question
        if touch.grab_current is not self:
            return
        touch.ungrab(self)

        ud = touch.ud
        self.canvas.remove_group(ud['identifier'])
