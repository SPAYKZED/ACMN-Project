import tkinter as tk
import random
import tkinter.messagebox
import math
from PIL import Image, ImageTk

# Initial parameters
WINDOW_SIZE = 1075
SQUARE_SIZE = 775
NUM_POINTS = 100
CIRCLE_RADIUS = 25

root = tk.Tk()
root.title("Mobile Network Base Stations")
root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")

canvas = tk.Canvas(root, bg='white', width=795, height=795)
img = Image.open("C:\\Python\\Project_ACMN\\map_bg.png").resize((SQUARE_SIZE, SQUARE_SIZE))
img_tk = ImageTk.PhotoImage(img)
ph_station = tk.PhotoImage(file='station.png')
root.iconphoto(False,ph_station)
city_icon = Image.open("C:\\Python\\Project_ACMN\\city1.png").resize((30, 30))
city_icon_tk = ImageTk.PhotoImage(city_icon)
canvas.grid(row=0, column=0, rowspan=22)
city_centers = []

def are_points_within_range(x, y, points, min_distance, max_distance=None):
    #This function checks if a given point (x, y) is within a certain distance range of any points from the list.
    for point in points:
        px, py = point[:2]  # Extract the x and y coordinates of the point
        distance = ((x - px) ** 2 + (y - py) ** 2) ** 0.5  # Calculate Euclidean distance
        # If max_distance is provided, check if the point is within the min and max range. Otherwise, check if it's less than min_distance.
        if max_distance:                                                      #param x: x-coordinate of the point
            if min_distance <= distance <= max_distance:                      #param y: y-coordinate of the point
                return True                                                   #param points: list of points (other points to check against)
        else:                                                                 #param min_distance: minimum distance to check
            if distance < min_distance:                                       #param max_distance: maximum distance to check (if specified)
                return True                                                   #return: True if the point is within the specified range
    return False                                                              #of any point in the list, otherwise False


def draw_random_points():
    #Draws random base stations and cities on the canvas based on user parameters.

    canvas.delete("base_station")
    # Drawing the square on the canvas
    canvas.create_rectangle(10, 10, 10 + SQUARE_SIZE, 10 + SQUARE_SIZE, fill='white', width=7)
    canvas.create_image(10, 10, anchor=tk.NW, image=img_tk, tags="background")

    # Gathering and preparing city parameters
    min_cities = int(min_cities_var.get())
    max_cities = int(max_cities_var.get())
    num_cities = random.randint(min_cities, max_cities)
    min_city_radius = int(min_city_radius_var.get())
    max_city_radius = int(max_city_radius_var.get())

    # Checking if cities should be retained or drawn a new
    if not keep_cities_var.get() or not city_centers:
        canvas.delete("city")  # Also delete existing cities if they were drawn previously
        city_centers.clear()

        # Drawing the cities
        for _ in range(num_cities):
            tries = 0
            city_radius = random.randint(min_city_radius, max_city_radius)
            # Finding a position for the city such that it doesn't overlap with other cities
            while tries < 1000:
                x = random.randint(10 + city_radius, 10 + SQUARE_SIZE - city_radius)
                y = random.randint(10 + city_radius, 10 + SQUARE_SIZE - city_radius)
                if not are_points_within_range(x, y, city_centers, 2 * city_radius):
                    city_centers.append((x, y, city_radius))
                    break
                tries += 1
            if tries == 1000:
                tk.messagebox.showerror("Error", "Failed to place all the stations/cities. Try adjusting parameters.")
                return

        # Drawing the city centers and borders on the canvas
        for i, (cx, cy, cradius) in enumerate(city_centers):
            canvas.create_text(cx, cy - 18, text=chr(65 + i), font=("Arial", 14, "bold"), fill='red')
            canvas.create_image(cx, cy, image=city_icon_tk, tags="city")
            canvas.create_oval(cx - cradius, cy - cradius, cx + cradius, cy + cradius, outline='red', width=3, tags="city")

    existing_points = []    # List to store the locations of base stations to prevent overlap
    num_points = int(num_points_var.get())      # Retrieve settings from the UI
    circle_radius = int(circle_radius_var.get())
    percentage_in_city = float(percentage_in_city_var.get())
    percentage_outside = float(percentage_outside_var.get())

    if percentage_in_city + percentage_outside != 100:
        tk.messagebox.showerror("Error", "The sum of percentages should be 100%.")
        return

    # Calculate the number of base stations inside and outside of cities
    stations_in_city = int((percentage_in_city / 100) * num_points)
    stations_outside = num_points - stations_in_city
    stations_per_city = stations_in_city // num_cities

    # Place base stations inside the cities
    for cx, cy, cradius in city_centers:
        for _ in range(stations_per_city):
            tries = 0
            while tries < 1000:
                angle = 2 * math.pi * random.random()   # Randomly choose an angle and distance to position the base station within the city
                distance_from_center = cradius * random.random()
                x = cx + distance_from_center * math.cos(angle)
                y = cy + distance_from_center * math.sin(angle)

                # Ensure this base station doesn't overlap with other base stations
                if not are_points_within_range(x, y, existing_points, 0, 1.4 * circle_radius):
                    existing_points.append((x, y))
                    canvas.create_oval(x, y, x + 3, y + 3, fill='black', tags="base_station")
                    canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, outline='black', width=2, tags="base_station")
                    break
                tries += 1

    # Place base stations outside the cities
    for _ in range(stations_outside):
        tries = 0
        while tries < 1000:
            # Randomly choose a position for the base station
            x = random.randint(10 + circle_radius, 10 + SQUARE_SIZE - circle_radius)
            y = random.randint(10 + circle_radius, 10 + SQUARE_SIZE - circle_radius)

            # Ensure this base station doesn't overlap with cities or other base stations
            if not any(are_points_within_range(x, y, [(cx, cy)], cr) for cx, cy, cr in city_centers) and not are_points_within_range(x, y, existing_points, 0, 1.5 * circle_radius):
                existing_points.append((x, y))
                canvas.create_oval(x, y, x + 3, y + 3, fill='blue', tags="base_station")
                canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, outline='blue', width=2, tags="base_station")
                break
            tries += 1

    # Redraw the cities on the canvas
    for i, (cx, cy, cradius) in enumerate(city_centers):
        canvas.create_text(cx, cy - 18, text=chr(65 + i), font=("Arial", 14, "bold"), fill='red', tags="city")
        canvas.create_image(cx, cy, image=city_icon_tk, tags="city")
        canvas.create_oval(cx - cradius, cy - cradius, cx + cradius, cy + cradius, outline='red', width=3, tags="city")

    # Draw base stations on the canvas
  # for x, y in existing_points:
  #     canvas.create_oval(x, y, x + 2, y + 2, fill='black', tags="base_station")
  #     canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, outline='black', width=2, tags="base_station")


