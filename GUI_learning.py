import tkinter as tk

chessBoardSize=(540,540)
abs_zero = (32,32)
stepLength = 35
total_step = 15
coord = 10, 50, 240, 210
pieces_x = [i for i in range(abs_zero[0], abs_zero[0]+523, stepLength)]
pieces_y = [i for i in range(abs_zero[1], 529, stepLength)]
root = tk.Tk()


#先画棋盘
chessBorard = tk.Canvas(root,bg = "saddlebrown",width=chessBoardSize[0], height=chessBoardSize[1])
chessBorard.grid(row=0, column=0, rowspan=6)
# 线条
for i in range(total_step):
    chessBorard.create_line(abs_zero[0], (stepLength * i + abs_zero[1]), abs_zero[0]+(total_step-1)*stepLength, (stepLength * i + abs_zero[1]))
    chessBorard.create_line((stepLength * i + abs_zero[0]), abs_zero[1], (stepLength * i + abs_zero[0]), abs_zero[1]+(total_step-1)*stepLength)
# 透明棋子（设置透明棋子，方便后面落子的坐标定位到正确的位置）
for i in pieces_x:
    for j in pieces_y:
        chessBorard.create_oval(i - PIECE_SIZE, j - PIECE_SIZE,
                           i + PIECE_SIZE, j + PIECE_SIZE,
                           width=0, tags=(str(i), str(j)))
#窗口循环
root.mainloop()