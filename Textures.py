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
    'double_wall_horizontal': 'resources/blocks/double_wall_horizontal.png',
    'double_wall_vertical': 'resources/blocks/air.png'

}

for source_name in sorted(sources):
    if not os.path.isfile(sources[source_name]):
        raise ValueError("File %s does not exist." % sources[source_name])

textures = multi_key_dict()
textures[(0, 0, 0), 'W'] = CoreImage(source=sources['wall']).texture
textures[(255, 255, 255), 'A'] = CoreImage(source=sources['air']).texture
textures[(0, 0, 0), 'L'] = CoreImage(source=sources['wall_left']).texture
textures[(0, 0, 0), 'R'] = CoreImage(source=sources['wall_right']).texture
textures[(0, 0, 0), 'T'] = CoreImage(source=sources['wall_top']).texture
textures[(0, 0, 0), 'B'] = CoreImage(source=sources['wall_bottom']).texture
textures[(0, 0, 0), 'LB'] = CoreImage(source=sources['angle_left_bottom']).texture
textures[(0, 0, 0), 'LT'] = CoreImage(source=sources['angle_left_top']).texture
textures[(0, 0, 0), 'RB'] = CoreImage(source=sources['angle_right_bottom']).texture
textures[(0, 0, 0), 'RT'] = CoreImage(source=sources['angle_right_top']).texture
textures[(0, 0, 0), 'V'] = CoreImage(source=sources['double_wall_horizontal']).texture
textures[(0, 0, 0), 'H'] = CoreImage(source=sources['double_wall_vertical']).texture
