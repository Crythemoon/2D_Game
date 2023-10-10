import arcade
import asyncio
import os
import sys
import level
GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(GAME_DIRECTORY)
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_NAME = 'Vampire Tombs'

class game(arcade.Window):
    def __init__(self,width,height,name):
        super().__init__(width,height,name)
        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)

        self.player_list = None
        self.wall_list = None

    def setup(self,background_path,player_sprite,wall_sprite_list): #Game setup
        self.background = arcade.load_texture(background_path)

        self.player_list = arcade.SpriteList()
        for i in player_sprite:
            self.player_list.append(i)

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        for i in wall_sprite_list:
            self.wall_list.append(i)

    def on_draw(self):  #Game render
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)
        self.player_list.draw()
        self.wall_list.draw()
    
    def update(self,delta_time):    #Game logic
        self.player_list.update()
        self.player_list.update_animation()

        
async def main():
    start = game(SCREEN_WIDTH,SCREEN_HEIGHT,GAME_NAME)
    level1 = await level.level_1()
    start.setup(level1.background_path,level1.player_sprite_list,level1.wall_sprite_list)
    arcade.run()
asyncio.run(main())