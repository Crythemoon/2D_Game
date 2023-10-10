import arcade
from PIL import Image
import asyncio
import numpy
import os

RIGHT_FACING = 0
LEFT_FACING = 1
UPDATE_PER_FRAME = 70
GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

def load_texture_pair(file_path):
    return [
        arcade.load_texture(file_path),
        arcade.load_texture(file_path,flipped_horizontally=True)
    ]

class Player_Model(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.scale = 1
        main_path = f'{GAME_OBJECT}\\character'

        self.idle_texture = []
        for i in range(2):
            texture = load_texture_pair(f'{main_path}\\tile_00{i+15}.png')
            self.idle_texture.append(texture)
        self.idle_texture.append(load_texture_pair(f'{main_path}\\tile_0016.png'))

    def update_animation(self,delta_time: float = 1 / 60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        
        self.cur_texture += 1
        if self.cur_texture > 1 * UPDATE_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATE_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.idle_texture[frame][direction]

async def tile_map_22():
    wall_path = f'{GAME_OBJECT}\\wall\\tile_22.png'
    wall_sprite = arcade.Sprite(wall_path,2)
    return wall_sprite

async def tile_map_122():
    wall_path = f'{GAME_OBJECT}\\wall\\tile_122.png'
    wall_sprite = arcade.Sprite(wall_path,2)
    return wall_sprite