num_points_var = tk.StringVar(value=NUM_POINTS)
circle_radius_var = tk.StringVar(value=CIRCLE_RADIUS)
min_cities_var = tk.StringVar(value="2")
max_cities_var = tk.StringVar(value="5")
min_city_radius_var = tk.StringVar(value="80")
max_city_radius_var = tk.StringVar(value="125")
percentage_in_city_var = tk.StringVar(value="80")
percentage_outside_var = tk.StringVar(value="20")


stations_count_frame = tk.LabelFrame(root, text="Stations Count & Radius", padx=5, pady=5)
stations_count_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
tk.Label(stations_count_frame, text="COUNT:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
tk.Entry(stations_count_frame, textvariable=num_points_var).grid(row=0, column=1, padx=5, pady=5)
tk.Label(stations_count_frame, text="RADIUS:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Entry(stations_count_frame, textvariable=circle_radius_var).grid(row=1, column=1, padx=5, pady=5)


cities_count_frame = tk.LabelFrame(root, text="Cities Count Range", padx=5, pady=5)
cities_count_frame.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
tk.Label(cities_count_frame, text="MIN COUNT:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
tk.Entry(cities_count_frame, textvariable=min_cities_var).grid(row=0, column=1, padx=5, pady=5)
tk.Label(cities_count_frame, text="MAX COUNT:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Entry(cities_count_frame, textvariable=max_cities_var).grid(row=1, column=1, padx=5, pady=5)


city_radius_frame = tk.LabelFrame(root, text="City Radius Range", padx=5, pady=5)
city_radius_frame.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
tk.Label(city_radius_frame, text="MIN:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
tk.Entry(city_radius_frame, textvariable=min_city_radius_var).grid(row=0, column=1, padx=5, pady=5)
tk.Label(city_radius_frame, text="MAX:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Entry(city_radius_frame, textvariable=max_city_radius_var).grid(row=1, column=1, padx=5, pady=5)


stations_percent_frame = tk.LabelFrame(root, text="Stations Percentage", padx=5, pady=5)
stations_percent_frame.grid(row=7, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
tk.Label(stations_percent_frame, text="INSIDE CITY:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
tk.Entry(stations_percent_frame, textvariable=percentage_in_city_var).grid(row=0, column=1, padx=5, pady=5)
tk.Label(stations_percent_frame, text="OUTSIDE CITY:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Entry(stations_percent_frame, textvariable=percentage_outside_var).grid(row=1, column=1, padx=5, pady=5)

keep_cities_var = tk.BooleanVar()
tk.Checkbutton(root, text="Keep cities on map", variable=keep_cities_var).grid(row=10, column=1, columnspan=2, pady=5)
tk.Button(root, text="\n          Apply          \n", command=draw_random_points, activebackground='blue', activeforeground='white', relief='raised', bd=5).grid(row=9, column=1, columnspan=2, pady=20)


draw_random_points()
root.mainloop()