import arcade
import asyncio
import os
import sys
import object_initialize

GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(GAME_DIRECTORY)
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

TILE_PIXEL_SIZE = 54

LAYER_NAME_FLAG = "Flag"
LAYER_NAME_NPC = "NPC"
LAYER_NAME_COIN = "Coin"
LAYER_NAME_HEART = "Heart"
LAYER_NAME_FOREGROUND = "Foregrounds"
LAYER_NAME_LADDER = "Ladders"
LAYER_NAME_ENEMY = "Enemy"
LAYER_NAME_DYNAMIC_PLATFORM = "Dynamic Platforms"
LAYER_NAME_PLATFORMS_B = "Platforms B"
LAYER_NAME_PLATFORMS_A = "Platforms A"
LAYER_NAME_BACKGROUND = "Backgrounds"
LAYER_NAME_DEATH_ZONE = "Death Zone"

class level1():
    def __init__(self):
        self.level = 1
        self.map_path = f'{GAME_DIRECTORY}\\level\\level_1.tmx'
        self.layer_option = {
            LAYER_NAME_FLAG: {
                'use_spatial_hash': True
            },
            LAYER_NAME_NPC: {
                'use_spatial_hash': True
            },
            LAYER_NAME_COIN: {
                'use_spatial_hash': True
            },
            LAYER_NAME_HEART:{
                'use_spatial_hash': True
            },
            LAYER_NAME_LADDER:{
                'use_spatial_hash': True
            },
            LAYER_NAME_ENEMY:{
                'use_spatial_hash': True
            },
            LAYER_NAME_DYNAMIC_PLATFORM:{
                'use_spatial_hash': True
            },
            LAYER_NAME_PLATFORMS_B:{
                'use_spatial_hash': True
            },
            LAYER_NAME_PLATFORMS_A:{
                'use_spatial_hash': True
            },
            LAYER_NAME_DEATH_ZONE:{
                'use_spatial_hash': True
            }
        }
        self.player_sprite = object_initialize.Player_Model()

        self.player_sprite.center_x = 1 * TILE_PIXEL_SIZE
        self.player_sprite.center_y = 6 * TILE_PIXEL_SIZE
        

class level2():
    def __init__(self):
        self.level = 2
        