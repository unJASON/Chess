import tkinter as tk

coord = 10, 50, 240, 210
root = tk.Tk()


# 创建一个Canvas，设置其背景色为白色
cv = tk.Canvas(root,bg = 'white')
# 创建一个矩形，坐标为(10,10,110,110)
cv.create_rectangle(10,10,110,110)
cv.pack()
root.mainloop()
# 为明显起见，将背景色设置为白色，用以区别 root
root.mainloop()