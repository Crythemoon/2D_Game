import arcade
import os
import sys
import model_render

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.append(GAME_DIRECTORY)

PLAYER_WALKING_SPEED = 0.5

class keyboard_input(model_render.game):
    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_list[0].change_y = PLAYER_WALKING_SPEED
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