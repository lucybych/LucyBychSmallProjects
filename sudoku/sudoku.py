import random
from flask import Flask, render_template, jsonify

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_full_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for num in nums:
                if is_valid(board, i, j, num):
                    board[i][j] = num
                    if solve(board):
                        break
                    board[i][j] = 0
    return board

def remove_numbers(board, hints):
    total_cells = 81
    cells_to_remove = total_cells - hints

    while cells_to_remove > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            cells_to_remove -= 1

    return board

def generate_sudoku(hints=20):
    board = generate_full_board()
    puzzle = remove_numbers(board, hints)
    return puzzle

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate")
def generate():
    hints = random.randint(17,41)
    puzzle = generate_sudoku(hints=hints)
    return jsonify({"puzzle": puzzle})

if __name__ == "__main__":
    app.run(debug=True)