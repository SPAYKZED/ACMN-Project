import tkinter as tk
import random
import tkinter.messagebox
import math

# Initial parameters
WINDOW_SIZE = 1050
SQUARE_SIZE = 775
NUM_POINTS = 100
CIRCLE_RADIUS = 25
NUM_CITIES = 5
CITY_RADIUS = 125

root = tk.Tk()
root.title("Mobile Network Base Stations")
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")

canvas = tk.Canvas(root, bg='white', width=795, height=800)
canvas.grid(row=0, column=0, rowspan=22)


def are_points_within_range(x, y, points, min_distance, max_distance=None):
    for px, py in points:
        distance = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
        if max_distance:
            if min_distance <= distance <= max_distance:
                return True
        else:
            if distance < min_distance:
                return True
    return False

def draw_random_points():
    canvas.delete("all")

    city_radius = int(city_radius_var.get())
    square_size = min(int(square_size_var.get()), 780)
    num_cities = int(num_cities_var.get())
    city_centers = []

    for _ in range(num_cities):
        tries = 0
        while tries < 5000:
            x = random.randint(10 + city_radius, 10 + square_size - city_radius)
            y = random.randint(10 + city_radius, 10 + square_size - city_radius)
            # Проверка пересечения радиусов городов
            if not are_points_within_range(x, y, city_centers, 2 * city_radius):
                city_centers.append((x, y))
                break
            tries += 1

        # Если не удается разместить все города
        if tries == 5000:
            tk.messagebox.showerror("Error", "Not enough space to place all the cities of the given radius.")
            return

    square_size = min(int(square_size_var.get()), 780)
    num_points = int(num_points_var.get())
    circle_radius = int(circle_radius_var.get())
    existing_points = []

    stations_in_city = int(0.8 * num_points)  # 80% станций будут в городах
    stations_outside = num_points - stations_in_city

    # Размещаем станции внутри городов
    stations_per_city = stations_in_city // NUM_CITIES
    for cx, cy in city_centers:
        for _ in range(stations_per_city):
            tries = 0
            while tries < 5000:
                angle = 2 * math.pi * random.random()  # случайный угол
                distance_from_center = city_radius * random.random()  # случайное расстояние от центра, но внутри города
                x = cx + distance_from_center * math.cos(angle)
                y = cy + distance_from_center * math.sin(angle)

                if not are_points_within_range(x, y, existing_points, 0, 1.5 * circle_radius):
                    existing_points.append((x, y))
                    break
                tries += 1

    # Размещаем станции вне городов
    for _ in range(stations_outside):
        tries = 0
        while tries < 5000:
            x = random.randint(10 + circle_radius, 10 + square_size - circle_radius)
            y = random.randint(10 + circle_radius, 10 + square_size - circle_radius)
            if not are_points_within_range(x, y, city_centers, 0, city_radius) and not are_points_within_range(x, y, existing_points,0, 1.5 * circle_radius):
                existing_points.append((x, y))
                break
            tries += 1

    for x, y in existing_points:
        canvas.create_oval(x, y, x + 2, y + 2, fill='black')
        canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, outline='black', width=2)

    # Drawing cities
    for i, (cx, cy) in enumerate(city_centers):
        canvas.create_text(cx, cy - 18, text=chr(65 + i), font=("Arial", 14, "bold"), fill='red')
        canvas.create_line(cx - 10, cy, cx + 10, cy, fill='black')
        canvas.create_line(cx, cy - 10, cx, cy + 10, fill='black')
        canvas.create_oval(cx - city_radius, cy - city_radius, cx + city_radius, cy + city_radius, outline='red', width=1.5)

    canvas.create_rectangle(10, 10, 10 + square_size, 10 + square_size, width=2)

square_size_var = tk.StringVar(value=SQUARE_SIZE)
num_points_var = tk.StringVar(value=NUM_POINTS)
circle_radius_var = tk.StringVar(value=CIRCLE_RADIUS)
city_radius_var = tk.StringVar(value=CITY_RADIUS)
num_cities_var = tk.StringVar(value=NUM_CITIES)

tk.Label(root, text="SQUARE SIZE:").grid(row=0, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=square_size_var).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="NUM POINTS:").grid(row=1, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=num_points_var).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="CIRCLE RADIUS:").grid(row=2, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=circle_radius_var).grid(row=2, column=2, padx=5, pady=5)

tk.Label(root, text="CITY RADIUS:").grid(row=3, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=city_radius_var).grid(row=3, column=2, padx=5, pady=5)

tk.Label(root, text="NUM CITIES:").grid(row=4, column=1, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=num_cities_var).grid(row=4, column=2, padx=5, pady=5)

tk.Button(root, text="\n          Apply          \n", command=draw_random_points).grid(row=5, column=1, columnspan=2, pady=20)

draw_random_points()
root.mainloop()