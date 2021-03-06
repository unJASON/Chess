"""修改胜利判断条件,base on v1"""
import random
import copy
import time
import Const
import numpy as np
from random import choice, shuffle
from math import log, sqrt
from abs_AI import abs_AI



class AI_mcst_v2(abs_AI):
    def __init__(self,board,**kwargs):
        self.cnt = 0
        self.board = board
        # self.player = [1, 2]  # player1 and player2
        self.n_in_row = int(kwargs.get('n_in_row', 5))
        self.calculation_time = float(kwargs.get('time', 5))
        self.max_actions = int(kwargs.get('max_actions', 1000))



        self.confident = 1.96
        #RAVE
        self.equivalence = 1000
        self.max_depth = 1

        self.plays = {}  # key:(action, state), value:visited times
        self.wins = {}  # key:(action, state), value:win times
        self.plays_rave = {}  # key:(move, state), value:visited times
        self.wins_rave = {}  # key:(move, state), value:{player: win times}


    def putChess(self,mode,play_turn,coor_black,coor_white):
        self.player = play_turn[0]
        coor_white = self.trans_cor2abs(coor_white,self.board.width)
        coor_black = self.trans_cor2abs(coor_black,self.board.width)
        #模拟棋盘现状
        self.board.putBoard(coor_black,coor_white)
        simulations = 0
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            play_turn_copy = copy.deepcopy(play_turn)
            board_copy = copy.deepcopy(self.board)
            self.run_simulation(play_turn_copy,board_copy)
            simulations = simulations + 1
        print("total simulations=", simulations)
        move=self.select_one_move()
        coord_x,coord_y = self.locate_move(move)
        print('Maximum depth searched:', self.max_depth)
        print("AI move: %d,%d\n" % (move//self.board.width, move % self.board.width))
        print("before prune:" + str(self.plays_rave.__len__()))
        self.prune()
        print("after prune:"+str(self.plays_rave.__len__()))
        return coord_x,coord_y
    def locate_move(self,move):
        x = move//self.board.width
        y = move % self.board.width
        coord_x = Const.abs_zero[0] + x * Const.stepLength
        coord_y = Const.abs_zero[1] + y * Const.stepLength
        return coord_x,coord_y

    def trans_cor2abs(self,coords, width):
        if coords.__len__() == 0:
            return coords
        code = []
        for coord in coords:
            code.append(int((coord[0] - Const.abs_zero[0]) / Const.stepLength * width
                            + (coord[1] - Const.abs_zero[1]) / Const.stepLength))
        return code


    def run_simulation(self,play_turn,board):
        """
                UCT RAVE main process
                """
        plays = self.plays
        wins = self.wins
        plays_rave = self.plays_rave
        wins_rave = self.wins_rave
        player = self.get_player(play_turn)

        availables = board.availables

        visited_states = set()
        winner = -1
        expand = True
        states_list = []
        # Simulation
        for t in range(1, self.max_actions + 1):
            self.cnt = self.cnt + 1
            # Selection
            # if all moves have statistics info, choose one that have max UCB value
            state = board.current_state()
            """modified"""
            # actions = [(move, player) for move in availables]
            actions = board.get_player_action(player)

            action = self.expands(plays,actions,wins,wins_rave,player,plays_rave,state)
            move, p = action
            board.update(player, move)

            # Expand
            # add only one new child node each time
            if expand and (action, state) not in plays:
                expand = False
                plays[(action, state)] = 0
                wins[(action, state)] = 0

                if t > self.max_depth:
                    self.max_depth = t

            states_list.append((action, state))  # states in one simulation by order of visited
            # for i, (m_root, s_root) in enumerate(states_list):
            #     for (m_sub, s_sub) in states_list[i:]:
            #         if (m_sub, s_root) not in plays_rave:
            #             plays_rave[(m_sub, s_root)] = 0
            #             wins_rave[(m_sub, s_root)] = {}
            #             for p in self.play_turn:
            #                 wins_rave[(m_sub, s_root)][p] = 0

            # AMAF value
            # next (action, state) is child node of all previous (action, state) nodes
            for (m, pp), s in states_list:
                if (move, s) not in plays_rave:
                    plays_rave[(move, s)] = 0
                    wins_rave[(move, s)] = {}
                    for p in play_turn:
                        wins_rave[(move, s)][p] = 0
            visited_states.add((action, state))

            is_full = not len(availables)
            win, winner = self.has_a_winner(board,action)
            if is_full or win:
                break
            player = self.get_player(play_turn)
        # Back-propagation
        self.backpropagation(states_list,plays,winner,wins,plays_rave,wins_rave)


    def expands(self,plays,actions,wins,wins_rave,player,plays_rave,state):
        if all(plays.get((action, state)) for action in actions):
            total = 0
            for a, s in plays:
                if s == state:
                    total += plays.get((a, s))  # N(s)
            beta = self.equivalence / (3 * total + self.equivalence)

            value, action = max(
                ((1 - beta) * (wins[(action, state)] / plays[(action, state)]) +
                 beta * (wins_rave[(action[0], state)][player] / plays_rave[(action[0], state)]) +
                 sqrt(self.confident * log(total) / plays[(action, state)]), action)
                for action in actions)  # UCT RAVE

        else:
            # a simple strategy
            # prefer to choose the nearer moves without statistics,
            # and then the farthers.
            # try to add statistics info to all moves quickly
            # adjacents = []
            # if len(availables) > self.n_in_row:
            #     adjacents = self.adjacent_moves(board, state, player, plays)

            # if len(adjacents):
            #     action = (choice(adjacents), player)
            # else:
            #     peripherals = []
            #     for action in actions:
            #         if not plays.get((action, state)):
            #             peripherals.append(action)
            #     action = choice(peripherals)
            action = choice(actions)
        return action

    def backpropagation(self,states_list,plays,winner,wins,plays_rave,wins_rave):
        for i, ((m_root, p), s_root) in enumerate(states_list):
            action = (m_root, p)
            # if (action, s_root) in plays:
            if plays.__contains__((action, s_root)):
                plays[(action, s_root)] += 1  # all visited moves
                """based on Local_AI modified here"""
                # if player == winner and player in action:
                if p == winner :
                    wins[(action, s_root)] += 1  # only winner's moves

            for ((m_sub, p), s_sub) in states_list[i:]:
                plays_rave[(m_sub, s_root)] += 1  # all child nodes of s_root
                if winner in wins_rave[(m_sub, s_root)]:
                    wins_rave[(m_sub, s_root)][winner] += 1  # each node is divided by the player

    def select_one_move(self):
        """
        select by win percentage
        """

        percent_wins, move = max(
            (self.wins.get(((move, self.player), self.board.current_state()), 0) /
             self.plays.get(((move, self.player), self.board.current_state()), 1),
             move)
            for move in self.board.availables)

        # display the statistics for each possible play,
        # first is MC value, second is AMAF value
        for x in sorted(
                ((100 * self.wins.get(((move, self.player), self.board.current_state()), 0) /
                  self.plays.get(((move, self.player), self.board.current_state()), 1),
                  100 * self.wins_rave.get((move, self.board.current_state()), {}).get(self.player, 0) /
                  self.plays_rave.get((move, self.board.current_state()), 1),
                  self.wins.get(((move, self.player), self.board.current_state()), 0),
                  self.plays.get(((move, self.player), self.board.current_state()), 1),
                  self.wins_rave.get((move, self.board.current_state()), {}).get(self.player, 0),
                  self.plays_rave.get((move, self.board.current_state()), 1),
                  # self.locate_move(move))
                  [move // self.board.width, move % self.board.width])
                 for move in self.board.availables),
                reverse=True):
            print('{6}: {0:.2f}%--{1:.2f}% ({2} / {3})--({4} / {5})'.format(*x))
        return move

    def get_player(self, players):
        p = players.pop(0)
        players.append(p)
        return p


    def prune(self):
        """
        remove not selected path
        """
        length = len(self.board.states)
        keys = list(self.plays)
        for a, s in keys:
            if len(s) < length + 2:
                del self.plays[(a, s)]
                del self.wins[(a, s)]

        keys = list(self.plays_rave)
        for m, s in keys:
            if len(s) < length + 2:
                del self.plays_rave[(m, s)]
                del self.wins_rave[(m, s)]

    def piecesCount(self,border,states,x,y,player, pieces_count, x1, y1):
        for i in range(1, Const.n_in_row):
            new_x = x + x1*i
            new_y = y + y1*i
            #在边界内部
            if new_x < border and new_y < border and new_x >=0 and new_y >=0:
                if states.__contains__(new_x*border+new_y) and states[new_x*border+new_y] == player:
                    pieces_count +=1
                else:
                    break
            else:
                break
        return pieces_count

    def coorJudge(self,border,x,y,player, states):

        pieces_count = 0
        pieces_count = self.piecesCount(border,states,x,y,player, pieces_count, 1, 0)  # 右边
        pieces_count = self.piecesCount(border,states,x,y,player, pieces_count, -1, 0)  # 左边
        if pieces_count >= Const.n_in_row - 1:
            return True

        pieces_count = 0
        pieces_count = self.piecesCount(border,states,x,y,player, pieces_count, 0, -1)  # 上边
        pieces_count = self.piecesCount(border,states,x,y,player, pieces_count, 0, 1)  # 下边
        if pieces_count >= Const.n_in_row - 1:
            return True

        pieces_count = 0
        pieces_count = self.piecesCount(border,states,x,y,player, pieces_count, 1, 1)  # 右下角
        pieces_count = self.piecesCount(border,states,x,y,player, pieces_count, -1, -1)  # 左上角
        if pieces_count >= Const.n_in_row - 1:
            return True

        pieces_count = 0
        pieces_count = self.piecesCount(border,states,x,y,player, pieces_count, 1, -1)  # 右上角
        pieces_count = self.piecesCount(border,states,x,y,player, pieces_count, -1, 1)  # 左下角
        if pieces_count >= Const.n_in_row - 1:
            return True

        return False

    def has_a_winner(self, board,action):
        moved = list(set(range(board.width * board.height)) - set(board.availables))
        if(len(moved) < self.n_in_row + 2):
            return False, -1
        width = board.width
        states = board.states
        m = action[0]
        x = m // width
        y = m % width
        player = action[1]
        if self.coorJudge(width,x,y,player,states):
            return True,player
        return False, -1

