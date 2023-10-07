import arcade
import os
import asyncio
import sys

GAME_OBJECT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     
GAME_OBJECT_DIRECTORY = os.path.join(GAME_OBJECT_DIRECTORY,'game_object')
sys.path.append(GAME_OBJECT_DIRECTORY)
print(GAME_OBJECT_DIRECTORY)
import object_initialize #type: ignore

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
GAME_NAME = 'Vampire Tombs'

class game_render(arcade.Window):
    def __init__(self,width,height,name):
        super().__init__(width,height,name)
        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)
        self.player_list = []

    def setup(self,background_image): #Game setup
        #background
        self.background = arcade.load_texture(background_image)

        #player
        self.player_list = arcade.SpriteList()
        def player_model(x,y):
            self.player_sprite = object_initialize.character_idle_animation(x,y)
            return self.player_sprite
        
        self.player_list.append(player_model)

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
