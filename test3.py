import os
import sys
import arcade
import level

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(GAME_DIRECTORY)

SCREEN_WIDTH = 1680
SCREEN_HEIGHT = 1080

class GameView(arcade.Window):
    def __init__(self,width,height):
        super().__init__(width,height)

        os.chdir(GAME_DIRECTORY)

        self.tile_map = None

        self.scene = None

        self.level_list = []

    def setup(self):
        room = level.level_1()
        self.level_list.append(room)

        self.current_room = 0

        self.tile_map = arcade.load_tilemap(
            self.level_list[self.current_room].map_path,
            1,
            self.level_list[self.current_room].layer_option
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def on_draw(self):
        self.clear()

        self.scene.draw()

def main():
    window = GameView(SCREEN_WIDTH,SCREEN_HEIGHT)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
