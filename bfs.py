import tkinter as tk
from tkinter import messagebox
from collections import deque


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


class State:
    def __init__(self, board: Board, start: tuple, goal: tuple):
        self.board = board
        self.start = start
        self.goal = goal
        self.position = start
        self.path = []

    def check_goal(self):
        return self.position == self.goal

    def is_valid(self, position):
        row, col = position
        return (0 <= row < self.board.rows and
                0 <= col < self.board.cols and
                self.board.grid[row][col] == 1)

    def move_to_max(self, direction):
        row, col = self.position

        if direction == "up":
            while row > 0 and self.is_valid((row - 1, col)):
                row -= 1
        elif direction == "down":
            while row < self.board.rows - 1 and self.is_valid((row + 1, col)):
                row += 1
        elif direction == "left":
            while col > 0 and self.is_valid((row, col - 1)):
                col -= 1
        elif direction == "right":
            while col < self.board.cols - 1 and self.is_valid((row, col + 1)):
                col += 1

        self.position = (row, col)

    def bfs_path(self):
        start = self.start
        goal = self.goal
        queue = deque([(start, [start])])  
        visited = set()

        while queue:
            current_position, path = queue.popleft()

            if current_position in visited:
                continue

            visited.add(current_position)

            if current_position == goal:
                return path  

            row, col = current_position
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  

            for dr, dc in directions:
                next_position = (row + dr, col + dc)

                if self.is_valid(next_position) and next_position not in visited:
                    queue.append((next_position, path + [next_position]))

        return []  


class GameGUI:
    def __init__(self, root, state):
        self.root = root
        self.state = state
        self.cell_size = 40
        self.canvas = tk.Canvas(root, width=self.state.board.cols * self.cell_size,
                                height=self.state.board.rows * self.cell_size)
        self.canvas.pack()

        self.reset_button = tk.Button(root, text="إعادة اللعب", command=self.reset_game)
        self.reset_button.pack()

        self.bfs_button = tk.Button(root, text="عرض الطريق باستخدام BFS", command=self.show_bfs_path)
        self.bfs_button.pack()

        self.draw_board()
        self.root.bind("<Key>", self.handle_keypress)

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.state.board.rows):
            for j in range(self.state.board.cols):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                if (i, j) == self.state.start:
                    color = "green"
                elif (i, j) == self.state.goal:
                    color = "red"
                elif (i, j) == self.state.position:
                    color = "blue"
                elif (i, j) in self.state.path:
                    color = "yellow"
                elif self.state.board.grid[i][j] == 0:
                    color = "black"
                else:
                    color = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def handle_keypress(self, event):
        direction = None
        if event.keysym == "Up":
            direction = "up"
        elif event.keysym == "Down":
            direction = "down"
        elif event.keysym == "Left":
            direction = "left"
        elif event.keysym == "Right":
            direction = "right"

        if direction:
            self.state.move_to_max(direction)
            self.draw_board()

            if self.state.check_goal():
                messagebox.showinfo("نجاح", "لقد وصلت إلى الهدف!")
                self.reset_button.config(state="normal")

    def show_bfs_path(self):
        path = self.state.bfs_path()
        if path:
            self.state.path = path
            self.draw_board()
            messagebox.showinfo("BFS", f"الطريق إلى الهدف: {path}")
        else:
            messagebox.showinfo("BFS", "لا يوجد طريق إلى الهدف!")

    def reset_game(self):
        board = Board(10, 10)
        start = (1, 1)
        goal = (8, 8)
        self.state = State(board, start, goal)
        self.draw_board()


if __name__ == "__main__":
    board = Board(10, 10)
    start = (1, 1)
    goal = (8, 8)
    state = State(board, start, goal)

    root = tk.Tk()
    root.title("Sliding Movement Game with BFS")
    game_gui = GameGUI(root, state)
    root.mainloop()
