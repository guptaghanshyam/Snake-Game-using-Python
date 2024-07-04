import math
import turtle
import random

# Constants
WIDTH = 800
HEIGHT = 600
DELAY = 200
FOOD_SIZE = 40
SNACK_SIZE = 20

offsets = {
    "up": (0, SNACK_SIZE),
    "down": (0, -SNACK_SIZE),
    "left": (-SNACK_SIZE, 0),
    "right": (SNACK_SIZE, 0),
}

# High score
high_score = 0

# Load the high score if it exists
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass

# Function to update the high score
def update_high_score():
    global high_score
    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))

# Bind the direction keys to their respective functions
def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("left"), "Left")
    screen.onkey(lambda: set_snake_direction("right"), "Right")

# Set the snake direction, ensuring no self-collision
def set_snake_direction(direction):
    global snake_direction
    if direction == "up" and snake_direction != "down":
        snake_direction = "up"
    elif direction == "down" and snake_direction != "up":
        snake_direction = "down"
    elif direction == "left" and snake_direction != "right":
        snake_direction = "left"
    elif direction == "right" and snake_direction != "left":
        snake_direction = "right"

# Main game loop
def game_loop():
    stamper.clearstamps()

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check for collisions
    if new_head in snake or new_head[0] < -WIDTH / 2 or new_head[0] > WIDTH / 2 or new_head[1] < -HEIGHT / 2 or new_head[1] > HEIGHT / 2:
        reset()
    else:
        snake.append(new_head)

        if not food_collision():
            snake.pop(0)

        stamper.shape("assets/snake-head-20x20.gif")
        stamper.goto(snake[-1][0], snake[-1][1])
        stamper.stamp()
        stamper.shape("circle")

        for segment in snake[:-1]:
            stamper.goto(segment[0], segment[1])
            stamper.stamp()

        screen.title(f"Snake Game - Score: {score} - High Score: {high_score}")
        screen.update()

        turtle.ontimer(game_loop, DELAY)

# Check for food collision
def food_collision():
    global food_pos, score
    if get_distance(snake[-1], food_pos) < 20:
        score += 1
        update_high_score()
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        return True
    return False

# Get a random position for the food
def get_random_food_pos():
    x = random.randint(-WIDTH / 2 + FOOD_SIZE, WIDTH / 2 - FOOD_SIZE)
    y = random.randint(-HEIGHT / 2 + FOOD_SIZE, HEIGHT / 2 - FOOD_SIZE)
    return (x, y)

# Calculate the distance between two positions
def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Reset the game
def reset():
    global score, snake, snake_direction, food_pos
    score = 0
    snake = [[0, 0], [SNACK_SIZE, 0], [SNACK_SIZE * 2, 0], [SNACK_SIZE * 3, 0]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    game_loop()

# Create a window for drawing
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake Game")
screen.bgpic("assets/bg2.gif")
screen.register_shape("assets/snake-food-32x32.gif")
screen.register_shape("assets/snake-head-20x20.gif")
screen.tracer(0)

# Event handler
screen.listen()
bind_direction_keys()

# Create a turtle for binding
stamper = turtle.Turtle()
stamper.shape("circle")
stamper.color("blue")
stamper.penup()

# Create the food turtle
food = turtle.Turtle()
food.shape("assets/snake-food-32x32.gif")
food.shapesize(FOOD_SIZE / 20)
food.penup()

# Start the game
reset()

turtle.done()
