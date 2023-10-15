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

SCREEN_WIDTH = 1680
SCREEN_HEIGHT = 1080

CHARACTER_SCALING = 1

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
        self.scale = CHARACTER_SCALING

        main_path = f'{GAME_OBJECT}\\character'

        self.is_idle = True
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        self.idle_texture = []  #idle animation
        for i in range(2):
            texture = load_texture_pair(f'{main_path}\\idle_animation_000{i+1}.png')
            self.idle_texture.append(texture)
        self.idle_texture.append(load_texture_pair(f'{main_path}\\idle_animation_0001.png'))
        for i in range(2):
            texture = load_texture_pair(f'{main_path}\\idle_animation_000{i+3}.png')
            self.idle_texture.append(texture)

        self.walking_texture = []
        for i in range(4):
            texture = load_texture_pair(f'{main_path}\\walking_animation_000{i+1}.png')
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

def TutorialCharacter():
    texture_path = f'{GAME_OBJECT}\\NPC\\tile_0021.png'
    character = arcade.Sprite(texture_path,0.8)
    character.center_x = SCREEN_WIDTH - (312 / 2)
    character.center_y = 312 / 2
    return character

def texture_bubble():
    texture_path = f'{GAME_OBJECT}\\text_bubble\\pixel-speech-bubble.png'
    speech_bubble = arcade.Sprite(texture_path,1)
    speech_bubble.center_x = SCREEN_WIDTH * 2 / 3
    speech_bubble.center_y = SCREEN_HEIGHT / 3
    return speech_bubble