import arcade
import asyncio
import os
import sys
import object_initialize
import test3

GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(GAME_DIRECTORY)
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

LAYER_NAME_NPC = "NPC"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_DYNAMIC_PLATFORM = "Dynamic Platform"
LAYER_NAME_FOREGROUND = "Foregrounds"
LAYER_NAME_BACKGROUND = "Backgrounds"
LAYER_NAME_ENEMY = "Enemies"
LAYER_NAME_PLAYER = "Player"

class level1():
    def __init__(self):
        self.level = 1
        self.map_path = f'{GAME_DIRECTORY}\\level\\level_1.tmx'
        self.layer_option = {
            LAYER_NAME_NPC: {"use_spatial_hash": True},
            LAYER_NAME_PLATFORMS: {"use_spatial_hash": True},
            LAYER_NAME_DYNAMIC_PLATFORM: {"use_spatial_hash": True},
            LAYER_NAME_ENEMY: {"use_spatial_hash": True}
        }

class level2():
    def __init__(self):
        self.level = 2
        