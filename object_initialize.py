import arcade
from PIL import Image
import asyncio
import numpy
import os

GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

DISPLAY_SIZE = arcade.get_display_size

def scale(s,x):
    return DISPLAY_SIZE(1)[1] / (s*x)

async def image_size(path):
    im = Image.open(path)
    height = numpy.array(im)
    height = height.shape[0]
    return height

async def character_idle_animation(x,y):
    image_path = f'{GAME_OBJECT}\\character\\Idle gif right.gif'
    task = await(image_size(image_path))
    size = scale(task,30)
    model = arcade.Sprite(image_path,size)
    model.center_x = x
    model.center_y = y
    return model
