import arcade
import model_render

class number_level(model_render.game()):
    def __init__(self,level):
        self.level = level
        self.background = []
        self.player_sprite = []
        self.background_object = []
        self.imovable_object = []

    def level_background(self,background_image):
        self.image = background_image
    def level_player(self,x_position,y_position,player_sprite):
        pass
    def level_background_object(self,background_object):
        self.background_object = []
        self.background_object.append(background_object)
    def level_imovable_object(self):
        self.