import os
import sys
import arcade
import arcade.gui
from arcade.gui.events import UIOnClickEvent
import level
import object_initialize
import math
from typing import Optional
import pickle

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(GAME_DIRECTORY)
GAME_SAVES = os.path.join(GAME_DIRECTORY,'saves')

WINDOW_WIDTH = 1620
WINDOW_HEIGHT = 810

SAVE_BINARY = 0
LEVEL_BINARY = 1
HEALTH_BINARY = 2
COIN_BINARY = 3

TILE_SCALLING = 1
CHARACTER_SCALING = 1
TILE_PIXEL_SIZE = 54

SCREEN_TILES_WIDTH = 30
SCREEN_TILES_HEIGHT = 15

UPDATE_PER_FRAME = 20

PLAYER_WALKING_SPEED = 0.5
PLAYER_RUNNING_SPEED = 1
PLAYER_CLIMBING_SPEED = 0.5
PLAYER_JUMP_SPEED = 10
PLAYER_DASH_SPEED = 10

RIGHT_FACING = 0
LEFT_FACING = 1

GRAVITY = 2

LAYER_NAME_FLAG = "Flag"
LAYER_NAME_NPC = "NPC"
LAYER_NAME_COIN = "Coin"
LAYER_NAME_HEART = "Heart"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_LADDER = "Ladders"
LAYER_NAME_ENEMY = "Enemy"
LAYER_NAME_DYNAMIC_PLATFORM = "Dynamic Platforms"
LAYER_NAME_PLATFORM = "Platforms"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DEATH_ZONE = "Death Zone"
LAYER_NAME_PLAYER = "Player"

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.WHITE)

        os.chdir(GAME_DIRECTORY)

        self.tile_map = None
        self.scene = None

        self.level = None
        self.health = None
        self.coin = None

        self.level_list = [level.level1]

        self.player_sprite_list = None
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

        self.time_between_dash = 0.0
        self.dash_cooldown = 4.0

        self.time_since_last_attack = 0.0
        self.time_between_attack = 3.0

        self.physics_engine = None

    def load_level(self):
        with open(f'{GAME_SAVES}\\save.bin', 'rb') as file:
            x = pickle.load(file)
            self.level_number = x[LEVEL_BINARY][1]
            self.health = x[HEALTH_BINARY][1]
            self.coin = x[COIN_BINARY][1]
            file.close()
        
        self.level = self.level_list[self.level_number]

    def setup(self):
        self.load_level()

        self.camera = arcade.Camera(self.window.width, self.window.height)

        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        layer_option = self.level.layer_option      #MAP
        self.tile_map = arcade.load_tilemap(map_file=self.level.map_path,scaling=TILE_SCALLING,layer_options=layer_option)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMY]        #ENEMY_SPRITE
        for my_object in enemies_layer:
            cartesians = self.tile_map.get_cartesian(
                my_object.shape[0],my_object.shape[1]
            )
            enemy_type = my_object.properties["type"]
            if enemy_type == "bat":
                enemy = object_initialize.BatEnemy()
            enemy.center_x = math.floor(
                (cartesians[0] * TILE_SCALLING * self.tile_map.tile_width)
            )
            enemy.center_y = math.floor(
                (cartesians[1] + 1) * TILE_SCALLING * self.tile_map.tile_height
            )

            if "boundary_left" in my_object.properties:
                enemy.boundary_left = my_object.properties["boundary_left"]
            if "boundary_right" in my_object.properties:
                enemy.boundary_right = my_object.properties["boundary_right"]
            if "change_x" in my_object.properties:
                enemy.change_x = my_object.properties["change_x"]
            self.scene.add_sprite(LAYER_NAME_ENEMY,enemy)
        
        self.player_sprite_list = arcade.SpriteList()       #PLAYER_SPRITE

        self.player_sprite = object_initialize.Player_Model()
        self.player_sprite.center_x = self.level.player_sprite_center_x
        self.player_sprite.center_y = self.level.player_sprite_center_y

        self.player_sprite_list.append(self.player_sprite)

        self.scene.add_sprite_list_after(
            name= LAYER_NAME_PLAYER,
            after=LAYER_NAME_LADDER,
            sprite_list=self.player_sprite_list
            )

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms = self.scene[LAYER_NAME_DYNAMIC_PLATFORM],
            gravity_constant = GRAVITY,
            ladders = self.scene[LAYER_NAME_LADDER],
            walls = self.scene[LAYER_NAME_PLATFORM]
        )

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        self.clear()

        self.scene.draw()

        self.camera.use()

    def process_keychange(self):
        if self.up_pressed and not self.down_pressed:           #LADDER KEYCHANGE
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_CLIMBING_SPEED
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_CLIMBING_SPEED

        if self.physics_engine.is_on_ladder():
            if (
                not self.up_pressed
                and not self.down_pressed
            ):
                self.player_sprite.change_y = 0
            elif (
                self.up_pressed
                and self.down_pressed
            ):
                self.player_sprite.change_y = 0
        
        if self.space_pressed:          #JUMP KEYCHANGE
            if (
                not self.physics_engine.is_on_ladder()
                and self.physics_engine.can_jump(y_distance = 10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        if self.shift_pressed:          #RUNNING KEYCHANGE
            player_speed = PLAYER_RUNNING_SPEED
        elif not self.shift_pressed:
            player_speed = PLAYER_WALKING_SPEED
        
        if self.right_pressed and not self.left_pressed:            #MOVING KEYCHANGE
            self.player_sprite.change_x = player_speed
        elif not self.right_pressed and self.left_pressed:
            self.player_sprite.change_x = -player_speed
        elif not self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = 0

        if (                            #DASHING KEYCHANGE
            self.f_pressed
            and self.player_sprite.character_face_direction == RIGHT_FACING
            and not self.dash_needs_reset
        ):
            self.player_sprite.center_x = self.player_sprite.center_x + PLAYER_DASH_SPEED
            self.dash_needs_reset = True

        if (
            self.f_pressed
            and self.player_sprite.character_face_direction == LEFT_FACING
            and not self.dash_needs_reset
        ):
            self.player_sprite.center_x = self.player_sprite.center_x - PLAYER_DASH_SPEED


    def on_key_press(self,key,modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.SPACE:
            self.space_pressed = True
        elif key == arcade.key.F:
            self.f_pressed = True
        elif key == arcade.key.MOD_SHIFT:
            self.shift_pressed = True
        elif key == arcade.key.J:
            self.attack_pressed = True
        elif key == arcade.key.K:
            self.spell_pressed = True

        self.process_keychange()

    def on_key_release(self,key,modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.SPACE:
            self.space_pressed = False
        elif key == arcade.key.F:
            self.f_pressed = False
        elif key == arcade.key.MOD_SHIFT:
            self.shift_pressed = False
        elif key == arcade.key.J:
            self.attack_pressed = False
        elif key == arcade.key.K:
            self.spell_pressed = False

        self.process_keychange()

    def center_camera_to_player(self):
        screen_center_x = self.camera.scale * (self.player_sprite.center_x - (self.camera.viewport_width / 2))
        screen_center_y = self.camera.scale * (self.player_sprite.center_y) - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_center = (screen_center_x,screen_center_y)
        self.camera.move_to(player_center)

    def on_update(self,delta_time):
        self.physics_engine.update()

        if self.dash_needs_reset:
            self.time_since_last_dash += delta_time
            if self.time_since_last_dash >= self.time_between_dash:
                self.time_since_last_dash = 0.0
                self.dash_needs_reset = False

        if self.physics_engine.is_on_ladder and not self.physics_engine.can_jump:
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        if self.dash_needs_reset:
            self.time_between_dash += UPDATE_PER_FRAME
            if self.time_between_dash == self.dash_cooldown:
                self.time_between_dash = 0
                self.dash_needs_reset = False

        self.scene.update_animation(                #SCENE ANIMATION UPDATE
            delta_time,
            [
                LAYER_NAME_ENEMY,
                LAYER_NAME_PLAYER
            ],
        )

        self.scene.update(
            names=[
                LAYER_NAME_ENEMY,
                LAYER_NAME_PLAYER
                ]
        )
        for enemy in self.scene[LAYER_NAME_ENEMY]:
            if enemy.right > enemy.boundary_right and enemy.change_x > 0:
                enemy.change_x *= -1
            if enemy.left < enemy.boundary_left and enemy.change_x < 0:
                enemy.change_x *= -1

        self.center_camera_to_player()


def main():
    window = arcade.Window(width=WINDOW_WIDTH,height=WINDOW_HEIGHT,title="Test")
    game = GameView()
    window.show_view(game)
    arcade.run()

main()