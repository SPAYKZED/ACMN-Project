import tkinter as tk
import random
import tkinter.messagebox

# Initial parameters
WINDOW_SIZE = 1050
SQUARE_SIZE = 775
NUM_POINTS = 50
CIRCLE_RADIUS = 30
NUM_CITIES = 5
DEFAULT_CITY_RADIUS = 100

root = tk.Tk()
root.title("Mobile Network Base Stations")
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")

canvas = tk.Canvas(root, bg='white', width=795, height=800)
canvas.grid(row=0, column=0, rowspan=22)

def is_within_distance(x, y, centers, distance):
    for cx, cy in centers:
        if ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 < distance:
            return True
    return False

def is_overlapping(x, y, existing_points, circle_radius):
    for ex, ey in existing_points:
        if ((x - ex) ** 2 + (y - ey) ** 2) ** 0.5 < 1.7 * circle_radius:
            return True
    return False


def draw_random_points():
    canvas.delete("all")

    city_radius = int(city_radius_var.get())

    city_centers = []
    while len(city_centers) < NUM_CITIES:
        x = random.randint(10 + city_radius, SQUARE_SIZE - city_radius)
        y = random.randint(10 + city_radius, SQUARE_SIZE - city_radius)
        # Проверка пересечения радиусов городов
        if not is_within_distance(x, y, city_centers, 2 * city_radius):
            city_centers.append((x, y))

    square_size = min(int(square_size_var.get()), 780)
    num_points = int(num_points_var.get())
    circle_radius = int(circle_radius_var.get())
    existing_points = []

    for _ in range(num_points):
        tries = 0
        while tries < 5000:
            x = random.randint(10 + circle_radius, 10 + square_size - circle_radius)
            y = random.randint(10 + circle_radius, 10 + square_size - circle_radius)
            # Проверка нахождения базовой станции рядом с городом
            if is_within_distance(x, y, city_centers, city_radius):
                probability_threshold = 0.7
            else:
                probability_threshold = 0.3

            if not is_overlapping(x, y, existing_points, circle_radius) and random.random() < probability_threshold:
                existing_points.append((x, y))
                break

            tries += 1
        else:
            tk.messagebox.showerror("Error",
                                    "Can't draw the required number of base stations without overlapping. Try reducing the number of base stations or their size.")
            return

        canvas.create_oval(x, y, x + 2, y + 2, fill='black')
        canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, outline='black', width=2)

    # Drawing cities
    for i, (cx, cy) in enumerate(city_centers):
        canvas.create_text(cx, cy - 18, text=chr(65 + i), font=("Arial", 14, "bold"))
        canvas.create_line(cx - 10, cy, cx + 10, cy, fill='black')
        canvas.create_line(cx, cy - 10, cx, cy + 10, fill='black')
        canvas.create_oval(cx - city_radius, cy - city_radius, cx + city_radius, cy + city_radius, outline='red', width=1.5)

    canvas.create_rectangle(10, 10, 10 + square_size, 10 + square_size, width=2)


square_size_var = tk.StringVar(value=SQUARE_SIZE)
num_points_var = tk.StringVar(value=NUM_POINTS)
circle_radius_var = tk.StringVar(value=CIRCLE_RADIUS)
city_radius_var = tk.StringVar(value=DEFAULT_CITY_RADIUS)

tk.Label(root, text="SQUARE SIZE:").grid(row=0, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=square_size_var).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="NUM POINTS:").grid(row=1, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=num_points_var).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="CIRCLE RADIUS:").grid(row=2, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=circle_radius_var).grid(row=2, column=2, padx=5, pady=5)

tk.Label(root, text="CITY RADIUS:").grid(row=3, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=city_radius_var).grid(row=3, column=2, padx=5, pady=5)

tk.Button(root, text="\n          Apply          \n", command=draw_random_points).grid(row=5, column=1, columnspan=2, pady=20)

draw_random_points()
root.mainloop()