import random
# from GUI_learning import stepLength
abs_x = 32
abs_y = 32
stepLength = 35
def putChess():
    x = abs_x + random.randint(0,15)*stepLength
    y = abs_y + random.randint(0,15)*stepLength
    return x,y
