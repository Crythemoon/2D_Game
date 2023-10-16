import arcade
import os
import sys
import object_initialize

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
sys.path.append(GAME_DIRECTORY)

SCREEN_WIDTH = 1680
SCREEEN_HEIGHT = 1080

class CutScene(arcade.View):
    def __init__(self,level):
        super().__init__()
        self.level = level
        self.texture_list = None
        self.text_list = None
        self.next_scene = True
        self.scene = 0

    def setup(self,character_texture,text_bubble_texture,text_list):
        self.texture_list = arcade.SpriteList()

        character = character_texture
        self.texture_list.append(character)

        text_bubble = text_bubble_texture
        self.texture_list.append(text_bubble)

        self.text_list = text_list

    def on_draw(self):
        text = self.text_list[self.scene]
        self.texture_list.draw()
        if self.next_scene:
            arcade.draw_text(
                text,
                50,
                50
            )
            self.next_scene = False
            self.scene += 1

    def on_key_press(self, key,modifers):
        if key == arcade.key.SPACE:
            self.next_scene = True


def main():
    window = arcade.Window(SCREEN_WIDTH,SCREEEN_HEIGHT)
    scene = CutScene(1)
    text_list = ("Hello World","This is a test")
    scene.setup(object_initialize.TutorialCharacter(),object_initialize.texture_bubble(),text_list)
    window.show_view(scene)
    arcade.run()

if __name__ == "__main__":
    main()