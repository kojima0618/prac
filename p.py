import random
import time
import heapq
import copy
from collections import deque

class Puzzle:
    actions = [[0,1],[0,-1],[1,0],[-1,0]]

    def __init__(self, edgelength):
        self.edgelength = edgelength
        self.board = [[j + i * edgelength for j in range(1, edgelength+1)] for i in range(edgelength)]
        self.board[edgelength-1][edgelength-1] = 0
        self.space = [edgelength-1, edgelength-1]
        
    def space_search(self):
        for i in range(self.edgelength):
            for j in range(self.edgelength):
                if self.board[i][j] == 0:
                    self.space = [i, j]
                    return

    def step(self, action):
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
        for row in self.board:
            print(' '.join(map(str, row)))
        print()

    def able_actions(self):
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
        permutation_count = 0
        self.space_search()
        check_board = sum(self.board, [])
        check_board = [i if i != 0 else 9 for i in check_board]
        for i in range(len(check_board)):
            for j in range(i+1, len(check_board)):
                if(check_board[i] > check_board[j]):
                    permutation_count += 1
        
        if((permutation_count +  (self.edgelength*2-self.space[0]-self.space[1] + 2)) % 2 == 0):
            return True
        else:
            return False

class Node:
    def __init__(self, puzzle, pre_node, deep):
        self.puzzle :Puzzle = puzzle
        self.pre_node = pre_node
        self.deep = deep
        self.searched = False
        if heuristic_case >= 0:
            self.cost = self.heuristic(heuristic_case) + self.deep
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def heuristic(self, num):
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
            '''for i in range(self.puzzle.edgelength):
                for j in range(self.puzzle.edgelength):
                    temp = self.puzzle.board[i][j]
                    if(temp == 0):
                        temp = self.puzzle.edgelength ** 2
                    k, l = divmod(temp, self.puzzle.edgelength)
                    if(l==0):
                        k -= 1
                        l += self.puzzle.edgelength
                distance = distance + abs(k-i) + abs((l - 1) - j)'''
            return distance

class IDS:
    def __init__(self, first_board, goal_board):
        self.limit = 0
        self.first_node = Node(first_board, None, 0)
        self.goal_board = goal_board.board
        self.openlist = deque([self.first_node])
    
    def ids(self):
        while True:
            if not self.dls():
                self.limit += 1
                print(self.limit)
                self.first_node.searched = False
                self.openlist = deque([self.first_node])
            else:
                return True

    def dls(self):
        while self.openlist:
            node = self.openlist.popleft()
            
            if node.deep >= self.limit:
                continue
            
            if not node.searched:
                node.searched = True
                for action in node.puzzle.able_actions():
                    next_node = Node(node.puzzle.step(action), node, node.deep + 1)
                    if next_node.puzzle.board == self.goal_board:
                        self.route_show(next_node)
                        return True
                    if not node.pre_node or next_node.puzzle.board != node.pre_node.puzzle.board:
                        self.openlist.appendleft(next_node)
        return False

    def route_show(self, goal_node):
        goal_route = deque()
        while goal_node:
            goal_route.appendleft(goal_node)
            goal_node = goal_node.pre_node
        
        for node in goal_route:
            node.puzzle.show()
            print('↓')
        print("Goal reached")

class BFS:
    def __init__(self, first_board, goal_board):
        self.first_node = Node(first_board, None, 0)
        self.goal_board = goal_board.board
        self.openqueue = []
        heapq.heappush(self.openqueue, self.first_node)
        
    def bfs(self):
        while self.openqueue:
            node = heapq.heappop(self.openqueue)
            for action in node.puzzle.able_actions():
                next_node = Node(node.puzzle.step(action), node, node.deep + 1)
                if next_node.puzzle.board == self.goal_board:
                    self.route_show(next_node)
                    return True
                if not node.pre_node or next_node.puzzle.board != node.pre_node.puzzle.board:
                    heapq.heappush(self.openqueue, next_node)

    def route_show(self, goal_node):
        goal_route = deque()
        while goal_node:
            goal_route.appendleft(goal_node)
            goal_node = goal_node.pre_node
        
        goal_route.pop()
        for node in goal_route:
            node.puzzle.show()
            print('↓')
        
        goal_board.show()
        print("Goal reached")
        print('hands = ', len(goal_route))

# Initialize the boards
edge_length = 4
first_board = Puzzle(edge_length)
able_solve = False

while able_solve == False:
    flat_board = sum(first_board.board, [])
    random.shuffle(flat_board)
    first_board.board = [flat_board[i:i + edge_length] for i in range(0, edge_length**2, edge_length)]
    able_solve = first_board.able_solve()
first_board.space_search()

first_board.show()

goal_board = Puzzle(edge_length)

heuristic_case = 2
goal_place = []
if(heuristic_case == 2):
    goal_board1 = sum(goal_board.board, [])
    for i in range(edge_length):
        for j in range(edge_length):
            goal_place.append([i,j])
    goal_dict = dict(zip(goal_board1, goal_place))
# Run IDS
ids_puzzle = IDS(first_board, goal_board)
bfs_puzzle = BFS(first_board, goal_board)
t1 = time.time()
if first_board.board != goal_board.board:
    #ids_puzzle.ids()
    bfs_puzzle.bfs()
t2 = time.time()

print(f"Time taken: {t2 - t1} seconds")