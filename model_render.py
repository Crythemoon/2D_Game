import arcade
import sys
sys.path.insert(0,'C:\\Users\\cryth\\OneDrive\\Documents\\GitHub\\2D_Game\\game-object')

class game(arcade.Window):
    def __init__(self,width,height,name):
        super().__init__(width,height,name)
        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self): #Game setup
        self.background = arcade.load_texture('C:\\Users\\cryth\\OneDrive\\Documents\\GitHub\\2D_Game\\game-object\\game-attribute\\background\\forest-background.png')
    
    def on_draw(self):  #Game render
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,1920,1200,self.background)
    
    def update(self,delta_time):    #Game logic
        pass
