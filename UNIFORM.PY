import tkinter as tk
from tkinter import messagebox
import heapq

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self.initialize_grid()

    def initialize_grid(self):
        grid = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

        for i in range(self.rows):
            grid[i][0] = 0
            grid[i][self.cols - 1] = 0
        for j in range(self.cols):
            grid[0][j] = 0
            grid[self.rows - 1][j] = 0

        manual_walls = [
            (1, 3), (2, 3), (3, 3), (4, 3),
            (5, 2), (5, 3), (5, 4),
            (7, 6), (6, 6), (5, 6), (4, 6),
            (3, 8), (4, 8), (5, 8),
            (2, 5), (6, 2), (8, 4)
        ]

        for (i, j) in manual_walls:
            grid[i][j] = 0

        grid[1][1] = 1  
        grid[self.rows - 2][self.cols - 2] = 1  

        return grid


class NextState:
    def __init__(self, position, direction, board):
        self.position = position
        self.direction = direction
        self.board = board

    def check_valid(self, position):
        row, col = position
        return 0 <= row < self.board.rows and 0 <= col < self.board.cols and self.board.grid[row][col] != 0

    def move(self):
        row, col = self.position
        if self.direction == "up":
            return self.move_up(row, col)
        elif self.direction == "down":
            return self.move_down(row, col)
        elif self.direction == "left":
            return self.move_left(row, col)
        elif self.direction == "right":
            return self.move_right(row, col)
        return None

    def move_up(self, row, col):
        while row > 0 and self.check_valid((row - 1, col)):
            row -= 1
        return (row, col)

    def move_down(self, row, col):
        while row < self.board.rows - 1 and self.check_valid((row + 1, col)):
            row += 1
        return (row, col)

    def move_left(self, row, col):
        while col > 0 and self.check_valid((row, col - 1)):
            col -= 1
        return (row, col)

    def move_right(self, row, col):
        while col < self.board.cols - 1 and self.check_valid((row, col + 1)):
            col += 1
        return (row, col)


class State:
    def __init__(self, board: Board, start: tuple, goal: tuple):
        self.board = board
        self.start = start
        self.goal = goal
        self.position = start
        self.history = []  
        self.cost = 0  

    def check_goal(self):
        return self.position == self.goal

    def get_next_states(self):
        directions = ["up", "down", "left", "right"]
        next_states = []

        for direction in directions:
            next_state_position = NextState(self.position, direction, self.board).move()
            if next_state_position:
                next_states.append((next_state_position, direction))
        return next_states

    def move(self, next_state_position, direction_cost):
        self.position = next_state_position
        self.history.append(self.position)
        self.cost += direction_cost  

    def get_cost(self):
        return self.cost


class UniformCostSearch:
    def __init__(self, start: tuple, goal: tuple, board: Board):
        self.start = start
        self.goal = goal
        self.board = board
        self.frontier = []
        self.explored = set()

    def search(self):
        initial_state = State(self.board, self.start, self.goal)
        heapq.heappush(self.frontier, (initial_state.get_cost(), initial_state))

        while self.frontier:
            current_cost, current_state = heapq.heappop(self.frontier)

            if current_state.check_goal():
                return current_state.history

            if current_state.position in self.explored:
                continue

            self.explored.add(current_state.position)

            next_states = current_state.get_next_states()
            for next_state_position, direction in next_states:
                direction_cost = 1  
                new_state = State(self.board, current_state.start, self.goal)
                new_state.move(next_state_position, direction_cost)
                heapq.heappush(self.frontier, (new_state.get_cost(), new_state))

        return []  


if __name__ == "__main__":
    board = Board(10, 10)
    start = (1, 1)
    goal = (8, 8)
    
    ucs = UniformCostSearch(start, goal, board)
    solution_path = ucs.search()
    
    if solution_path:
        print("Found path:", solution_path)
    else:
        print("No path found")
