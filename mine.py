import tkinter as tk
from tkinter import messagebox

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
        
        return grid

class State:
    def __init__(self, board: Board, start1: tuple, goal1: tuple, start2: tuple, goal2: tuple):
        self.board = board
        self.start1 = start1
        self.goal1 = goal1
        self.start2 = start2
        self.goal2 = goal2
        self.position1 = start1
        self.position2 = start2
        self.game_over = False  

    def check(self, direction, position):
        
        row, col = position
        if direction == "up":
            return self.is_valid_position((row - 1, col))
        elif direction == "down":
            return self.is_valid_position((row + 1, col))
        elif direction == "left":
            return self.is_valid_position((row, col - 1))
        elif direction == "right":
            return self.is_valid_position((row, col + 1))
        return False

    def is_valid_position(self, position):
        row, col = position
        if 0 <= row < self.board.rows and 0 <= col < self.board.cols:
            return self.board.grid[row][col] != 0
        return False

    def move(self, direction, player):
        if self.game_over:
            return

        if player == 1:
            row, col = self.position1
        else:
            row, col = self.position2
        
        
        while True:
            if direction == "up":
                new_position = (row - 1, col)
            elif direction == "down":
                new_position = (row + 1, col)
            elif direction == "left":
                new_position = (row, col - 1)
            elif direction == "right":
                new_position = (row, col + 1)

            if self.is_valid_position(new_position):
                row, col = new_position
            else:
                break
        
        
        if player == 1:
            self.position1 = (row, col)
            self.board.grid[row][col] = 2  
        else:
            self.position2 = (row, col)
            self.board.grid[row][col] = 3 

        
        if player == 1 and self.position1 == self.goal1:
            self.game_over = self.position2 == self.goal2  
        elif player == 2 and self.position2 == self.goal2:
            self.game_over = self.position1 == self.goal1  

        return self

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

        self.draw_board()
        self.root.bind("<Key>", self.handle_keypress)

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.state.board.rows):
            for j in range(self.state.board.cols):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                if (i, j) == self.state.position1:
                    color = "red" 
                elif (i, j) == self.state.position2:
                    color = "blue"  
                elif (i, j) == self.state.start1:
                    color = "#ff7f7f"  
                elif (i, j) == self.state.start2:
                    color = "#7fbfff"  
                elif (i, j) == self.state.goal1:
                    color = "#ff4c4c"  
                elif (i, j) == self.state.goal2:
                    color = "#4cafff"  
                elif self.state.board.grid[i][j] == 0:
                    color = "black"  
                elif self.state.board.grid[i][j] == 2:
                    color = "yellow"  
                elif self.state.board.grid[i][j] == 3:
                    color = "cyan"  
                else:
                    color = "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def handle_keypress(self, event):
        if self.state.game_over:
            return  

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
            if not self.state.game_over:
                
                if self.state.position1 != self.state.goal1:
                    self.state.move(direction, 1)  
                if self.state.position2 != self.state.goal2:
                    self.state.move(direction, 2)  
                self.draw_board()

    def reset_game(self):
        board = Board(10, 10)
        start1 = (1, 1)
        goal1 = (8, 1)  
        start2 = (1, 8)
        goal2 = (8, 8)
        self.state = State(board, start1, goal1, start2, goal2)
        self.reset_button.config(state="disabled")
        self.draw_board()

if __name__ == "__main__":
    board = Board(10, 10)
    start1 = (1, 1)

    goal1 = (8, 1)  
    start2 = (1, 8)
    goal2 = (8, 8)
    state = State(board, start1, goal1, start2, goal2)
    
    root = tk.Tk()
    root.title("Zero Squares Game")
    game_gui = GameGUI(root, state)
    root.mainloop()
