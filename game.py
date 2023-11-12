import os
import sys
import arcade
import arcade.gui
from arcade.gui.events import UIOnClickEvent
import level
from typing import Optional
import pickle

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(GAME_DIRECTORY)

SAVE_BINARY = 0
LEVEL_BINARY = 1
HEALTH_BINARY = 2
COIN_BINARY = 3

TILE_SCALLING = 1
CHARACTER_SCALING = 1
TILE_PIXEL_SIZE = 54

SCREEN_TILES_WIDTH = 30
SCREEN_TILES_HEIGHT = 15

PLAYER_WALKING_SPEED = 0.5
PLAYER_RUNNING_SPEED = 1
PLAYER_CLIMBING_SPEED = 0.5
GRAVITY = 2
PLAYER_JUMP_SPEED = 10

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
        
class Menu(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()
        
        new_game_button = arcade.gui.UIFlatButton(text="New Game", width = 200)
        self.v_box.add(new_game_button.with_space_around(bottom=20))

        continue_button = arcade.gui.UIFlatButton(text="Continue", width=200)
        with open(f'{GAME_DIRECTORY}\\saves\\save.bin', 'rb') as file:
            x = pickle.load(file)
            if x[SAVE_BINARY][1] == 1:
                self.v_box.add(continue_button.with_space_around(bottom=20))
            file.close()
        
        quit_button = arcade.gui.UIFlatButton(text="Quit",width=200)
        self.v_box.add(quit_button)

        new_game_button.on_click = self.on_click_newgame
        continue_button.on_click = self.on_click_continue
        quit_button.on_click = self.on_click_quit

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x ="center_x",
                anchor_y="center_y",
                child=self.v_box
            )
        )

    def on_click_newgame(self,event):
        saves = [
            ['saves', 0],
            ['levels', 0],
            ['health' , 3],
            ['coin', 0]
        ]
        with open(f'{GAME_DIRECTORY}\\saves\\save.bin', 'rb') as file:
            x = pickle.load(file)
            if x[SAVE_BINARY][1] == 1:
                with open(f'{GAME_DIRECTORY}\\saves\\save.bin', 'wb') as file:
                    pickle.dump(saves,file)
            file.close()
        game_view = GameView()
        self.window.show_view(game_view)

    def on_click_continue(self,event):
        game_view = GameView()
        self.window.show_view(game_view)

    def on_click_quit(self,event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.manager.draw()

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

        self.health = None
        self.coin = None

        self.tile_map = None
        self.scene = None
        
        self.physics_engine: Optional(arcade.PymunkPhysicsEngine)

        self.level_list = (level.level1(),level.level2())

        self.level = None

        self.end_of_map = 0

        self.camera: Optional(arcade.Camera) = None

        self.gui_camera: Optional(arcade.Camera) = None

    def setup(self):

        with open(f'{GAME_DIRECTORY}\\saves\\save.bin', 'rb') as file:
            x = pickle.load(file)
            self.level = x[LEVEL_BINARY][1]
            self.health = x[HEALTH_BINARY][1]
            self.coin = x[COIN_BINARY][1]
            file.close()

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player_sprite = self.level_list[level].player_sprite

        self.camera = arcade.Camera(self.window.width,self.window.height)
        self.gui_camera = arcade.Camera(self.window.width,self.window.height)

        enemy_layer = self.tile_map.object_lists[LAYER_NAME_ENEMY]

        for my_object in enemy_layer:
            cartesian = self.tile_map.get_cartesian
    
    def load_level(self,level):

        layer_option = self.level_list[level].layer_option
        self.tile_map = arcade.load_tilemap(self.level_list[level].map_path,scaling=TILE_SCALLING)
        

        
