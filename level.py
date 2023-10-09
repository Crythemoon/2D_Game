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
        self.background_object_list = []
        self.imovable_object_list = []

    def level_background(self,background_path):
        self.background_path = background_path

    def level_player(self,player_sprite):
        self.player_sprite_list.append(player_sprite)

    def level_background_object(self,background_object):
        self.background_object = []
        self.background_object.append(background_object)

    def level_imovable_object(self):
        pass

async def level_1():
    level = number_level(1)

    background_path = f'{GAME_OBJECT}\\background\\forest-background.png'
    level.level_background(background_path)

    player_sprite = await object_initialize.character_idle_animation(50,50)
    level.level_player(player_sprite)
    
    await player_sprite
    return level