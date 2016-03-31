import os.path
from kivy.uix.image import Image as CoreImage

sources = {
    'wall': 'resources/wall.png',
    'air': 'resources/air.png'
}

for source_name in sorted(sources):
    if not os.path.isfile(sources[source_name]):
        raise ValueError("File %s does not exist." % sources[source_name])

textures = {
    (0, 0, 0): CoreImage(source=sources['wall']).texture,
    (255, 255, 255): CoreImage(source=sources['air']).texture
}
