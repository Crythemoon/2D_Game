import os
import sys
import arcade
import arcade.gui
from arcade.gui.events import UIOnClickEvent
import level
from typing import Optional
import pickle

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(GAME_DIRECTORY)

SAVE_BINARY = 0
LEVEL_BINARY = 1
HEALTH_BINARY = 2
COIN_BINARY = 3

TILE_SCALLING = 1
CHARACTER_SCALING = 1
TILE_PIXEL_SIZE = 54

PLAYER_WALKING_SPEED = 0.5
PLAYER_RUNNING_SPEED = 1
PLAYER_CLIMBING_SPEED = 0.5
GRAVITY = 2
PLAYER_JUMP_SPEED = 10

LAYER_NAME_CHARACTER = "Characters"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_FOREGROUND = "Foregrounds"
LAYER_NAME_BACKGROUND = "Backgrounds"
LAYER_NAME_ENEMY = "Enemies"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_JUMPABLE_PLATFORM = "Jump Platforms"
        
class Menu(arcade.View):
    def __init__(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.WHITE)

        self.v_box = arcade.gui.UIBoxLayout()
        
        new_game_button = arcade.gui.UIFlatButton(text="New Game", width = 200)
        self.v_box.add(new_game_button.with_space_around(bottom=20))

        continue_button = arcade.gui.UIFlatButton(text="Continue", width=200)
        with open(f'{GAME_DIRECTORY}\\saves\\save.bin', 'rb') as file:
            x = pickle.load(file)
            if x[SAVE_BINARY][1] == 1:
                self.v_box.add(continue_button.with_space_around(bottom=20))
            file.close()
        
        quit_button = arcade.gui.UIFlatButton(text="Quit",width=200)
        self.v_box.add(quit_button)

        new_game_button.on_click = self.on_click_newgame
        continue_button.on_click = self.on_click_continue
        quit_button.on_click = self.on_click_quit

    def on_click_newgame(self):
        saves = [
            ['saves', 0],
            ['levels', 0],
            ['health' , 3],
            ['coin', 0]
        ]
        with open(f'{GAME_DIRECTORY}\\saves\\save.bin', 'rb') as file:
            x = pickle.load(file)
            if x[SAVE_BINARY][1] == 1:
                with open(f'{GAME_DIRECTORY}\\saves\\save.bin', 'wb') as file:
                    pickle.dump(saves,file)
            file.close()
        game_view = GameView()
        self.window.show_view(game_view)

    def on_click_continue(self):
        game_view = GameView()
        self.window.show_view(game_view)

    def on_click_quit(self):
        arcade.exit()

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        os.chdir(GAME_DIRECTORY)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.attack_pressed = False
        self.jump_needs_reset = False

        self.tile_map = None

        self.scene = None

        self.player_sprite: Optional(arcade.Sprite) = None
        self.NPC_sprite_list: Optional(arcade.SpriteList) = None
        self.foregound_sprite_list: Optional(arcade.SpriteList) = None
        self.enemies_sprite_list: Optional(arcade.SpriteList) = None
        self.dynamic_platform_sprite_list: Optional(arcade.SpriteList) = None
        self.platform_sprite_list: Optional(arcade.SpriteList) = None

        self.health = None
        self.coin = None

        self.tile_map = None
        self.scene = None
        
        self.physics_engine: Optional(arcade.PymunkPhysicsEngine)

        self.level_list = (level.level1(),level.level2())

        self.level = None

        self.end_of_map = 0

        self.camera: Optional(arcade.Camera) = None

        self.gui_camera: Optional(arcade.Camera) = None

    def load_level(self):
        with open(f'{GAME_DIRECTORY}\\saves\\save.bin', 'rb') as file:
            x = pickle.load(file)
            self.level = x[LEVEL_BINARY][1]
            self.health = x[HEALTH_BINARY][1]
            self.coin = x[COIN_BINARY][1]
            file.close()

        self.tile_map = arcade.load_tilemap(self.level_list[self.level].map_path,scaling=TILE_SCALLING)

        self.end_of_map = self.tile_map.width * TILE_PIXEL_SIZE
        

    def setup(self):
        self.camera = arcade.Camera(self.window.width,self.window.height)
        self.gui_camera = arcade.Camera(self.window.width,self.window.height)

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()

    def process_keychange(self):

        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_CLIMBING_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_CLIMBING_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_WALKING_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_WALKING_SPEED
        else:
            self.player_sprite.change_x = 0

        if self.right_pressed and self.shift_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_RUNNING_SPEED
        elif self.left_pressed and self.shift_pressed and not self.right_pressed:
            self.player_sprite.change_x = PLAYER_RUNNING_SPEED
        elif self.right_pressed and self.shift_pressed and self.left_pressed:
            self.player_sprite.change_x = 0

        

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.MOD_SHIFT:
            self.shift_pressed = True

        if key == arcade.key.PLUS:
            self.camera.zoom(0.01)
        elif key == arcade.key.MINUS:
            self.camera.zoom(-0.01)

        self.process_keychange()

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.MOD_SHIFT:
            self.shift_pressed = False

        self.process_keychange()

    def on_mouse_scroll(self, x, y, scroll_x,scroll_y):
        self.camera.zoom(-0.01 *scroll_y)
    
    def center_camera_to_player(self, speed = 0.2):
        screen_center_x = self.camera.scale * (self.player_sprite.center_x - (self.camera.viewport_width / 2))
        screen_center_y = self.camera.scale * (self.player_sprite.center_y - (self.camera.viewport_height / 2))
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = (screen_center_x, screen_center_y)    

        self.camera.move_to(player_centered, speed)

    def on_update(self,delta_time):
        self.physics_engine.update()

        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_BACKGROUND,
                LAYER_NAME_CHARACTER,
                LAYER_NAME_FOREGROUND,
                LAYER_NAME_ENEMY,
                LAYER_NAME_CHARACTER,
                LAYER_NAME_PLAYER
            ]
        )

        self.scene.update(
            [LAYER_NAME_ENEMY,LAYER_NAME_CHARACTER]
        )