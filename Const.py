player = {'black':1,'white':2}

#棋子像素大小
piece_size = 10

#棋盘像素大小
chessBoardSize=(540,540)

#绝对零点所在像素
abs_zero = (32,32)
#每个棋子间间隔
stepLength = 35

#共15条线
total_step = 10

piece_color_black = "black"
piece_color_white = "white"

#连成5子赢
n_in_row = 5



pieces_x = [i for i in range(abs_zero[0], abs_zero[0]+523, stepLength)]
pieces_y = [i for i in range(abs_zero[1], 529, stepLength)]

Mode_Local_GUI = 1