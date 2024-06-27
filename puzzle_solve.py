import random
import memory_profiler as MP
import time
import heapq
from collections import deque
import gc

#@profile


class Puzzle:

    ''' edgelength : ボードの辺の長さ
        board : ボードを二次元配列として扱う。スペースは0で表す。
        space : 0の位置
    '''
    

    def __init__(self, edgelength):

        ''' 指定された辺の長さのボードを作成。
            edgelength = 3 の場合は、
            1 2 3
            4 5 6
            7 8 0
        '''

        self.edgelength = edgelength
        self.board = [[j + i * edgelength for j in range(1, edgelength+1)] for i in range(edgelength)]
        self.board[edgelength-1][edgelength-1] = 0
        self.space = [edgelength-1, edgelength-1]
    
    #0の位置を返す
    def space_search(self):
        for i in range(self.edgelength):
            for j in range(self.edgelength):
                if self.board[i][j] == 0:
                    self.space = [i, j]
                    return

    def step(self, action):

        ''' 動かす方向を引数で指定。
            その方向に動かした後のボードをクラス変数にもつ
            新しいPuzzle型の変数を作成'''
        
        next_board = [row[:] for row in self.board]
        i, j = self.space
        di, dj = action
        ni, nj = i + di, j + dj
        next_board[i][j] = self.board[ni][nj]
        next_board[ni][nj] = 0
        next_puzzle = Puzzle(self.edgelength)
        next_puzzle.board = next_board
        next_puzzle.space = [ni, nj]
        return next_puzzle
        
    def show(self):
        '''ボードの出力'''
        for row in self.board:
            print(' '.join(map(str, row)))
        print()

    def able_actions(self):
        ''' 0の位置から、動かすことができる方向をable_actionに格納する。'''
        self.space_search()
        able_actions = []
        i, j = self.space
        if j > 0:
            able_actions.append([0, -1])
        if j < self.edgelength - 1:
            able_actions.append([0, 1])
        if i > 0:
            able_actions.append([-1, 0])
        if i < self.edgelength - 1:
            able_actions.append([1, 0])
        return able_actions
    
    def able_solve(self):

        ''' パズルの初期位置がゴールにたどり着くかを確かめる。
            ただし、ゴールのボードの形は
            1 2 3
            4 5 6
            7 8 0
            とする。(edgelength = 3の場合)'''
        
        permutation_count = 0
        self.space_search()
        check_board = sum(self.board, [])
        check_board = [i if i != 0 else edge_length**2 for i in check_board]
        for i in range(len(check_board)):
            for j in range(i+1, len(check_board)):
                if(check_board[i] > check_board[j]):
                    permutation_count += 1
        
        '''ゴールまでの互換の回数と、スペースのマンハッタン距離の和が偶数であることが条件'''
        if((permutation_count +  (self.edgelength*2-self.space[0]-self.space[1] + 2)) % 2 == 0):
            return True
        else:
            return False

class Node:

    ''' puzzle : Puzzle型の変数
        pre_node : 前ノード(ルートを記録するため)
        deep : 探索の深さ
        searched : 探索したかを記録する。
        heauristic_case : heauristic関数を指定するグローバル変数
        cost : それまでの探索コストとheauristic関数の値の和
                A*探索では、この値が小さいほうから探索を行う。'''
        
    def __init__(self, puzzle, pre_node, deep):
        self.puzzle :Puzzle = puzzle
        self.pre_node = pre_node
        self.deep = deep
        self.searched = False
        if heuristic_case >= 0:
            self.cost = self.heuristic(heuristic_case) + self.deep
    
    def __lt__(self, other):
        '''探索の優先度をつける際にcostを比較する。'''
        return self.cost < other.cost
    
    def heuristic(self, num):

        ''' num = 0の場合、単なる幅優先探索
            num = 1の場合、ゴールと場所が違う個数を返す。
            num = 2の場合、ゴールとのマンハッタン距離の合計を返す。'''
        
        if num == 0:
            return 0
        
        elif num == 1:
            count = sum(self.puzzle.board[i][j] != self.puzzle.edgelength*i + j + 1 for i in range(self.puzzle.edgelength)
            for j in range(self.puzzle.edgelength))
            if self.puzzle.board[self.puzzle.edgelength-1][self.puzzle.edgelength-1] == 0:
                count -= 1
            return count
        
        elif num == 2:
            distance = 0
            for i in range(self.puzzle.edgelength):
                for j in range(self.puzzle.edgelength):
                    value = self.puzzle.board[i][j]
                    if value != 0:
                        goal_i, goal_j = goal_dict[value]
                        distance += abs(i - goal_i) + abs(j - goal_j)
            return distance

