import sys
sys.path.append(".")

import numpy as np, matplotlib.pyplot as plt, noise, random
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from matplotlib import colors
from Model.WorldModel import Cell
from constants import NUM_CELLS, MAX_DAYS, MAX_LIFE_E, MAX_LIFE_C
from Model.Creatures import Vegetob ,Carviz, Erbast, Creatures



#THINGS TODO
#1) Right now animation can run on this window that's nice
#2) Once you click run the window needs to open but animation shouldn't show up plots should be empty
#3) You should be able to do some adjustments so after the second step we can handle sliders and values
#4) there are titles we need to adjust their positions not a problem easy thing
#5) Titles are not showing the correct value but they suppose to so not a problem easy
#6) We should handle reset button from my experience I can say that one is an ass so problematic
#7) Implement a data collector by using pickle
#8) Fix the carvizes bugging in the water
#9) Optimise if you can
#10) Add a title that shows total amount of creatures  
# Set TkAgg backend
plt.switch_backend('TkAgg')

class SimulationInterface():
    def __init__(self):
        self.max_days = MAX_DAYS
        self.erb_lifetime = MAX_LIFE_E
        self.car_lifetime = MAX_LIFE_C
        self.day = 0
        self.erb_counter = 0
        self.car_counter = 0
        self.hunt_counter = 0
        self.x_data = [0]
        self.y_data = [0]
        self.y_erb_data = [self.erb_counter]
        self.y_car_data = [self.car_counter]
        self.y_hunt_data = [self.hunt_counter]
        self.pop_erb = [self.y_erb_data]
        self.pop_car = [self.y_car_data]
        self.num_car = 10
        self.num_erb = 20

        self.cellsList = np.empty((NUM_CELLS, NUM_CELLS), dtype=object)
        self.water_cells = np.zeros((NUM_CELLS, NUM_CELLS), dtype=bool)
        self.colorsList = np.zeros((NUM_CELLS, NUM_CELLS))


        self.setup_plots()
        self.setup_sliders()
        self.setup_buttons()
        self.button_events()
        self.initialize_cells_list()
        self.animate()
        self.animation = FuncAnimation(self.fig, self.update, interval=60, save_count=200)
        self.animation_paused = True
        self.start_animation()


    def setup_plots(self):
        # Create Plots
        self.cmap = colors.ListedColormap(['blue', 'green', 'yellow', 'red', 'black'])
        self.bounds = [0, 10, 20, 30, 40, 50]
        self.norm = colors.BoundaryNorm(self.bounds, self.cmap.N)
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.ax1.minorticks_off()
        self.ax2.minorticks_off()
        self.line_erb = self.ax2.plot(self.x_data, self.y_erb_data, color='yellow', label='Erbast')
        self.line_car = self.ax2.plot(self.x_data, self.y_car_data, color='red', label='Carviz')
        self.im = self.ax1.imshow(self.colorsList, cmap=self.cmap, norm=self.norm)
        self.fig.subplots_adjust(bottom=0.35, top=0.95, left=0.1, right=0.9, wspace=0.3)

    def setup_sliders(self):
        # Create sliders
        self.slider1_ax = self.fig.add_axes([0.15, 0.25, 0.25, 0.03])
        self.slider2_ax = self.fig.add_axes([0.15, 0.2, 0.25, 0.03])
        self.slider3_ax = self.fig.add_axes([0.15, 0.15, 0.25, 0.03])
        self.slider4_ax = self.fig.add_axes([0.15, 0.1, 0.25, 0.03])
        self.slider5_ax = self.fig.add_axes([0.6, 0.25, 0.25, 0.03])
        self.slider6_ax = self.fig.add_axes([0.6, 0.2, 0.25, 0.03])
        self.slider7_ax = self.fig.add_axes([0.6, 0.15, 0.25, 0.03])

        self.slider1 = Slider(self.slider1_ax, 'Animation Speed', 0, 500, valinit=60, valstep=10)
        self.slider2 = Slider(self.slider2_ax, 'Number Cells', 50, 100, valinit=50, valstep=10)
        self.slider3 = Slider(self.slider3_ax, 'Carviz Pop', 10, 500, valinit=10, valstep=1)
        self.slider4 = Slider(self.slider4_ax, 'Carviz Life', 10, 1000, valinit=10, valstep=1)
        self.slider5 = Slider(self.slider5_ax, 'Erbast Pop', 10, 500, valinit=10, valstep=1)
        self.slider6 = Slider(self.slider6_ax, 'Erbast Life', 10, 1000, valinit=10, valstep=1)
        self.slider7 = Slider(self.slider7_ax, 'Water Amount', 0, 20, valinit=5, valstep=5)

    def setup_buttons(self):
        # Create buttons
        self.start_button_ax = self.fig.add_axes([0.3, 0.05, 0.1, 0.04])
        self.reset_button_ax = self.fig.add_axes([0.45, 0.05, 0.1, 0.04])
        self.pause_button_ax = self.fig.add_axes([0.6, 0.05, 0.1, 0.04])
        
        self.start_button = Button(self.start_button_ax, 'Start')
        self.reset_button = Button(self.reset_button_ax, 'Reset')
        self.pause_button = Button(self.pause_button_ax, 'Pause/Resume')
    
    def button_events(self):
        # Set button click events
        self.start_button.on_clicked(self.start_animation)
        self.pause_button.on_clicked(self.pause_animation)
        self.reset_button.on_clicked(self.reset_animation)

    def initialize_cells_list(self):
        creatures = Creatures()
        creatures.update_num_cells(NUM_CELLS)
        scale = 10

        for i in range(NUM_CELLS):
            for j in range(NUM_CELLS):
                noise_value = noise.pnoise2(i / scale, j / scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=NUM_CELLS, repeaty=NUM_CELLS)
                vg = Vegetob()
                vg.row = i
                vg.column = j
                vg.density = vg.generateDensity()
                if noise_value > 0.25 or (i == 25 and j == 25):  # Assign cells as water based on noise threshold
                    self.water_cells[i][j] = True
                else:
                    self.cellsList[i][j] = Cell(i, j, "Ground", vg)

        # Group neighboring water cells together
        for i in range(NUM_CELLS):
            for j in range(NUM_CELLS):
                if self.water_cells[i][j]:
                    if i > 0 and self.cellsList[i-1][j].terrainType == "Water":
                        self.cellsList[i][j] = self.cellsList[i-1][j]
                    elif j > 0 and self.cellsList[i][j-1].terrainType == "Water":
                        self.cellsList[i][j] = self.cellsList[i][j-1]
                    else:
                       self.cellsList[i][j] = Cell(i, j, "Water", None)

    def simulate(self):
        for sublist in self.cellsList:
            for veg in sublist:
                if veg.terrainType != "Water":  # Exclude water cells from growth
                    veg.vegetob.grow()

        for row in self.cellsList:
            for cell in row:
                if cell.erbast:
                    cell.erbast.herdDecision(self.cellsList)
                if cell.pride:
                    cell.pride.prideDecision(self.cellsList)

        for row in self.cellsList:
            for cell in row:
                if cell.pride:
                    cell.pride.fight_between_prides(cell.pride, self.cellsList)


        for row in self.cellsList:
            for cell in row:
                if cell.erbast:
                    cell.erbast.herdGraze(self.cellsList)
                    cell.erbast.groupAging()
                if cell.pride:
                    for cr in cell.pride:
                        if cell.erbast:
                            cr.hunt(self.cellsList)
                    cell.pride.groupAging()
        
        self.update_population_counts()


    def update_population_counts(self):

        for row in range(NUM_CELLS):
            for column in range(NUM_CELLS):
                if (
                    row < len(self.cellsList)
                    and column < len(self.cellsList[row])
                    and len(self.cellsList[row][column].erbast) > 0
                    and len(self.cellsList[row][column].pride) > 0
                ):
                    self.car_counter += 1
                    self.erb_counter += 1
                    self.hunt_counter += 1

                    self.colorsList[row][column] = 45
                elif (
                    row < len(self.cellsList)
                    and column < len(self.cellsList[row])
                    and len(self.cellsList[row][column].erbast) > 0
                ):
                    self.erb_counter += 1
                    self.colorsList[row][column] = 25
                elif (
                    row < len(self.cellsList)
                    and column < len(self.cellsList[row])
                    and len(self.cellsList[row][column].pride) > 0
                ):
                    self.colorsList[row][column] = 35
                    self.car_counter += 1
                elif (
                    row < len(self.cellsList)
                    and column < len(self.cellsList[row])
                    and self.cellsList[row][column].terrainType == "Ground"
                ):
                    self.colorsList[row][column] = 15
                elif (
                    row < len(self.cellsList)
                    and column < len(self.cellsList[row])
                    and self.cellsList[row][column].terrainType == "Water"
                ):
                    self.colorsList[row][column] = 5

    def update(self, frame):

        self.simulate()

        self.im.set_array(self.colorsList)
        # Calculate the time in Planisuss convention
        centuries = self.day // 1000
        decades = (self.day % 1000) // 100
        years = (self.day % 100) // 10
        months = self.day % 10

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
        self.ax1.set_title(title)

        self.x_data.append(self.day)

        new_erb_pop = [self.erb_counter]
        new_car_pop = [self.car_counter]

        prev_erb_pop = self.pop_erb[-1]
        prev_car_pop = self.pop_car[-1]

        self.pop_erb.append(np.concatenate([prev_erb_pop, new_erb_pop]))
        self.pop_car.append(np.concatenate([prev_car_pop, new_car_pop]))
        

        y_erb_data = self.pop_erb[-1]
        y_car_data = self.pop_car[-1]
        self.y_hunt_data.append(self.hunt_counter)
        
        x_erb_data = np.arange(len(self.pop_erb))
        x_car_data = np.arange(len(self.pop_car))

        #self.line_erb.set_data(x_erb_data, y_erb_data)
        #self.line_car.set_data(x_car_data, y_car_data)

        max_y = max(max(y_erb_data), max(y_car_data))
        max_x = max(len(x_erb_data), len(x_car_data))
        gap = 0.02 * max(max_x, max_y)  # Calculate the maximum gap
        
        self.ax2.set_xlim(0, max_x + gap)
        self.ax2.set_ylim(0, max_y + gap)

        erb_max=max(y_erb_data)
        car_max=max(y_car_data)

        erb_tot=sum(y_erb_data)
        car_tot=sum(y_car_data)

        hunt_tot = sum(self.y_hunt_data)

        self.ax2.set_xlabel('Days')
        self.ax2.set_ylabel('Population')
        self.ax2.set_title((f'Max Carviz: {car_max}      Max Erbast: {erb_max}        \n\n Cur Carviz: {self.car_counter}      Cur Erbast: {self.erb_counter}      Tot Kills: {hunt_tot}'))
        max_days = self.max_days
        # Check if there are no carvizes after the first day
        if self.day > 0 and self.car_counter == 0:
            max_days = self.day

        # Check if the current day exceeds the maximum days
        if self.day >= max_days:
            self.animation.event_source.stop()  # Stop the animation

        return self.im, self.line_erb, self.line_car

    def start_animation(self, event=None):
        if self.animation_paused:
            self.animation.event_source.start()
            self.animation_paused = False

    def reset_animation(self, event):
        self.day = 0
        self.erb_counter = 0
        self.car_counter = 0
        self.hunt_counter = 0
        self.x_data = [0]
        self.y_data = [0]
        self.y_erb_data = [self.erb_counter]
        self.y_car_data = [self.car_counter]
        self.y_hunt_data = [self.hunt_counter]
        self.pop_erb = [self.y_erb_data]
        self.pop_car = [self.y_car_data]
        self.setup_plots()

    def pause_animation(self, event):
        if not self.animation_paused:
            self.animation.event_source.stop()
            self.animation_paused = True

    def animate(self):
            for _ in range(self.num_car):
                    carv = Carviz(lifetime = self.car_lifetime)
                    carv_placed = False
                    while not carv_placed:
                        row = random.randint(0, NUM_CELLS - 1)
                        column = random.randint(0, NUM_CELLS - 1)

                        if (
                            row < NUM_CELLS and column < NUM_CELLS
                            and row < len(self.cellsList) and column < len(self.cellsList[row])
                            and self.cellsList[row][column].terrainType != "Water"
                        ):
                            carv.row = row
                            carv.column = column
                            self.cellsList[row][column].pride.append(carv)
                            carv_placed = True

            for _ in range(self.num_erb):
                erb = Erbast(lifetime = self.erb_lifetime)
                erb_placed = False
                while not erb_placed:
                    row = random.randint(0, NUM_CELLS - 1)
                    column = random.randint(0, NUM_CELLS - 1)

                    if (
                        row < NUM_CELLS and column < NUM_CELLS
                        and row < len(self.cellsList) and column < len(self.cellsList[row])
                        and self.cellsList[row][column].terrainType != "Water"
                        and len(self.cellsList[row][column].erbast) == 0
                    ):
                        erb.row = row
                        erb.column = column
                        self.cellsList[row][column].erbast.append(erb)
                        erb_placed = True

if __name__ == '__main__':
    sim = SimulationInterface()
    plt.show()