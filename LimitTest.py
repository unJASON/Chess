from pure.MTCS_AI_v2 import AI_mcst_v2
from Board import Board
import Const
board = Board(width = Const.total_step,height = Const.total_step)

#测试纯跑AI的效率
ai = AI_mcst_v2(board,n_in_row=Const.n_in_row,time=6)
click_x, click_y = ai.putChess(Const.Mode_Local_GUI,[Const.player['black'], Const.player['white']],[],[])
print(ai.cnt)
print("done")