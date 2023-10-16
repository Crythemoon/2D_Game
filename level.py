import arcade
import asyncio
import os
import sys
import object_initialize

GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(GAME_DIRECTORY)
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_FOREGROUND = "Foregounds"
LAYER_NAME_BACKGROUND = "Backgrounds"
LAYER_NAME_CHARACTER = "Characters"

class number_level():
    def __init__(self,level):
        self.level = level
        self.background_path = None
        self.player_sprite_list = []

    def level_background(self,background_path):
        self.background_path = background_path

    def level_player(self,player_sprite):
        self.player_sprite = player_sprite

    def level_tile_map(self,map_path,layer_option):
        self.map_path = map_path
        self.layer_option = layer_option

def level_1():
    level = number_level(1)

    player_sprite = object_initialize.Player_Model()
    player_sprite.center_x = 100
    player_sprite.center_y = 100
    player_sprite.scale = 1
    level.level_player(player_sprite)

    tile_map_path = f'{GAME_DIRECTORY}\\level\\level_1.tmx'

    layer_option = {
        LAYER_NAME_PLATFORMS:{
            "use_spatial_hash": True
        },
        LAYER_NAME_BACKGROUND:{
            "use_spatial_hash": False
        },
        LAYER_NAME_FOREGROUND:{
            "use_spatial_hash": False
        },
        LAYER_NAME_CHARACTER:{
            "use_spatial_hash": True
        }
    }
    level.level_tile_map(map_path=tile_map_path,layer_option=layer_option)

    tile_map = arcade.load_tilemap(tile_map_path,1,layer_option)
    scene = arcade.Scene.from_tilemap(tile_map)
    def tutorial_character():
        character_interaction = arcade.check_for_collision(player_sprite,scene["Character"])
        pass
    

    return level

