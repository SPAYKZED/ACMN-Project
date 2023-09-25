import tkinter as tk
import random
import tkinter.messagebox

# Initial parameters
WINDOW_SIZE = 1050
SQUARE_SIZE = 775
NUM_POINTS = 50
CIRCLE_RADIUS = 30

# Initialize the main window
root = tk.Tk()
root.title("Random Points in Rectangle")
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")

# Create a canvas to draw on
canvas = tk.Canvas(root, bg='white', width=795, height=800)
canvas.grid(row=0, column=0, rowspan=22)

# Check if a new circle overlaps with existing circles
def is_overlapping(x, y, existing_points, circle_radius):
    for ex, ey in existing_points:
        if ((x - ex) ** 2 + (y - ey) ** 2) ** 0.5 < 1.7 * circle_radius:    #The Euclidean distance formula
            return True
    return False


# Function to draw random points inside a rectangle
def draw_random_points():
    canvas.delete("all")

    # Get the entered values from user
    square_size = min(int(square_size_var.get()), 780)
    num_points = int(num_points_var.get())
    circle_radius = int(circle_radius_var.get())

    existing_points = []  # List to store centers of drawn circles

    # Draw circles
    for _ in range(num_points):
        tries = 0
        while tries < 5000:  # maximum number of attempts
            x = random.randint(10 + circle_radius, 10 + square_size - circle_radius)
            y = random.randint(10 + circle_radius, 10 + square_size - circle_radius)
            if not is_overlapping(x, y, existing_points, circle_radius):
                existing_points.append((x, y))
                break
            tries += 1
        else:  # If the maximum number of attempts has been reached
            tk.messagebox.showerror("Error",
                                    "Can't draw the required number of circles without overlapping. Try reducing the number of circles or their size.")
            return

        # Draw the circle and its center point
        canvas.create_oval(x, y, x + 2, y + 2, fill='black')
        canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, outline='black', width=2)

    # Draw the rectangle
    canvas.create_rectangle(10, 10, 10 + square_size, 10 + square_size, width=2)


# Variables to store the entered values
square_size_var = tk.StringVar(value=SQUARE_SIZE)
num_points_var = tk.StringVar(value=NUM_POINTS)
circle_radius_var = tk.StringVar(value=CIRCLE_RADIUS)

# Creating widgets for data input
tk.Label(root, text="SQUARE SIZE:").grid(row=0, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=square_size_var).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="NUM POINTS:").grid(row=1, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=num_points_var).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="CIRCLE RADIUS:").grid(row=2, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=circle_radius_var).grid(row=2, column=2, padx=5, pady=5)


# Button to refresh the drawing
tk.Button(root, text="\n          Apply          \n", command=draw_random_points).grid(row=5, column=1, columnspan=2, pady=20)

# Initial drawing
draw_random_points()

root.mainloop()