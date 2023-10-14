import arcade
import os
import sys

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(GAME_DIRECTORY)

SCREEN_WIDTH = 1680
SCREEEN_HEIGHT = 1080

class CutScene(arcade.View):
    def __init__(self,level):
        super().__init__()
        self.level = level
        self.texture_list = None

    def setup(self,texture,x,y):
        self.texture_list = arcade.SpriteList
        character = texture
        character.center_x = SCREEN_WIDTH - (x / 2)
        character.center_y = y / 2
        self.texture_list.append(character)

    def on_draw(self):
        self.texture_list.draw()