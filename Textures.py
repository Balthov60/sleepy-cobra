from kivy.uix.image import Image as CoreImage

import os.path

from multi_key_dict import multi_key_dict

sources = {
    'wall': 'resources/wall.png',
    'air': 'resources/air.png'
}

for source_name in sorted(sources):
    if not os.path.isfile(sources[source_name]):
        raise ValueError("File %s does not exist." % sources[source_name])

textures = multi_key_dict()
textures[(0, 0, 0), 'W'] = CoreImage(source=sources['wall']).texture
textures[(255, 255, 255), 'X'] = CoreImage(source=sources['air']).texture
