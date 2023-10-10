import arcade
from PIL import Image
import asyncio
import numpy
import os

RIGHT_FACING = 0
LEFT_FACING = 1
UPDATE_PER_FRAME = 20
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

        self.is_idle = True

        self.idle_texture = []  #idle animation
        for i in range(2):
            texture = load_texture_pair(f'{main_path}\\idle_character_000{i+1}.png')
            self.idle_texture.append(texture)
        self.idle_texture.append(load_texture_pair(f'{main_path}\\idle_character_0001.png'))
        for i in range(2):
            texture = load_texture_pair(f'{main_path}\\idle_character_000{i+3}.png')
            self.idle_texture.append(texture)

        self.walking_texture = []
        for i in range(4):
            texture = load_texture_pair(f'{main_path}\\walking_character_000{i+1}.png')
            self.walking_texture.append(texture)

        self.jumping_texture = []
        


    def update_animation(self,delta_time: float = 1 / 60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_x == 0 and self.change_y == 0:
            self.cur_texture += 1
            if self.cur_texture > 4 * UPDATE_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.idle_texture[frame][direction]

        if self.change_x != 0 and self.change_y == 0:
            self.cur_texture += 1
            if self.cur_texture > 3 * UPDATE_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.walking_texture[frame][direction]