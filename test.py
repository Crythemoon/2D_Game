import os
GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
GAME_OBJECT = os.path.join(GAME_DIRECTORY,'game_object')

main_path = f'{GAME_OBJECT}\\character'
for i in range (2):
    print(f'{main_path}\\idle_character_000{i+1}.png')