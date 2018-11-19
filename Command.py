from Game import Game
from human_play import Human
from pure.MTCS_AI_v1 import AI_mcst_v1
from pure.MTCS_AI_v2 import AI_mcst_v2
from Board import Board
import Const


if __name__ == '__main__':
    board = Board(width=Const.total_step, height=Const.total_step)
    human = Human()
    huam2 = Human()
    game = Game(board)
    game.start_play(human,huam2,start_player=1,is_shown=1)




