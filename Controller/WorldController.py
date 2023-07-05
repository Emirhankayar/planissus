import sys
sys.path.append(".")

import random, matplotlib, noise, tkinter as tk, numpy as np
from tkinter import ttk
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from Model.Creatures import Erbast, Carviz, Vegetob, Creatures
from Model.WorldModel import Cell
from constants import NUM_CELLS, MAX_DAYS, MAX_LIFE_E, MAX_LIFE_C

matplotlib.use('TkAgg')

# Create a function to initialize the cellsList array
def initialize_cells_list(NUM_CELLS):
    global cellsList, water_cells, colorsList, creatures
    creatures = Creatures()
    creatures.update_num_cells(NUM_CELLS)

    cellsList = np.empty((NUM_CELLS, NUM_CELLS), dtype=object)
    water_cells = np.zeros((NUM_CELLS, NUM_CELLS), dtype=bool)
    colorsList = np.zeros((NUM_CELLS, NUM_CELLS))  # Initialize colorsList with zeros

    scale = 10

    for i in range(NUM_CELLS):
        for j in range(NUM_CELLS):
            noise_value = noise.pnoise2(i / scale, j / scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=NUM_CELLS, repeaty=NUM_CELLS)
            vg = Vegetob()
            vg.row = i
            vg.column = j
            vg.density = vg.generateDensity()
            if noise_value > 0.25 or (i == 25 and j == 25):  # Assign cells as water based on noise threshold
                water_cells[i][j] = True
            else:
                cellsList[i][j] = Cell(i, j, "Ground", vg)

    # Group neighboring water cells together
    for i in range(NUM_CELLS):
        for j in range(NUM_CELLS):
            if water_cells[i][j]:
                if i > 0 and cellsList[i-1][j].terrainType == "Water":
                    cellsList[i][j] = cellsList[i-1][j]
                elif j > 0 and cellsList[i][j-1].terrainType == "Water":
                    cellsList[i][j] = cellsList[i][j-1]
                else:
                    cellsList[i][j] = Cell(i, j, "Water", None)

initialize_cells_list(NUM_CELLS) 

max_days = MAX_DAYS
erb_lifetime = MAX_LIFE_E
carv_lifetime = MAX_LIFE_C
day = 0

cmap = colors.ListedColormap(['blue', 'green', 'yellow', 'red', 'black'])
bounds = [0, 10, 20, 30, 40, 50]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax.minorticks_off()
ax2.minorticks_off()

# Adjust the position and size of each subplot
fig.tight_layout(pad=6)

erb_counter = 0
carv_counter = 0
kill_counter = 0

x_data = [0]

y_erbast_data = [erb_counter]
y_carv_data = [carv_counter]
y_kill_data = [kill_counter]

populations_erbast = [y_erbast_data]
populations_carviz = [y_carv_data]

line_erbast, = ax2.plot(x_data, y_erbast_data, color='yellow', label='Erbast')
line_carv, = ax2.plot(x_data, y_carv_data, color='red', label='Carviz')

im = ax.imshow(colorsList, cmap=cmap, norm=norm)


# Simulation logic
def simulate():
    global cellsList

    for sublist in cellsList:
        for veg in sublist:
            if veg.terrainType != "Water":  # Exclude water cells from growth
                veg.vegetob.grow()

    for row in cellsList:
        for cell in row:
            if cell.erbast:
                cell.erbast.herdDecision(cellsList)
            if cell.pride:
                cell.pride.prideDecision(cellsList)

    for row in cellsList:
        for cell in row:
            if cell.pride:
                cell.pride.fight_between_prides(cell.pride, cellsList)


    for row in cellsList:
        for cell in row:
            if cell.erbast:
                cell.erbast.herdGraze(cellsList)
                cell.erbast.groupAging()
            if cell.pride:
                for cr in cell.pride:
                    if cell.erbast:
                        cr.hunt(cellsList)
                cell.pride.groupAging()

    update_population_counts()

# Update population counts
def update_population_counts():
    global erb_counter, carv_counter, kill_counter
    erb_counter = 0
    carv_counter = 0
    kill_counter = 0


    for row in range(NUM_CELLS):
        for column in range(NUM_CELLS):
            if (
                row < len(cellsList)
                and column < len(cellsList[row])
                and len(cellsList[row][column].erbast) > 0
                and len(cellsList[row][column].pride) > 0
            ):
                carv_counter += 1
                erb_counter += 1
                kill_counter += 1

                colorsList[row][column] = 45
            elif (
                row < len(cellsList)
                and column < len(cellsList[row])
                and len(cellsList[row][column].erbast) > 0
            ):
                erb_counter += 1
                colorsList[row][column] = 25
            elif (
                row < len(cellsList)
                and column < len(cellsList[row])
                and len(cellsList[row][column].pride) > 0
            ):
                colorsList[row][column] = 35
                carv_counter += 1
            elif (
                row < len(cellsList)
                and column < len(cellsList[row])
                and cellsList[row][column].terrainType == "Ground"
            ):
                colorsList[row][column] = 15
            elif (
                row < len(cellsList)
                and column < len(cellsList[row])
                and cellsList[row][column].terrainType == "Water"
            ):
                colorsList[row][column] = 5


