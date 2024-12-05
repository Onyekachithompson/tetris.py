import turtle
import random
import time

# Screen setup
wn = turtle.Screen()
wn.title("Tetris")
wn.bgcolor("black")
wn.setup(width=600, height=800)
wn.tracer(0)

# Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

# Define the shapes of the Tetris blocks (I, O, T, L, J, S, Z)
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]],  # J shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
]

# Game variables
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
current_shape = random.choice(SHAPES)
shape_x, shape_y = GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0

# Draw a cell
def draw_cell(x, y, color):
    turtle.penup()
    turtle.goto(x * CELL_SIZE - 150, 350 - y * CELL_SIZE)
    turtle.pendown()
    turtle.color(color)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(CELL_SIZE)
        turtle.right(90)
    turtle.end_fill()

# Draw the grid and shape
def draw_grid():
    turtle.clear()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] != 0:
                draw_cell(x, y, "blue")
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell != 0:
                draw_cell(shape_x + x, shape_y + y, "red")
    wn.update()

# Collision detection
def check_collision(dx, dy):
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell == 0:
                continue
            nx, ny = shape_x + x + dx, shape_y + y + dy
            if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT or grid[ny][nx] != 0:
                return True
    return False

# Merge shape into grid
def merge_shape():
    global current_shape, shape_x, shape_y
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell != 0:
                grid[shape_y + y][shape_x + x] = 1
    check_lines()
    current_shape = random.choice(SHAPES)
    shape_x, shape_y = GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0

# Check for completed lines
def check_lines():
    global grid
    grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(grid) < GRID_HEIGHT:
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])

# Rotate shape
def rotate_shape():
    global current_shape
    rotated_shape = [list(row) for row in zip(*current_shape[::-1])]
    if not check_collision(0, 0):
        current_shape = rotated_shape

# Move shape
def move_left():
    global shape_x
    if not check_collision(-1, 0):
        shape_x -= 1

def move_right():
    global shape_x
    if not check_collision(1, 0):
        shape_x += 1

def move_down():
    global shape_y
    if check_collision(0, 1):
        merge_shape()
    else:
        shape_y += 1

# Key bindings
wn.listen()
wn.onkey(move_left, "Left")
wn.onkey(move_right, "Right")
wn.onkey(rotate_shape, "Up")
wn.onkey(move_down, "Down")

# Main game loop
while True:
    wn.update()
    time.sleep(0.5)
    move_down()
    draw_grid()