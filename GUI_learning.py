import tkinter as tk
from Local_AI import AI_mcst
from Local_AI_v1 import AI_mcst_v1
from Board import Board
import Const
# 定义重置按钮的功能
def gameReset():
    global person_flag, coor_black, coor_white, piece_color
    person_flag = 1  # 打开落子开关
    # var.set("执黑棋")  # 还原提示标签
    var1.set("")  # 还原输赢提示标签
    var2.set("")  # 还原游戏结束提示标签
    showChange("black")  # 还原棋子提示图片
    chessBorard.delete("piece")  # 删除所有棋子
    coor_black = []  # 清空黑棋坐标存储器
    coor_white = []  # 清空白棋坐标存储器
black_win = 0
white_win = 0
def trainAI():
    global click_x,click_y,black_win,white_win
    total = 1
    i = 0

    while i< total:
        gameReset()
        is_full = False
        while(1):
            click_x, click_y = ai.putChess([Const.player['black'], Const.player['white']], coor_black, coor_white)
            flag, is_win1 = coorJudge()
            if is_win1:
                black_win = black_win + 1
                break
            #棋盘满了
            if coor_black.__len__() + coor_white.__len__() >= Const.total_step * Const.total_step:
                is_full = True
                break
            click_x, click_y = ai_2.putChess([Const.player['white'], Const.player['black']], coor_black, coor_white)
            flag, is_win2 = coorJudge()
            if is_win2:
                white_win = white_win + 1
                break
            # 棋盘满了
            if coor_black.__len__() + coor_white.__len__() >= Const.total_step * Const.total_step:
                is_full = True
                break
        i = i + 1

        print("i:"+ str(i))
    print("black_win:"+str(black_win))
    print("white_win:"+str(white_win))
    pass
# 右上方的棋子提示（工具）
def showChange(color):
    global piece_color
    piece_color = color
    side_canvas.delete("show_piece")
    side_canvas.create_oval(150 - Const.piece_size, 25 - Const.piece_size,
                            150 + Const.piece_size, 25 + Const.piece_size,
                            fill=piece_color, tags=("show_piece"))


# 输赢的提示、游戏结束的提示（工具）
def pushMessage():
    if person_flag == -1:
        var1.set("白棋赢")
    elif person_flag == 1:
        var1.set("黑棋赢")
    var2.set("游戏结束")


# 棋子的计数（工具）
def piecesCount(coor, pieces_count, t1, t2):
    for i in range(1, 5):
        (x, y) = (click_x + t1 * Const.stepLength * i, click_y + t2 * Const.stepLength * i)
        if (x, y) in coor:
            pieces_count += 1
        else:
            break
    return pieces_count


# 事件监听处理
signal = 0
def coorBack(event):  # return coordinates of cursor 返回光标坐标
    global click_x, click_y
    click_x = event.x
    click_y = event.y
    flag,is_win =coorJudge()
    #AI逻辑
    if flag and not is_win:
        click_x,click_y=ai_2.putChess([Const.player['white'],Const.player['black'] ],coor_black,coor_white)
        flag2,is_win2 = coorJudge()

        # #放成功为止
        # while not flag2:
        #     click_x, click_y = ai.putChess([2,1],coor_black,coor_white)
        #     flag2, is_win2 = coorJudge()
        #     if is_win2:
        #         break



'''判断输赢的逻辑'''


# preJudge调用realJudge0，realJudge0调用realJudge1和realJudge2；
# realJudge1负责横纵两轴的计数，realJudge2负责两斜线方向的计数
# realJudge0汇总指定颜色棋子结果，作出决策，判断是否游戏结束
# preJudge决定是判断黑棋还是判断白棋，对两种颜色的棋子判断进行导流
def preJudge(piece_color):
    if piece_color == "black":
        return realJudge0(coor_black)
    elif piece_color == "white":
        return realJudge0(coor_white)


def realJudge0(coor):
    global person_flag, person_label

    if realJudge1(coor) == 1 or realJudge2(coor) == 1:
        pushMessage()
        person_flag = 0
        return True
    return False


def realJudge1(coor):
    pieces_count = 0
    pieces_count = piecesCount(coor, pieces_count, 1, 0)  # 右边
    pieces_count = piecesCount(coor, pieces_count, -1, 0)  # 左边
    # if pieces_count >= 4:
    if pieces_count >= Const.n_in_row-1:
        return 1
    else:
        pieces_count = 0
        pieces_count = piecesCount(coor, pieces_count, 0, -1)  # 上边
        pieces_count = piecesCount(coor, pieces_count, 0, 1)  # 下边
        # if pieces_count >= 4:
        if pieces_count >= Const.n_in_row - 1:
            return 1
        else:
            return 0


def realJudge2(coor):
    pieces_count = 0
    pieces_count = piecesCount(coor, pieces_count, 1, 1)  # 右下角
    pieces_count = piecesCount(coor, pieces_count, -1, -1)  # 左上角
    # if pieces_count >= 4:
    if pieces_count >= Const.n_in_row - 1:
        return 1
    else:
        pieces_count = 0
        pieces_count = piecesCount(coor, pieces_count, 1, -1)  # 右上角
        pieces_count = piecesCount(coor, pieces_count, -1, 1)  # 左下角
        # if pieces_count >= 4:
        if pieces_count >= Const.n_in_row - 1:
            return 1
        else:
            return 0


'''落子的逻辑'''


# 落子
def putPiece(piece_color):
    global coor_black, coor_white
    chessBorard.create_oval(click_x - Const.piece_size, click_y - Const.piece_size,
                       click_x + Const.piece_size, click_y + Const.piece_size,
                       fill=piece_color, tags=("piece"))
    if piece_color == "white":
        coor_white.append((click_x, click_y))
    elif piece_color == "black":
        coor_black.append((click_x, click_y))
    preJudge(piece_color)  # 每放置一枚棋子就对该种颜色的棋子进行一次判断


