import os
import pickle

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))\

save = [
    ['saves',0],
    ['levels',1],
    ['health', 3],
    ['coin', 0]
]
file = open(f'{GAME_DIRECTORY}\\saves\\save.bin','wb')
pickle.dump(save,file)

file = open(f'{GAME_DIRECTORY}\\saves\\save.bin', 'rb')
print(pickle.load(file))