# Update the animation frame
def update(frame):
    global day, max_days, title, killmax, carvmax, erbmax, erbtot, carvtot

    day = frame
    simulate()

    im.set_array(colorsList)
    # Calculate the time in Planisuss convention
    centuries = day // 1000
    decades = (day % 1000) // 100
    years = (day % 100) // 10
    months = day % 10

    title_parts = []
    if centuries > 0:
        title_parts.append(f"{centuries} Centuries")
    if decades > 0:
        title_parts.append(f"{decades} Decades")
    if years > 0:
        title_parts.append(f"{years} Years")
    if months > 0:
        title_parts.append(f"{months} Months")

    title = ", ".join(title_parts)
    ax.set_title(title)

    x_data.append(day)
    new_erbast_pop = [erb_counter]
    new_carv_pop = [carv_counter]

    prev_erbast_pop = populations_erbast[-1]
    prev_carv_pop = populations_carviz[-1]

    populations_erbast.append(np.concatenate([prev_erbast_pop, new_erbast_pop]))
    populations_carviz.append(np.concatenate([prev_carv_pop, new_carv_pop]))
    

    y_erbast_data = populations_erbast[-1]
    y_carv_data = populations_carviz[-1]
    y_kill_data.append(kill_counter)
    
    x_erbast_data = np.arange(len(populations_erbast))
    x_carv_data = np.arange(len(populations_carviz))

    line_erbast.set_data(x_erbast_data, y_erbast_data)
    line_carv.set_data(x_carv_data, y_carv_data)

    max_y = max(max(y_erbast_data), max(y_carv_data))
    max_x = max(len(x_erbast_data), len(x_carv_data))
    gap = 0.02 * max(max_x, max_y)  # Calculate the maximum gap
    
    ax2.set_xlim(0, max_x + gap)
    ax2.set_ylim(0, max_y + gap)

    erbmax=max(y_erbast_data)
    carvmax=max(y_carv_data)
    erbtot=sum(y_erbast_data)
    carvtot=sum(y_carv_data)
    killmax = sum(y_kill_data)  # Calculate the maximum of kill_counter

    ax2.set_xlabel('Days')
    ax2.set_ylabel('Population')
    ax2.set_title((f'Max Carviz: {carvmax}      Max Erbast: {erbmax}        \n\n Cur Carviz: {carv_counter}      Cur Erbast: {erb_counter}      Tot Kills: {killmax}'))
    
    ax2.legend()
    # Check if there are no carvizes after the first day
    if day > 0 and carv_counter == 0:
        max_days = day

    # Check if the current day exceeds the maximum days
    if day >= max_days:
        ani.event_source.stop()  # Stop the animation

    return im, line_erbast, line_carv

# Function to start the simulation
def start_simulation():
    global num_erbasts, num_carvizes, erb_lifetime, carv_lifetime, NUM_CELLS, cellsList, water_cells
    interval = interval_slider.get()
    num_erbasts = int(erb_input.get())
    num_carvizes = int(carv_input.get())
    erb_lifetime = int(erbast_lifetime.get())
    carv_lifetime = int(carviz_lifetime.get())
    NUM_CELLS = int(num_cells_combobox.get())  # Update the NUM_CELLS value
    creatures.update_num_cells(NUM_CELLS)
    initialize_cells_list(NUM_CELLS)
    #update_log()
    adjustment_window.destroy()
    main(interval)

# Functions to update the current value labels
def update_erbast_lifetime_label(value):
    value = int(erbast_lifetime.get())
    erbast_lifetime_slider_label.config(text="Erbast Lifetime: {}".format(value))

def update_carviz_lifetime_label(value):
    value = int(carviz_lifetime.get())
    carviz_lifetime_slider_label.config(text="Carviz Lifetime: {}".format(value))

def update_slider_value(event):
    current_value = int(interval_slider.get())
    interval_slider_label.config(text=f"Speed: {current_value}")


