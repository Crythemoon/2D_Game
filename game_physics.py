import arcade
import model_render

MOVEMENT_SPEED = 5
class keyboard_input(model_render.game):
    def on_key_press(self,key,modifiers):
        if key == arcade.key.UP:
            