# 找出离鼠标点击位置最近的棋盘线交点，调用putPiece落子
def coorJudge():
    global click_x, click_y
    coor = coor_black + coor_white
    global person_flag, show_piece
    # print("x = %s, y = %s" % (click_x, click_y))
    item = chessBorard.find_closest(click_x, click_y)
    tags_tuple = chessBorard.gettags(item)
    if len(tags_tuple) > 1:
        tags_list = list(tags_tuple)
        coor_list = tags_list[:2]
        try:
            for i in range(len(coor_list)):
                coor_list[i] = int(coor_list[i])
        except ValueError:
            pass
        else:
            # 离太远的话就算了
            if abs(coor_list[0] - click_x) >= Const.stepLength or abs(coor_list[1] - click_y) >= Const.stepLength:
                return False, False

            coor_tuple = tuple(coor_list)
            (click_x, click_y) = coor_tuple
            # print("tags = ", tags_tuple, "coors = ", coor_tuple)
            if ((click_x, click_y) not in coor) and (click_x in Const.pieces_x[:Const.total_step]) and (click_y in Const.pieces_y[:Const.total_step]):
                # print("True")
                if person_flag != 0:
                    if person_flag == 1:
                        putPiece("black")
                        showChange("white")
                        # var.set("执白棋")
                        is_win=preJudge("black")
                    elif person_flag == -1:
                        putPiece("white")
                        showChange("black")
                        is_win = preJudge("white")
                        # var.set("执黑棋")
                    person_flag *= -1
                    return True,is_win
    return False,False
#黑棋位置
coor_black = []
#白棋位置
coor_white = []
person_flag = 1
root = tk.Tk()
#AI初始化
board = Board(width = Const.total_step,height = Const.total_step)
ai = AI_mcst(board,n_in_row=Const.n_in_row, time=15)
ai_2 = AI_mcst_v1(board,n_in_row=Const.n_in_row,time=15)

#先画棋盘
chessBorard = tk.Canvas(root,bg = "saddlebrown",width=Const.chessBoardSize[0], height=Const.chessBoardSize[1])
chessBorard.grid(row=0, column=1, rowspan=6)
# 线条
for i in range(Const.total_step):
    chessBorard.create_line(Const.abs_zero[0], (Const.stepLength * i + Const.abs_zero[1]), Const.abs_zero[0]+(Const.total_step-1)*Const.stepLength, (Const.stepLength * i + Const.abs_zero[1]))
    chessBorard.create_line((Const.stepLength * i + Const.abs_zero[0]), Const.abs_zero[1], (Const.stepLength * i + Const.abs_zero[0]), Const.abs_zero[1]+(Const.total_step-1)*Const.stepLength)
# 透明棋子（设置透明棋子，方便后面落子的坐标定位到正确的位置）
for i in Const.pieces_x[:Const.total_step]:
    for j in Const.pieces_y[:Const.total_step]:
        chessBorard.create_oval(i - Const.piece_size, j - Const.piece_size,
                           i + Const.piece_size, j + Const.piece_size,
                           width=0, tags=(str(i), str(j)))
chessBorard.bind("<Button-1>", coorBack)  # 鼠标单击事件绑定

#显示当前棋手
side_canvas = tk.Canvas(root, width=220, height=50,bg = 'gray' )
side_canvas.grid(row=7, column=1)
side_canvas.create_text(70,25,font=("Arial", 20),text="当前玩家:")
side_canvas.create_oval(150 - Const.piece_size, 25 - Const.piece_size,
                        150 + Const.piece_size, 25 + Const.piece_size,
                        fill=Const.piece_color_black, tags=("show_piece"))


playerOne_canvas = tk.Canvas(root, width=220, height=50,bg = 'gray' )
playerOne_canvas.grid(row=1, column=0)
playerOne_canvas.create_text(50,25,font=("Arial", 20),text="玩家1:")
playerOne_canvas.create_oval(150 - Const.piece_size, 25 - Const.piece_size,
                        150 + Const.piece_size, 25 + Const.piece_size,
                        fill=Const.piece_color_black, tags=("show_piece"))

playerTwo_canvas = tk.Canvas(root, width=220, height=50,bg = 'gray' )
playerTwo_canvas.grid(row=1, column=2)
playerTwo_canvas.create_text(50,25,font=("Arial", 20),text="玩家2:")
playerTwo_canvas.create_oval(150 - Const.piece_size, 25 - Const.piece_size,
                        150 + Const.piece_size, 25 + Const.piece_size,
                        fill=Const.piece_color_white, tags=("show_piece"))



"""输赢提示标签"""
var1 = tk.StringVar()
var1.set("")
result_label = tk.Label(root, textvariable=var1, width=12, height=4,
                        anchor=tk.CENTER, fg="red", font=("Arial", 25))
result_label.grid(row=4, column=0)

"""游戏结束提示标签"""
var2 = tk.StringVar()
var2.set("")
game_label = tk.Label(root,fg="red", textvariable=var2, width=12, height=4,
                      anchor=tk.CENTER, font=("Arial", 25))
game_label.grid(row=4, column=2)

"""重置按钮"""
reset_button = tk.Button(root, text="重新开始", font=20,
                         width=8, command=gameReset)
reset_button.grid(row=5, column=2)

""""AI对战"""
AI_button = tk.Button(root, text="AI对战", font=20,
                         width=8, command=trainAI)
AI_button.grid(row=6, column=2)


#窗口循环
root.mainloop()




