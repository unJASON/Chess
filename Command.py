from Game import Game
from Board import Board
import Const


if __name__ == '__main__':
    board = Board(width=Const.total_step, height=Const.total_step)
    ai = AI_mcst(board, n_in_row=Const.n_in_row, time=15)
    ai_2 = AI_mcst_v2(board, n_in_row=Const.n_in_row, time=15)