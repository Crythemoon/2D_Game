import arcade
import sys
import os
import object_initialize

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(GAME_DIRECTORY)

SCREEN_WIDTH = 1680
SCREEN_HEIGHT = 1080

TILE_SCALING = 1
TILE_SIZE = 54

RIGHT_FACING = 0
LEFT_FACING = 1

LAYER_NAME_PLATFORM = "Platforms"
LAYER_NAME_PLAYER = "Player"

GRAVITY = 1

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        os.chdir(GAME_DIRECTORY)

        self.tile_map = None
        self.scene = None

        self.player_sprite = None

        self.camera = None

        self.gui_camera = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.space_pressed = False
        self.f_pressed = False
        self.shift_pressed = False
        self.attack_pressed = False
        self.spell_pressed = False
        self.jump_needs_reset = False
        self.dash_needs_reset = False

        self.time_since_last_dash = 0.0
        self.time_between_dash = 4.0

        self.time_since_last_attack = 0.0
        self.time_between_attack = 3.0

        self.physics_engine = None

    def setup(self):
        self.camera = arcade.Camera(self.window.width,self.window.height)

        self.gui_camera = arcade.Camera(self.window.width,self.window.height)

        layer_option = {
            LAYER_NAME_PLATFORM: {
                'use_spatial_hash': True
            }
        }

        map_path = f'{GAME_DIRECTORY}\\level\\testing_world.tmx'
        self.tile_map = arcade.load_tilemap(
            map_file=map_path,scaling = TILE_SCALING,layer_options=layer_option
            )
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player_sprite = object_initialize.Player_Model()
        self.player_sprite.center_x = 4 * TILE_SIZE
        self.player_sprite.center_y = 4 * TILE_SIZE

        self.scene.add_sprite(LAYER_NAME_PLAYER,self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms = self.scene[LAYER_NAME_PLATFORM],
            gravity_constant = GRAVITY
        )
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.setup()

    def on_draw(self):
        self.clear()
        
        self.scene.draw()

        self.camera.use()

def main():
    window = arcade.Window(width=SCREEN_WIDTH,height=SCREEN_HEIGHT)
    game = GameView()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()