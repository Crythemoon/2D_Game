import arcade
import asyncio
import os
import sys
import object_initialize

GAME_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(GAME_DIRECTORY)
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

LAYER_NAME_NPC = "NPC"
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_FOREGROUND = "Foregrounds"
LAYER_NAME_BACKGROUND = "Backgrounds"
LAYER_NAME_ENEMY = "Enemies"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_JUMPABLE_PLATFORM = "Jump Platforms"

class level_1(arcade.View):
    def __init__(self):
        super().__init__()
        