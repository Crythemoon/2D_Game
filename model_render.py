import arcade
import sys

class game(arcade.Window):
    def __init__(self,width,height,name):
        super().__init__(width,height,name)
        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self): #Game setup
        pass

    def on_draw(self):  #Game render
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,1920,1200,self.background)
    
    def update(self,delta_time):    #Game logic
        pass

class object(game.setup()):
    def background(self,background_image):
        super().