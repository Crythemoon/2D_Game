import os
import sys
import arcade
import level

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(GAME_DIRECTORY)

TILE_SCALLING = 1
CHARACTER_SCALING = 1
SPRITE_PIXEL_SIZE = 54

PLAYER_WALKING_SPEED = 0.5
GRAVITY = 2
PLAYER_JUMP_SPEED = 10

LAYER_NAME_CHARACTER = "Characters"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_FOREGROUND = "Foregrounds"
LAYER_NAME_BACKGROUND = "Backgrounds"
LAYER_NAME_ENEMY = "Enemies"
LAYER_NAME_PLAYER = "Player"

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        os.chdir(GAME_DIRECTORY)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        self.tile_map = None

        self.scene = None

        self.player_sprite_list = None
        
        self.physics_engine = None

        self.camera = None

        self.gui_camera = None

        self.end_of_map = 0

        self.level_list = []

    def setup(self):
        self.camera = arcade.Camera(self.window.width,self.window.height)
        self.gui_camera = arcade.Camera(self.window.width,self.window.height)

        room = level.level_1()
        self.level_list.append(room)

        self.current_room = 0

        self.tile_map = arcade.load_tilemap(
            self.level_list[self.current_room].map_path,
            1,
            self.level_list[self.current_room].layer_option
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite_list_after(LAYER_NAME_PLAYER,LAYER_NAME_FOREGROUND)
        
        self.player_sprite = self.level_list[self.current_room].player_sprite
        self.scene.add_sprite(LAYER_NAME_PLAYER,self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms = self.scene[LAYER_NAME_PLATFORMS],
            gravity_constant = GRAVITY
        )
    
    def on_show_view(self):
        self.setup()

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()
        