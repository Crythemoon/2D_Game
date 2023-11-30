import arcade
from PIL import Image
import asyncio
import numpy
import os

RIGHT_FACING = 0
LEFT_FACING = 1
UP_FACING = 0
DOWN_FACING = 1
IDLE_FACING = 3

UPDATE_PER_FRAME = 20
GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

SCREEN_WIDTH = 1680
SCREEN_HEIGHT = 1080

CHARACTER_SCALING = 0.8

PLAYER_WALKING_SPEED = 0.5
PLAYER_RUNNING_SPEED = 1

ENEMY_SCALING = 1
ENEMY_SPEED = 0.5

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

        self.walking = False
        self.running = False
        self.jumping = False
        self.attacking = False
        self.dashing = False
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

        self.running_texture = []
        for i in range(8):
            texture = load_texture_pair(f'{main_path}\\running_animation_000{i+1}.png')
            self.running_texture.append(texture)
        
        self.jumping_texture = []
        for i in range(8):
            texture = load_texture_pair(f'{main_path}\\jumping_animation_000{i+1}.png')
            self.jumping_texture.append(texture)

        self.climbing_texture = []
        for i in ('up','down'):
            texture = load_texture_pair(f'{main_path}\\climbing_{i}_animation.png')
        self.climbing_texture.append(load_texture_pair(f'{main_path}\\idle_animation_0001.png'))

        self.set_hit_box([[-48,-48],[-48,48],[48,-48],[48,48]])

    def update_animation(self,delta_time: float = 1 / 60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_x == 0 and self.change_y == 0 and not self.is_on_ladder:
            self.cur_texture += 1
            if self.cur_texture >= 5 * UPDATE_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.idle_texture[frame][direction]

        if self.walking and not self.is_on_ladder:
            self.cur_texture += 1
            if self.cur_texture >= 4 * UPDATE_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.walking_texture[frame][direction]

        if self.running and not self.is_on_ladder:
            self.cur_texture += 1
            if self.cur_texture >= 8:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.running_texture[frame][direction]

        if self.is_on_ladder:
            direction = self.character_face_direction
            if self.change_y > 0:
                self.texture = self.climbing_texture[UP_FACING][direction]
            elif self.change_y < 0:
                self.texture = self.climbing_texture[DOWN_FACING][direction]
            else:
                self.texture = self.climbing_texture[IDLE_FACING][direction]

        if self.jumping and not self.is_on_ladder:
            self.cur_texture += 1
            if self.cur_texture >= 8:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.jumping_texture[frame][direction]
        
        if self.dashing:
            self.texture = None


class BatEnemy(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.character_face_direction = LEFT_FACING
        self.cur_texture = 0
        self.cur_position = 0
        
        self.speed = ENEMY_SPEED

        self.scale = ENEMY_SCALING

        main_path = f'{GAME_OBJECT}\\kenney_pixel-platformer\\Tiles\\Characters'

        self.all_texture = []
        for i in range(3):
            texture = load_texture_pair(f'{main_path}\\tile_002{i+4}.png')
            self.all_texture.append(texture)
        
        self.set_hit_box(
            [
                [-32,-32],
                [-32,32],
                [32,-32],
                [32,32]
            ]
        )
        
    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_x == 0 and self.change_y == 0:
            self.cur_texture += 1
            if self.cur_texture >= 3 * UPDATE_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.all_texture[frame][direction]

        if self.change_x != 0 and self.change_y == 0:
            self.cur_texture += 1
            if self.cur_texture >= 3 * UPDATE_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.all_texture[frame][direction]

class BlueRobotEnemy(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.character_face_direction = LEFT_FACING

        self.cur_texture = 0
        self.scale = ENEMY_SCALING

        main_path = f'{GAME_OBJECT}\\kenney_pixel-platformer\\Tiles\\Characters'

        self.is_idle = True
        self.is_moving = False

        self.idle_texture = []
        for i in range (3):
            texture = load_texture_pair(f'{main_path}\\tile_00{i+18}')
            self.idle_texture.append(texture)
        
        self.moving_texture = []
        for i in range (2):
            texture = load_texture_pair(f'{main_path}\\tile_00{i+18}')
            self.moving_texture.append(texture)
    
    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        elif self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING

        if self.change_x == 0:
            self.is_idle = True
        elif self.change_x != 0:
            self.is_idle = False
            self.is_moving = True

        if self.is_idle:
            self.cur_texture += 1
            if self.cur_texture > 3 * UPDATE_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.idle_texture[frame][direction]

        if self.is_moving:
            self.cur_texture += 1
            if self.cur_texture > 2 * UPDATE_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.moving_texture[frame][direction]

class RedRobotEnemy(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.character_face_direction = LEFT_FACING

        self.cur_texture = 0
        self.scale = ENEMY_SCALING

        main_path = f'{GAME_OBJECT}\\kenney_pixel-platformer\\Tiles\\Characters'

        self.is_idle = True
        self.is_moving = False

        self.idle_texture = []
        for i in range(3):
            texture = load_texture_pair(f'{main_path}\\tile_00{i+15}')
            self.idle_texture.append(texture)
        
        self.moving_texture = []
        for i in range (2):
            texture = load_texture_pair(f'{main_path}\\tile_00{i+15}')
            self.moving_texture.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING
        elif self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction == LEFT_FACING
        
        if self.change_x == 0:
            self.is_idle = True
        elif self.change_x != 0:
            self.is_idle = False
            self.is_moving = True

        if self.is_idle:
            self.cur_texture += 1
            if self.cur_texture > 3 * UPDATE_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.idle_texture[frame][direction]
        
        if self.is_moving:
            self.cur_texture += 1
            if self.cur_texture > 2 * UPDATE_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATE_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.moving_texture[frame][direction]

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