class IDS:
    '''ノードの総数を格納する変数'''
    node_num = 0

    ''' limit : 深さの制限
        first_node : 最初のノード
        goal_board : ゴールのボードの形
        openlist : 探索するノードを格納するスタック
    '''

    def __init__(self, first_board, goal_board):
        self.limit = 0
        self.first_node = Node(first_board, None, 0)
        self.goal_board = goal_board.board
        self.openlist = deque([self.first_node])
    
    def ids(self):
        while True:
            '''opnelistが空だったら制限を1増やして、再度深さ優先探索'''
            if not self.dls():
                self.limit += 1
                self.first_node.searched = False
                self.openlist = deque([self.first_node])
            else:
                '''openlistに要素がある場合、そのまま探索'''
                return True


    def dls(self):
        '''openlistが空でない場合、実行する'''
        while self.openlist:
            node = self.openlist.popleft()
            '''探索するノードをpopして、探索数に+1する'''
            self.node_num += 1
            
            '''制限を超える深さは探索しない'''
            if node.deep >= self.limit:
                continue
            
            if not node.searched:
                node.searched = True
                '''次の状態をopenlistに加える'''
                for action in node.puzzle.able_actions():
                    next_node = Node(node.puzzle.step(action), node, node.deep + 1)
                    '''ゴールと一致するか'''
                    if next_node.puzzle.board == self.goal_board:
                        self.route_show(next_node)
                        return True
                    ''' 前回のノードと次のノードが一致しなかったら格納することで、
                        無駄な探索を避ける.
                    '''
                    if not node.pre_node or next_node.puzzle.board != node.pre_node.puzzle.board:
                        self.openlist.appendleft(next_node)
        return False

    def route_show(self, goal_node):
        goal_route = deque()
        while goal_node:
            goal_route.appendleft(goal_node)
            goal_node = goal_node.pre_node
        
        goal_route.pop()
        '''ゴールまでの順序を出力'''
        for node in goal_route:
            node.puzzle.show()
            print('↓')

        goal_board.show()
        print("Goal reached")

        print('hands : ', len(goal_route))
        '''ファイルへの書き込み'''
        with open('h2_hands.txt', mode='a') as f:
            f.write('%d ' % len(goal_route))

        with open('h2_node.txt', mode='a') as f:
            f.write('%d ' % self.node_num)

class BFS:

    ''' openqueue : 優先度付きキュー'''

    def __init__(self, first_board, goal_board):
        self.first_node = Node(first_board, None, 0)
        self.goal_board = goal_board.board
        self.openqueue = []
        heapq.heappush(self.openqueue, self.first_node)
        
    def bfs(self):
        node_num = 0
        while self.openqueue:
            node = heapq.heappop(self.openqueue)
            node_num += 1
            '''次の状態を優先度付きキューにcostが小さい順に入れる。'''
            for action in node.puzzle.able_actions():
                next_node = Node(node.puzzle.step(action), node, node.deep + 1)
                '''ゴールと一致するか'''
                if next_node.puzzle.board == self.goal_board:
                    self.route_show(next_node, node_num)
                    return True
                '''前回のノードと次のノードが一致するか'''
                if not node.pre_node or next_node.puzzle.board != node.pre_node.puzzle.board:
                    heapq.heappush(self.openqueue, next_node)

    def route_show(self, goal_node, node_num):
        goal_route = deque()
        while goal_node:
            goal_route.appendleft(goal_node)
            goal_node = goal_node.pre_node
        
        goal_route.pop()

        '''ゴールまでの順序を出力'''
        for node in goal_route:
            node.puzzle.show()
            print('↓')
        
        goal_board.show()
        print("Goal reached")
        print('hands = ', len(goal_route))
        print('searched node = ', node_num)

        '''ファイルへの書き込み'''
        with open('h2_hands.txt', mode='a') as f:
            f.write('%d ' % len(goal_route))

        with open('h2_node.txt', mode='a') as f:
            f.write('%d ' % node_num)

if __name__ == '__main__':

    '''探索する回数を設定'''
    for i in range(1):

        edge_length = 4
        first_board = Puzzle(edge_length)
        able_solve = False

        '''ゴールできるかをチェックして、できなければシャッフルする'''
        while able_solve == False:
            flat_board = sum(first_board.board, [])
            random.shuffle(flat_board)
            first_board.board = [flat_board[i:i + edge_length] for i in range(0, edge_length**2, edge_length)]
            able_solve = first_board.able_solve()
        first_board.space_search()

        goal_board = Puzzle(edge_length)

        '''どのヒューリスティック関数を使うか。IDSの場合は-1に設定'''
        heuristic_case = 1
        goal_place = []

        '''マンハッタン距離で利用する辞書型配列を作成しておく'''
        if(heuristic_case == 2):
            goal_board1 = sum(goal_board.board, [])
            for i in range(edge_length):
                for j in range(edge_length):
                    goal_place.append([i,j])
            goal_dict = dict(zip(goal_board1, goal_place))

        ids_puzzle = IDS(first_board, goal_board)
        bfs_puzzle = BFS(first_board, goal_board)

        '''bはメモリ、tは時間を計測するための変数'''
        b1 = MP.memory_usage()[0]
        t1 = time.time()
        if first_board.board != goal_board.board:

            '''IDSかA*どちらか'''
            if bfs_puzzle.bfs() == True:
            #if ids_puzzle.ids() == True:
            
                t2 = time.time()
                b2 = MP.memory_usage()[0]

                with open('h2_time.txt', mode='a') as f:
                    f.write('%f ' % (t2-t1))

                with open('h2_memory_mp.txt', mode='a') as f:
                    f.write('%f ' % (b2-b1))

        print(f"Time taken : {t2 - t1} seconds")
        print(f"used memory : {b2-b1} MByte" )
        t1 ,t2 = 0,0
        b2, b1 = 0,0

        '''メモリの解放'''
        gc.collect()

