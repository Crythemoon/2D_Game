import pickle
import os

GAME_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

FILE = os.path.join(GAME_DIRECTORY,'saves','save.bin')


saves = [
    ['saves', 0],
    ['levels', 0],
    ['health', 3],
    ['coin', 0],
    ['inventory']
    ['weapon']
    ['armor']
    ['accessory']
    
]

with open(FILE, 'rb') as file:
    x = pickle.load(file)
    print(x)