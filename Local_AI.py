import random
import copy
# from GUI_learning import stepLength
abs_x = 32
abs_y = 32
stepLength = 35

def putChess(coor_black,coor_white):
    coor_black_copy = copy.deepcopy(coor_black)
    coor_white_copy = copy.deepcopy(coor_white)
    x = abs_x + random.randint(0,15)*stepLength
    y = abs_y + random.randint(0,15)*stepLength
    MCTS(coor_black_copy,coor_white_copy)
    x,y=select_one_move()
    return x,y

def MCTS():
    pass
def select_one_move():
    pass