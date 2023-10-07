import arcade
import asyncio
import sys
sys.path.insert(0,'C:\\Users\\cryth\\OneDrive\\Documents\\GitHub\\2D_Game\\game-object')

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
GAME_NAME = 'Vampire Tombs'

class game_render(arcade.Window):
    def __init__(self,width,height,name):
        super().__init__(width,height,name)
        self.background = None
        arcade.set_background_color(arcade.color.AMAZON)

    async def setup(self,image): #Game setup
        self.background = arcade.load_texture(image)
    
    async def on_draw(self):  #Game render
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,1920,1200,self.background)
    
    def update(self,delta_time):    #Game logic
        pass

async def main():
    start = game_render(SCREEN_WIDTH,SCREEN_HEIGHT,GAME_NAME)
    image = 'C:\\Users\\cryth\\OneDrive\\Documents\\GitHub\\2D_Game\\game-object\\game-attribute\\background\\forest-background.png'
    await start.setup(image)
    arcade.run()
if __name__=='__main__':
    asyncio.run(main())
