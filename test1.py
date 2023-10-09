import os
import sys
from PIL import Image
import numpy
GAME_OBJECT = os.path.dirname(os.path.abspath(__file__))
GAME_OBJECT = os.path.join(GAME_OBJECT,'game_object')
print(GAME_OBJECT)
image = f'{GAME_OBJECT}\\background\\forest-background.png'
print(image)
im = Image.open(image)
height = numpy.array(im)
print(height.shape)