import arcade
import asyncio
import os
import sys
import level
GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(GAME_DIRECTORY)
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

PLAYER_START_X = 50
PLAYER_START_Y = 100
PLAYER_WALKING_SPEED = 0.5
GRAVITY = 2
PLAYER_JUMP_SPEED = 10

TILE_SCALING = 1
SPRITE_PIXEL_SIZE = 18
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

LAYER_NAME_PLATFORMS = 'Platforms'
LAYER_NAME_FOREGROUND = "Foregrounds"
LAYER_NAME_BACKGROUND = "Backgrounds"

SCREEN_WIDTH = 810
SCREEN_HEIGHT = 612
GAME_NAME = 'Vampire Tombs'

class game(arcade.Window):
    def __init__(self,width,height,name):
        super().__init__(width,height,name)
        self.tile_map = None

        self.scene = None

        self.physics_engine = None
        
        self.camera = None

        self.gui_camera = None

        self.end_of_map = 0

        self.level = None
        
        arcade.set_background_color(arcade.color.AMAZON)

        self.player_list = None

    def setup(self,player_sprite_list,wall_sprite_list,map_path): #Game setup
        self.camera = arcade.Camera(self.width,self.height)
        self.gui_camera = arcade.Camera(self.width,self.height)

        layer_option = {
            LAYER_NAME_PLATFORMS:{
                "use_spatial_hash": True
            },
            LAYER_NAME_BACKGROUND:{
                "use_spatial_hash": False
            },
            LAYER_NAME_FOREGROUND:{
                "use_spatial_hash": False
            }
        }

        self.tile_map = arcade.load_tilemap(map_path,1,layer_option)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite_list_after("Player",LAYER_NAME_FOREGROUND)

        self.player_list = player_sprite_list
        self.scene.add_sprite("Player",self.player_list[0])

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        self.physics_engine = arcade.PhysicsEnginePlatformer(player_sprite_list[0],gravity_constant=GRAVITY,walls=self.scene["Platforms"])

    def on_draw(self):  #Game render
        arcade.start_render()
        self.player_list.draw()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()

    def center_camera_to_player(self):
        screen_center_x = self.player_list[0].center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_list[0].center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    
    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_list[0].change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_list[0].change_y = -PLAYER_WALKING_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_list[0].change_x = -PLAYER_WALKING_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_list[0].change_x = PLAYER_WALKING_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_list[0].change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_list[0].change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_list[0].change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_list[0].change_x = 0

    def update(self,delta_time):    #Game logic
        self.player_list.update()
        self.player_list.update_animation()
        self.physics_engine.update()
        self.center_camera_to_player()

        
async def main():
    start = game(SCREEN_WIDTH,SCREEN_HEIGHT,GAME_NAME)
    level1 = await level.level_1()
    start.setup(level1.player_sprite_list,level1.wall_sprite_list,level1.map_path)

    arcade.run()
asyncio.run(main())