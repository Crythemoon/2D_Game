import arcade
from PIL import Image
import numpy
import asyncio
import os
import sys

DISPLAY = arcade.get_display_size

def scale(s,x):
    return DISPLAY(1)[1] / (s*x)

async def image_size(path):
    im = Image.open(path)
    height = numpy.asrray(im)
    return height

async def character_idle_animation(x,y):
    image_path = 'C:\\Users\\cryth\\OneDrive\\Documents\\GitHub\\2D_Game\\game-object\\game-attribute\\character\\Idle gif right.gif'
    task = asyncio.create_task(image_size(image_path))
    await task
    size = scale(task,30)
    model = arcade.Sprite(image_path,size)
    model.center_x = x
    model.center_y = y
    return model
