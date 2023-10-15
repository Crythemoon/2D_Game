import arcade
import os
import sys
import object_initialize

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(GAME_DIRECTORY)

SCREEN_WIDTH = 1680
SCREEEN_HEIGHT = 1080

class CutScene(arcade.View):
    def __init__(self,level):
        super().__init__()
        self.level = level
        self.texture_list = None

    def setup(self,character_texture,text_bubble_texture):
        self.texture_list = arcade.SpriteList()
        character = character_texture
        self.texture_list.append(character)
        text_bubble = text_bubble_texture
        self.texture_list.append(text_bubble)

    def on_draw(self):
        self.texture_list.draw()
