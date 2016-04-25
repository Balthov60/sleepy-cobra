from kivy.uix.image import Image as CoreImage

import os.path

from multi_key_dict import multi_key_dict

sources = {
    'wall': 'resources/blocks/wall.png',
    'air': 'resources/blocks/air.png',
    'wall_left': 'resources/blocks/wall_left.png',
    'wall_right': 'resources/blocks/wall_right.png',
    'wall_top': 'resources/blocks/wall_top.png',
    'wall_bottom': 'resources/blocks/wall_bottom.png',
    'angle_left_bottom': 'resources/blocks/angle_left_bottom.png',
    'angle_left_top': 'resources/blocks/angle_left_top.png',
    'angle_right_bottom': 'resources/blocks/angle_right_bottom.png',
    'angle_right_top': 'resources/blocks/angle_right_top.png',
    'angle_top': 'resources/blocks/angle_top.png',
    'angle_bottom': 'resources/blocks/angle_bottom.png',
    'angle_right': 'resources/blocks/angle_right.png',
    'angle_left': 'resources/blocks/angle_left.png',
    'double_wall_horizontal': 'resources/blocks/double_wall_horizontal.png',
    'double_wall_vertical': 'resources/blocks/double_wall_vertical.png'

}

for source_name in sorted(sources):
    if not os.path.isfile(sources[source_name]):
        raise ValueError("File %s does not exist." % sources[source_name])

textures = multi_key_dict()
textures[(0, 0, 0), 'W'] = CoreImage(source=sources['wall']).texture
textures[(255, 255, 255), 'A'] = CoreImage(source=sources['air']).texture
textures[(1, 0, 0), 'L'] = CoreImage(source=sources['wall_left']).texture
textures[(2, 0, 0), 'R'] = CoreImage(source=sources['wall_right']).texture
textures[(3, 0, 0), 'T'] = CoreImage(source=sources['wall_top']).texture
textures[(4, 0, 0), 'B'] = CoreImage(source=sources['wall_bottom']).texture
textures[(5, 0, 0), 'LB'] = CoreImage(source=sources['angle_left_bottom']).texture
textures[(6, 0, 0), 'LT'] = CoreImage(source=sources['angle_left_top']).texture
textures[(7, 0, 0), 'RB'] = CoreImage(source=sources['angle_right_bottom']).texture
textures[(8, 0, 0), 'RT'] = CoreImage(source=sources['angle_right_top']).texture
textures[(9, 0, 0), 'AT'] = CoreImage(source=sources['angle_top']).texture
textures[(10, 0, 0), 'AB'] = CoreImage(source=sources['angle_bottom']).texture
textures[(11, 0, 0), 'AR'] = CoreImage(source=sources['angle_right']).texture
textures[(12, 0, 0), 'AL'] = CoreImage(source=sources['angle_left']).texture
textures[(13, 0, 0), 'H'] = CoreImage(source=sources['double_wall_horizontal']).texture
textures[(14, 0, 0), 'V'] = CoreImage(source=sources['double_wall_vertical']).texture

# authorization boolean list format : {left, right, top, bot, start/stop}
authorizations = dict()
authorizations['W'] = [False, False, False, False, False]
authorizations['A'] = [True, True, True, True, False]
authorizations['L'] = [False, True, True, True, False]
authorizations['R'] = [True, False, True, True, False]
authorizations['T'] = [True, True, False, True, False]
authorizations['B'] = [True, True, True, False, False]
authorizations['LB'] = [False, True, True, False, False]
authorizations['LT'] = [False, True, False, True, False]
authorizations['RB'] = [True, False, True, False, False]
authorizations['RT'] = [True, False, False, True, False]
authorizations['AT'] = [False, False, False, True, False]
authorizations['AB'] = [False, False, True, False, False]
authorizations['AR'] = [False, True, False, False, False]
authorizations['AL'] = [True, False, False, False, False]
authorizations['H'] = [True, True, False, False, False]
authorizations['V'] = [False, False, True, True, False]

