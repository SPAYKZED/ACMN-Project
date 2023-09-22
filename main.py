import tkinter as tk
import random

# Parameters that can be changed
WINDOW_SIZE = 775
SQUARE_SIDE = 700
NUM_POINTS = 50
CIRCLE_RADIUS = 5


def draw_random_points(canvas, square_side=SQUARE_SIDE, num_points=NUM_POINTS, circle_radius=CIRCLE_RADIUS):
    for _ in range(num_points):
        x = random.randint(10 + circle_radius, 10 + square_side - circle_radius)
        y = random.randint(10 + circle_radius, 10 + square_side - circle_radius)

        canvas.create_oval(x, y, x + 2, y + 2, fill='black')            # Drawing a point
        # Drawing a circle around a point
        canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, outline='black')


# Create the main window
root = tk.Tk()
root.title("Random points in a square")

# Setting the window dimensions
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")

# Create a drawing area
canvas = tk.Canvas(root, bg='white')
canvas.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Drawing a square
canvas.create_rectangle(10, 10, 10 + SQUARE_SIDE, 10 + SQUARE_SIDE)

# Draw random points in a square with circles around them
draw_random_points(canvas)

# Start the main application loop
root.mainloop()