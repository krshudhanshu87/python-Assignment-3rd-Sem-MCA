from tkinter import *
import random

# ==================================
# GAME SETTINGS
# ==================================

GAME_WIDTH = 700
GAME_HEIGHT = 700

START_SPEED = 180      # snake starts slowly
MIN_SPEED = 50         # maximum speed limit
SPEED_INCREMENT = 5    # speed increase per score

SPACE_SIZE = 25
BODY_PARTS = 3

SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

score = 0
direction = "right"
game_speed = START_SPEED


# ==================================
# SNAKE CLASS
# ==================================

class Snake:

    def __init__(self):

        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:

            square = canvas.create_rectangle(
                x,
                y,
                x + SPACE_SIZE,
                y + SPACE_SIZE,
                fill=SNAKE_COLOR,
                tag="snake"
            )

            self.squares.append(square)


# ==================================
# FOOD CLASS
# ==================================

class Food:

    def __init__(self):

        while True:

            x = random.randint(
                0,
                (GAME_WIDTH // SPACE_SIZE) - 1
            ) * SPACE_SIZE

            y = random.randint(
                0,
                (GAME_HEIGHT // SPACE_SIZE) - 1
            ) * SPACE_SIZE

            if [x, y] not in snake.coordinates:
                break

        self.coordinates = [x, y]

        canvas.create_oval(
            x,
            y,
            x + SPACE_SIZE,
            y + SPACE_SIZE,
            fill=FOOD_COLOR,
            tag="food"
        )


# ==================================
# GAME LOOP
# ==================================

def next_turn(snake, food):

    global score
    global game_speed

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE

    elif direction == "down":
        y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])

    square = canvas.create_rectangle(
        x,
        y,
        x + SPACE_SIZE,
        y + SPACE_SIZE,
        fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)

    # Snake eats food
    if x == food.coordinates[0] and y == food.coordinates[1]:

        score += 1

        # Increase speed gradually
        if game_speed > MIN_SPEED:
            game_speed -= SPEED_INCREMENT

        label.config(
            text=f"Score : {score} | Speed : {START_SPEED - game_speed}"
        )

        canvas.delete("food")
        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(game_speed, next_turn, snake, food)


# ==================================
# CHANGE DIRECTION
# ==================================

def change_direction(new_direction):

    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction

    elif new_direction == "right" and direction != "left":
        direction = new_direction

    elif new_direction == "up" and direction != "down":
        direction = new_direction

    elif new_direction == "down" and direction != "up":
        direction = new_direction


# ==================================
# COLLISION CHECK
# ==================================

def check_collisions(snake):

    x, y = snake.coordinates[0]

    # Wall collision

    if x < 0 or x >= GAME_WIDTH:
        return True

    if y < 0 or y >= GAME_HEIGHT:
        return True

    # Self collision

    for body_part in snake.coordinates[1:]:

        if x == body_part[0] and y == body_part[1]:
            return True

    return False


# ==================================
# GAME OVER SCREEN
# ==================================

def game_over():

    canvas.delete(ALL)

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 - 40,
        text="GAME OVER",
        fill="red",
        font=("Consolas", 40, "bold")
    )

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 + 20,
        text=f"Final Score : {score}",
        fill="white",
        font=("Consolas", 25)
    )


# ==================================
# MAIN WINDOW
# ==================================

window = Tk()

window.title("Snake Game")
window.resizable(False, False)

label = Label(
    window,
    text="Score : 0 | Speed : 0",
    font=("Consolas", 20)
)
label.pack()

canvas = Canvas(
    window,
    bg=BACKGROUND_COLOR,
    width=GAME_WIDTH,
    height=GAME_HEIGHT
)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

center_x = int((screen_width / 2) - (window_width / 2))
center_y = int((screen_height / 2) - (window_height / 2))

window.geometry(
    f"{window_width}x{window_height}+{center_x}+{center_y}"
)

window.bind("<Left>",
            lambda event: change_direction("left"))

window.bind("<Right>",
            lambda event: change_direction("right"))

window.bind("<Up>",
            lambda event: change_direction("up"))

window.bind("<Down>",
            lambda event: change_direction("down"))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()