def main(interval):
    global ani, button  # Add the slider, animation, and button to the global scope
    # Increase the number of Carvizes
    for _ in range(num_carvizes):
            carv = Carviz(lifetime = carv_lifetime)
            carv_placed = False
            while not carv_placed:
                row = random.randint(0, NUM_CELLS - 1)
                column = random.randint(0, NUM_CELLS - 1)

                if (
                    row < NUM_CELLS and column < NUM_CELLS
                    and row < len(cellsList) and column < len(cellsList[row])
                    and cellsList[row][column].terrainType != "Water"
                ):
                    carv.row = row
                    carv.column = column
                    cellsList[row][column].pride.append(carv)
                    carv_placed = True


    # Increase the number of Erbasts
    for _ in range(num_erbasts):
        erb = Erbast(lifetime = erb_lifetime)
        erb_placed = False
        while not erb_placed:
            row = random.randint(0, NUM_CELLS - 1)
            column = random.randint(0, NUM_CELLS - 1)

            if (
                row < NUM_CELLS and column < NUM_CELLS
                and row < len(cellsList) and column < len(cellsList[row])
                and cellsList[row][column].terrainType != "Water"
                and len(cellsList[row][column].erbast) == 0
            ):
                erb.row = row
                erb.column = column
                cellsList[row][column].erbast.append(erb)
                erb_placed = True

    # Add pause and resume button
    button_ax = plt.axes([0.8, 0.01, 0.1, 0.05])
    button = Button(button_ax, 'Pause/Resume', color='lightgoldenrodyellow', hovercolor='0.975')

    def pause_resume_simulation(event):
        if ani.event_source is None:
            ani.event_source = fig.canvas.new_timer(interval=ani._interval)
            ani.event_source.add_callback(ani._step)
            ani.event_source.start()
            button.label.set_text('Pause')
        else:
            ani.event_source.stop()
            ani.event_source = None
            button.label.set_text('Resume')

    button.on_clicked(pause_resume_simulation)

    # Initialize the animation with the initial slider value
    ani = FuncAnimation(fig, update, frames=range(max_days), interval=interval, blit=False, repeat=False)

    # Display the plot
    plt.show()

# Create the adjustment window
adjustment_window = tk.Tk()
adjustment_window.title("Adjustments")

# Interval Slider
interval_slider_label = ttk.Label(adjustment_window, text="Interval")
interval_slider_label.pack()
interval_slider = ttk.Scale(adjustment_window, from_=1, to=500, orient="horizontal")
interval_slider.pack()
interval_slider.bind("<<Property>>", update_slider_value)

# Erb Count Input
erb_label = ttk.Label(adjustment_window, text="Number of Erbasts")
erb_label.pack()
erb_input = ttk.Entry(adjustment_window)
erb_input.pack()

# Carv Count Input
carv_label = ttk.Label(adjustment_window, text="Number of Carvizes")
carv_label.pack()
carv_input = ttk.Entry(adjustment_window)
carv_input.pack()

# Erbast Lifetime Slider
erbast_lifetime_label = ttk.Label(adjustment_window, text="Erbast Lifetime")
erbast_lifetime_label.pack()
erbast_lifetime = ttk.Scale(adjustment_window, from_=10, to=1000, orient="horizontal", command=update_erbast_lifetime_label)
erbast_lifetime.pack()
erbast_lifetime_slider_label = ttk.Label(adjustment_window, text="Erbast Lifetime: {}".format(erbast_lifetime.get()))
erbast_lifetime_slider_label.pack()

# Carviz Lifetime Slider
carviz_lifetime_label = ttk.Label(adjustment_window, text="Carviz Lifetime")
carviz_lifetime_label.pack()
carviz_lifetime = ttk.Scale(adjustment_window, from_=10, to=1000, orient="horizontal", command=update_carviz_lifetime_label)
carviz_lifetime.pack()
carviz_lifetime_slider_label = ttk.Label(adjustment_window, text="Carviz Lifetime: {}".format(carviz_lifetime.get()))
carviz_lifetime_slider_label.pack()

# Number of Cells Combobox
num_cells_label = ttk.Label(adjustment_window, text="Number of Cells")
num_cells_label.pack()
num_cells_combobox = ttk.Combobox(
    adjustment_window,
    values=["50", "60", "70", "80", "90" ,"100"],
    state="readonly",
)
num_cells_combobox.set(50)
num_cells_combobox.pack()

# Save Animation Checkbox
save_animation = tk.BooleanVar()
save_animation_checkbox = ttk.Checkbutton(adjustment_window, text="Save Animation", variable=save_animation)
save_animation_checkbox.pack()

# Start Button
start_button = ttk.Button(adjustment_window, text="Start Simulation", command=start_simulation)
start_button.pack()

# Set the command option of the sliders to their respective update functions
erbast_lifetime.config(command=update_erbast_lifetime_label)
erbast_lifetime.set(10)  # Set the default value as 10
carviz_lifetime.config(command=update_carviz_lifetime_label)
carviz_lifetime.set(10)  # Set the default value as 10
interval_slider.config(command=update_slider_value)

# Start the Tkinter event loop
adjustment_window.mainloop()
