import arcade
from arcade.application import Window

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(None)
    
    def on_draw(self):
        arcade.draw_text("Hello", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 
                         arcade.color.BLACK,font_size=50, anchor_x="center")
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game = GameView()
        self.window.show_view(game)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)
    
    def on_draw(self):
        arcade.draw_text("Hello", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 
                         arcade.color.BLACK,font_size=50, anchor_x="center")
    
def main():
    window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,"Hello")
    menu = MenuView()
    window.show_view(menu)
    arcade.run()
main()