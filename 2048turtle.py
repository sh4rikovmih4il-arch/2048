import turtle
import random
from datetime import datetime

CELL = 100
SIZE = 4
OFFSET = -200

coords = {
    "11": (-150, 150), "12": (-50, 150), "13": (50, 150), "14": (150, 150),
    "21": (-150,  50), "22": (-50,  50), "23": (50,  50), "24": (150,  50),
    "31": (-150, -50), "32": (-50, -50), "33": (50, -50), "34": (150, -50),
    "41": (-150,-150), "42": (-50,-150), "43": (50,-150), "44": (150,-150)
}

TILE_COLORS = {
    2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179", 16: "#F59563",
    32: "#F67C5F", 64: "#F84028", 128: "#EDCF72", 256: "#EDCC61",
    512: "#EDC850", 1024: "#EDC53F", 2048: "#EDC22E"
}

t = turtle.Turtle()
screen = turtle.Screen()
screen.title("2048")
screen.bgcolor("#FAF8EF")

t.hideturtle()
t.speed(0)
turtle.tracer(0)

score = 0
board = []

def draw_grid():
    t.color("#6B635A")
    t.pensize(5)
    for i in range(SIZE + 1):
        x = OFFSET + i * CELL
        t.penup()
        t.goto(x, OFFSET)
        t.setheading(90)
        t.pendown()
        t.forward(SIZE * CELL)

    for i in range(SIZE + 1):
        y = OFFSET + i * CELL
        t.penup()
        t.goto(OFFSET, y)
        t.setheading(0)
        t.pendown()
        t.forward(SIZE * CELL)

def draw_tile(row, col, value):
    key = f"{row+1}{col+1}"
    x, y = coords[key]

    color = TILE_COLORS.get(value, "#D0CA98")
    t.fillcolor(color)

    t.penup()
    t.goto(x - CELL/2, y - CELL/2)
    t.pendown()
    t.begin_fill()
    for _ in range(4):
        t.forward(CELL)
        t.left(90)
    t.end_fill()

    text_color = "#6B635A"
    font_size = 24 if value < 100 else 20 if value < 1000 else 16

    t.color(text_color)
    t.penup()
    t.goto(x, y - font_size/2)
    t.write(str(value), align="center", font=("Arial", font_size, "bold"))

def draw_score():
    t.penup()
    t.goto(-190, 220)
    t.color("#776E65")
    t.write(f"Счёт: {score}", align="left", font=("Arial", 24, "bold"))

def draw_board(board):
    t.clear()
    draw_grid()
    for r in range(SIZE):
        for c in range(SIZE):
            val = board[r][c]
            if val != 0:
                draw_tile(r, c, val)
    draw_score()
    turtle.update()

def init_game():
    global board
    board = [[0] * SIZE for _ in range(SIZE)]
    add_tile(board)
    add_tile(board)

def add_tile(board):
    empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def move_left(board):
    moved = False
    points_gained = 0
    for row in board:
        non_zero = [num for num in row if num != 0]
        merged = []
        i = 0
        while i < len(non_zero):
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                new_val = non_zero[i] * 2
                merged.append(new_val)
                points_gained += new_val
                i += 2
            else:
                merged.append(non_zero[i])
                i += 1
        merged += [0] * (SIZE - len(merged))
        if merged != row:
            moved = True
        row[:] = merged
    return moved, points_gained

def rotate_board(board, times=1):
    b = [row[:] for row in board]
    for _ in range(times):
        b = [list(row) for row in zip(*b[::-1])]
    return b

def move(board, direction):
    rotations = {'a': 0, 'd': 2, 'w': 1, 's': 3}
    rotated = rotate_board(board, rotations[direction])
    moved, points = move_left(rotated)
    board[:] = rotate_board(rotated, (4 - rotations[direction]) % 4)
    return moved, points

def is_game_over(board):
    if any(0 in row for row in board):
        return False
    for i in range(SIZE):
        for j in range(SIZE - 1):
            if board[i][j] == board[i][j + 1]:
                return False
    for i in range(SIZE - 1):
        for j in range(SIZE):
            if board[i][j] == board[i + 1][j]:
                return False
    return True

def has_won(board):
    return any(2048 in row for row in board)

def save_game():
    with open('save_2048.txt', 'w', encoding='utf-8') as f:
        f.write(f"{score}\n")
        for row in board:
            f.write(" ".join(str(x) for x in row) + "\n")

def load_game():
    global board, score
    with open('save_2048.txt', 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    score = int(lines[0])
    board = [[int(x) for x in lines[i].split()] for i in range(1, SIZE + 1)]
    draw_board(board)

def handle_move(direction):
    global score
    moved, points = move(board, direction)
    if moved:
        score += points
        add_tile(board)
        process_game_state()

def process_game_state():
    draw_board(board)
    if has_won(board):
        show_win_screen()
    elif is_game_over(board):
        show_game_over_screen()

def show_win_screen():
    screen.clearscreen()
    t.goto(-270, 0)
    t.color("#00FF00")
    t.write(f"Счёт: {score}. ПОБЕДА!", align="left", font=("Arial", 50, "bold"))
    turtle.update()
    save_stats()
    register_keys()

def show_game_over_screen():
    screen.clearscreen()
    t.goto(-250, 0)
    t.color("#776E65")
    t.write("Игра окончена!", align="left", font=("Arial", 50, "bold"))
    turtle.update()
    save_stats()
    register_keys()

def save_stats():
    max_val = max([max(row) for row in board])
    with open('game_stats_2048.txt', 'a', encoding='utf-8') as f:
        f.write(f"Счет: {score}\n")
        f.write(f"Максимальное число: {max_val}\n")
        f.write(f"Время: {datetime.now()}\n")
        f.write(f"Поле: {board}\n\n")

def register_keys():
    screen.onkey(lambda: handle_move('w'), "w")
    screen.onkey(lambda: handle_move('s'), "s")
    screen.onkey(lambda: handle_move('a'), "a")
    screen.onkey(lambda: handle_move('d'), "d")
    screen.onkey(save_game, "k")
    screen.onkey(load_game, "l")

init_game()
draw_board(board)
register_keys()
screen.listen()
turtle.done()