import random
import copy
# from GUI_learning import stepLength
abs_x = 32
abs_y = 32
stepLength = 35
class AI:
    def __init__(self,**kwargs):

        # self.board = board
        self.player = [1, 2]  # player1 and player2
        self.n_in_row = int(kwargs.get('n_in_row', 5))
        self.time = float(kwargs.get('time', 5))
        self.max_actions = int(kwargs.get('max_actions', 1000))

    def putChess(self,play_turn,coor_black,coor_white):
        coor_black_copy = copy.deepcopy(coor_black)
        coor_white_copy = copy.deepcopy(coor_white)
        play_turn_copy = copy.deepcopy(play_turn)
        x = abs_x + random.randint(0,15)*stepLength
        y = abs_y + random.randint(0,15)*stepLength
        MCTS(play_turn_copy,coor_black_copy,coor_white_copy)
        x,y=select_one_move()
        return x,y

    def MCTS(self,play_turn,coor_black_copy,coor_white_copy):
        pass
    def select_one_move(self,play_turn,coor_black_copy,coor_white_copy):
        pass