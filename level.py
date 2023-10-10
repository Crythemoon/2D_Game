import arcade
import asyncio
import os
import sys
import object_initialize

GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(GAME_DIRECTORY)
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

class number_level():
    def __init__(self,level):
        self.level = level
        self.background_path = None
        self.player_sprite_list = []
        self.wall_sprite_list = []
        self.background_object_list = []
        self.imovable_object_list = []

    def level_background(self,background_path):
        self.background_path = background_path

    def level_player(self,player_sprite):
        self.player_sprite_list.append(player_sprite)

    def level_wall(self,wall_sprite):
        self.wall_sprite_list.append(wall_sprite)

    def level_background_object(self,background_object):
        self.background_object = []
        self.background_object.append(background_object)

    def level_imovable_object(self):
        pass

async def level_1():
    level = number_level(1)

    background_path = f'{GAME_OBJECT}\\background\\forest-background.png'
    level.level_background(background_path)

    player_sprite = object_initialize.Player_Model()
    player_sprite.center_x = 100
    player_sprite.center_y = 100
    player_sprite.scale = 2
    level.level_player(player_sprite)

    wall_sprite_list = []
    for x in range(0,1000,36):
        wall_sprite = object_initialize.tile_map()
        wall_sprite.center_x = x
        wall_sprite.center_y = 17
        level.level_wall(wall_sprite)
    

    return level