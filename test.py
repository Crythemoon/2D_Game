import arcade
import os
import asyncio
import sys

import object_initialize

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
GAME_NAME = 'Vampire Tombs'

class game_render(arcade.Window):
    def __init__(self,width,height,name):
        super().__init__(width,height,name)
        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)
        self.player_list = None
        self.background_object = None
        self.imovable_object = None
        self.enemies = None

        GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))     
        sys.path.append(GAME_DIRECTORY)

    def setup(self): #Game setup
        def background_image(self,background_im):   #background
            self.background = arcade.load_texture(background_im)

        #player
        self.player_list = arcade.SpriteList()

        #background object
        self.background_object = arcade.SpriteList()

        #imovable object
        self.imovable_object = arcade.SpriteList()

        #don't touch object
        self.enemies = arcade.SpriteList()

    
    def on_draw(self):  #Game render
        arcade.start_render()

        #render background
        arcade.draw_lrwh_rectangle_textured(0,0,1920,1200,self.background)

        #render player
    
    def update(self,delta_time):    #Game logic
        pass

def main():
    start = game_render(SCREEN_WIDTH,SCREEN_HEIGHT,GAME_NAME)
    image = 'C:\\Users\\cryth\\OneDrive\\Documents\\GitHub\\2D_Game\\game-object\\game-attribute\\background\\forest-background.png'
    start.setup(image)
    start.setup.player_model(50,50)
    arcade.run()
if __name__=='__main__':
    asyncio.run(main())
