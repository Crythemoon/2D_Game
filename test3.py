import arcade
import os
import sys
from typing import Optional

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(GAME_DIRECTORY)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        os.chdir(GAME_DIRECTORY)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.attack_pressed = False
        self.jump_needs_reset = False

        self.tile_map = None

        self.scene = None

        self.player_sprite: Optional(arcade.Sprite) = None
        self.NPC_sprite_list: Optional(arcade.SpriteList) = None
        self.foregound_sprite_list: Optional(arcade.SpriteList) = None
        self.enemies_sprite_list: Optional(arcade.SpriteList) = None
        self.dynamic_platform_sprite_list: Optional(arcade.SpriteList) = None
        self.platform_sprite_list: Optional(arcade.SpriteList) = None

        self.tile_map = None
        self.scene = None
        
        self.physics_engine: Optional(arcade.PymunkPhysicsEngine)

        self.level = None

        self.end_of_map = 0

        self.camera: Optional(arcade.Camera) = None

        self.gui_camera: Optional(arcade.Camera) = None
