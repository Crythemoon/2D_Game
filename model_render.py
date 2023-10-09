import arcade
import asyncio
import os
import sys
import level
GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(GAME_DIRECTORY)
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
GAME_NAME = 'Vampire Tombs'

class game(arcade.Window):
    def __init__(self,width,height,name):
        super().__init__(width,height,name)
        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self,background_path): #Game setup
        self.background = arcade.load_texture(background_path)
    
    def on_draw(self):  #Game render
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,1920,1200,self.background)
    
    def update(self,delta_time):    #Game logic
        pass
        
async def main():
    start = game(SCREEN_WIDTH,SCREEN_HEIGHT,GAME_NAME)
    level1 = await level.level_1()
    start.setup(level1.background_path)
    arcade.run()
asyncio.run(main())