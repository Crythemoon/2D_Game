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

WINDOW_WIDTH = 1620
WINDOW_HEIGHT = 810

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

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.WHITE)

        os.chdir(GAME_DIRECTORY)

        self.tile_map = None
        self.scene = None

        self.level = None
        self.health = None
        self.coin = None

        self.level_list = [level.level1]

    def load_level(self):
        with open(f'{GAME_DIRECTORY}\\saves\\saves.bin', 'rb') as file:
            x = pickle.load(file)
            self.level_number = x[LEVEL_BINARY][1] - 1
            self.health = x[HEALTH_BINARY][1] - 1
            self.coin = x[COIN_BINARY][1]
            file.close()
        
        self.level = self.level_list[self.level_number]

    def setup(self):
        self.load_level
        layer_option = self.level.layer_option
        self.tile_map = arcade.load_tilemap(map_file=self.level.map_path,scaling=TILE_SCALLING,layer_options=layer_option)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def on_show_view(self):
        self.setup

    def on_draw(self):
        self.clear()
        self.scene.draw()


def main():
    window = arcade.Window(width=WINDOW_WIDTH,height=WINDOW_HEIGHT,title="Test")
    game = GameView()
    window.show_view(game)
    arcade.run()

main()