import tkinter as tk
import random

# Initial parameters
WINDOW_SIZE = 1050
RECT_WIDTH = 775
RECT_HEIGHT = 775
NUM_POINTS = 50
CIRCLE_RADIUS = 30


root = tk.Tk()
root.title("Random Points in Rectangle")
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")

canvas = tk.Canvas(root, bg='white', width=795, height=800)
canvas.grid(row=0, column=0, rowspan=22)

IS_SQUARE = tk.BooleanVar(value=False)
def draw_random_points():
    canvas.delete("all")

    rect_width = min(int(rect_width_var.get()), 800)
    if IS_SQUARE.get():
        rect_height = rect_width
    else:
        rect_height = min(int(rect_height_var.get()), 800)
    num_points = int(num_points_var.get())
    circle_radius = int(circle_radius_var.get())

    for _ in range(num_points):
        x = random.randint(10 + circle_radius, 10 + rect_width - circle_radius)
        y = random.randint(10 + circle_radius, 10 + rect_height - circle_radius)
        canvas.create_oval(x, y, x + 2, y + 2, fill='black')
        canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, outline='black',
                           width=2)

    canvas.create_rectangle(10, 10, 10 + rect_width, 10 + rect_height, width=2)


# Variables to store the entered values
rect_width_var = tk.StringVar(value=RECT_WIDTH)
rect_height_var = tk.StringVar(value=RECT_HEIGHT)
num_points_var = tk.StringVar(value=NUM_POINTS)
circle_radius_var = tk.StringVar(value=CIRCLE_RADIUS)

# Creating widgets for data input
tk.Label(root, text="RECT WIDTH:").grid(row=0, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=rect_width_var).grid(row=0, column=2, padx=5, pady=5)

# Checkbox to choose between rectangle and square
tk.Checkbutton(root, text="Make it a square", variable=IS_SQUARE).grid(row=1, column=2, padx=5, pady=5, sticky="w")

tk.Label(root, text="RECT HEIGHT:").grid(row=2, column=1, sticky="e", padx=5, pady=5)
rect_height_entry = tk.Entry(root, textvariable=rect_height_var)
rect_height_entry.grid(row=2, column=2, padx=5, pady=5)

tk.Label(root, text="NUM POINTS:").grid(row=3, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=num_points_var).grid(row=3, column=2, padx=5, pady=5)

tk.Label(root, text="CIRCLE RADIUS:").grid(row=4, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=circle_radius_var).grid(row=4, column=2, padx=5, pady=5)


# Function to enable/disable the height input field based on the checkbox status
def toggle_square_mode(*args):
    if IS_SQUARE.get():
        rect_height_entry.config(state=tk.DISABLED)
    else:
        rect_height_entry.config(state=tk.NORMAL)


IS_SQUARE.trace_add("write", toggle_square_mode)

# Button to refresh the drawing
tk.Button(root, text="Apply", command=draw_random_points).grid(row=5, column=1, columnspan=2, pady=20)

# Initial drawing
draw_random_points()

root.mainloop()