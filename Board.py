import Const
#将棋盘抽象出来
class Board(object):
    def __init__(self,**kwargs):
        # 棋盘长宽
        self.width = int(kwargs.get("width", 5))
        self.height = int(kwargs.get("height", 5))
        self.currentState = []
        self.availables = list(range(self.width * self.height))  # available moves
        self.states = {}
        self.player_action ={}
        self.player_action[Const.player['black']] = [(l,Const.player['black'] ) for l in self.availables]
        self.player_action[Const.player['white']] = [(l,Const.player['white'] ) for l in self.availables]
        pass

    # 模拟棋盘现状,需要重新初始化一下borad
    def putBoard(self, coor_black, coor_white):
        self.states = {}
        self.availables = list(range(self.width * self.height))  # available moves
        for i in coor_black:
            self.update(Const.player['black'], i)
        for i in coor_white:
            self.update(Const.player['white'], i)

    def update(self, player, move):
        self.states[move] = player
        self.availables.remove(move)
        self.player_action[Const.player['black']].remove( (move,Const.player['black']))
        self.player_action[Const.player['white']].remove( (move,Const.player['white']) )
        self.currentState.append((move,player))

    #慢！
    def current_state(self):
        # return tuple((m, self.states[m]) for m in sorted(self.states))  # for hash
        return tuple(self.currentState)
    def get_player_action(self,player):
        return self.player_action[player]