import sys
sys.path.append(".")
import time
import noise 
import random
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from Model.WorldModel import Cell
from constants import NUM_CELLS, MAX_DAYS, MAX_LIFE_E, MAX_LIFE_C, INTERVAL
from Model.Creatures import Vegetob, Carviz, Erbast, Creatures


# 8) Fix total carv and total erb, FIX INTERVAL ?!?
# 9) Fix the carviz water bug
# 10) Optimise

# Set TkAgg backend
plt.switch_backend('TkAgg')

class SimulationInterface:
    def __init__(self):
        self.max_days = MAX_DAYS
        self.erb_lifetime = MAX_LIFE_E
        self.car_lifetime = MAX_LIFE_C
        self.num_cells = NUM_CELLS
        self.interval = INTERVAL
        
        
        self.day = 0
        self.erb_counter = 0
        self.car_counter = 0
        self.hunt_counter = 0

        self.x_data = [0]

        self.y_erb_data = [self.erb_counter]
        self.y_car_data = [self.car_counter]
        self.y_hunt_data = [self.hunt_counter]

        self.pop_erb = [self.y_erb_data]
        self.pop_car = [self.y_car_data]

        self.car_max = 0
        self.erb_max = 0
        self.hunt_tot = 0
        
        self.num_car = 10
        self.num_erb = 20
        self.water_scale = 5
        self.has_started = False
        self.cellsList = np.empty((self.num_cells, self.num_cells), dtype=object)
        self.water_cells = np.zeros((self.num_cells, self.num_cells), dtype=bool)
        self.colorsList = np.zeros((self.num_cells, self.num_cells))
        self.setup_plots()
        self.setup_sliders()
        self.setup_buttons()
        self.button_events()

        self.im = self.ax1.imshow(self.colorsList, cmap=self.cmap, norm=self.norm)

        self.animation = None
        self.animation_paused = True
        self.initialize_animation()
        self.run_flag = 0
        self.has_fin = False

    def setup_animation_values(self):

        self.interval = self.slider1.val
        self.num_cells = self.slider2.val
        self.num_car = self.slider3.val
        self.car_lifetime = self.slider4.val
        self.num_erb = self.slider5.val
        self.erb_lifetime = self.slider6.val
        self.water_scale = self.slider7.val
        self.get_init_values()

        self.cellsList = np.empty((self.num_cells, self.num_cells), dtype=object)
        self.water_cells = np.zeros((self.num_cells, self.num_cells), dtype=bool)
        self.colorsList = np.zeros((self.num_cells, self.num_cells))

        self.im = self.ax1.imshow(self.colorsList, cmap=self.cmap, norm=self.norm)

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
        self.slider7 = Slider(self.slider7_ax, 'Water Amount', 1, 20, valinit=15, valstep=5)

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
        creatures.update_num_cells(self.num_cells)
        scale = self.water_scale

        for i in range(self.num_cells):
            for j in range(self.num_cells):
                noise_value = noise.pnoise2(i / scale, j / scale, octaves=6, persistence=0.5, lacunarity=2.0,
                                            repeatx=self.num_cells, repeaty=self.num_cells)
                vg = Vegetob()
                vg.row = i
                vg.column = j
                vg.density = vg.generateDensity()
                if noise_value > 0.25:  # Assign cells as water based on noise threshold
                    self.water_cells[i][j] = True
                else:
                    self.cellsList[i][j] = Cell(i, j, "Ground", vg)

        # Group neighboring water cells together
        for i in range(self.num_cells):
            for j in range(self.num_cells):
                if self.water_cells[i][j]:
                    if i > 0 and self.cellsList[i - 1][j].terrainType == "Water":
                        self.cellsList[i][j] = self.cellsList[i - 1][j]
                    elif j > 0 and self.cellsList[i][j - 1].terrainType == "Water":
                        self.cellsList[i][j] = self.cellsList[i][j - 1]
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
        self.erb_counter = 0
        self.car_counter = 0
        self.hunt_counter = 0

        for row in range(self.num_cells):
            for column in range(self.num_cells):
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
        if self.has_started:
            self.simulate()
            self.day += 1
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
            self.ax1.title.set_fontsize(8)
            self.title = title
            self.x_data.append(self.day)

            new_erb_pop = [self.erb_counter]
            new_car_pop = [self.car_counter]

            prev_erb_pop = self.pop_erb[-1]
            prev_car_pop = self.pop_car[-1]

            self.pop_erb.append(np.concatenate([prev_erb_pop, new_erb_pop]))
            self.pop_car.append(np.concatenate([prev_car_pop, new_car_pop]))

            self.y_erb_data = self.pop_erb[-1]
            self.y_car_data = self.pop_car[-1]
            self.y_hunt_data.append(self.hunt_counter)

            self.x_erb_data = np.arange(len(self.pop_erb))
            self.x_car_data = np.arange(len(self.pop_car))

            self.line_erb[0].set_data(self.x_erb_data, self.y_erb_data)
            self.line_car[0].set_data(self.x_car_data, self.y_car_data)

            max_y = max(max(self.y_erb_data), max(self.y_car_data))
            max_x = max(len(self.x_erb_data), len(self.x_car_data))
            gap = 0.02 * max(max_x, max_y)  # Calculate the maximum gap

            self.ax2.set_xlim(0, max_x + gap)
            self.ax2.set_ylim(0, max_y + gap)

            self.erb_max = max(self.y_erb_data)
            self.car_max = max(self.y_car_data)

            self.erb_tot = sum(self.y_erb_data)
            self.car_tot = sum(self.y_car_data)

            self.hunt_tot = sum(self.y_hunt_data)
            
            
            self.ax2.set_xlabel('Days', fontsize=8)
            self.ax2.set_ylabel('Population', fontsize=8)

            self.ax2.set_title((
                f'\n\n Max Carviz: {self.car_max}      Max Erbast: {self.erb_max}      Cur Carviz: {self.car_counter}      Cur Erbast: {self.erb_counter}      Tot Kills: {self.hunt_tot}'))
            self.ax2.title.set_fontsize(8)
            

            if self.day >= 0 and self.car_counter == 0:
                self.run_flag += 1
                time.sleep(0.1)
                self.animation.event_source.stop()  # Stop the animation 
                if self.erb_counter > 0:
                    print("Erbasts survived!")
                self.get_final_values()
                self.save_simulation_data()
                self.read_pickle_file('simulation_data.pickle')
        
            return self.im, self.line_erb, self.line_car

    def initialize_animation(self):
        interval = 60
        self.animation = FuncAnimation(
            self.fig, self.update, interval=interval, save_count=200
        )
        print(1, interval)
        self.animation.pause()  # Pause the animation initially

    def start_animation(self, event=None):
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
        self.setup_animation_values()
        interval = self.interval
    
        self.initialize_cells_list()

        self.has_started = True

        self.im.set_array(self.colorsList)

        if self.animation_paused:
            self.animation_paused = False
            # place creatures on the cells list
            self.animate()

            if self.animation is None:
                self.animation = FuncAnimation(self.fig, self.update, interval=interval, save_count=200)
                print(2, interval)
                self.animation.event_source.start()

            # Disable the "Start" button
            self.start_button.set_active(False)
            self.start_button.color = 'gray'  # Optional: Change button color to indicate it's disabled
                    
        elif not self.animation_paused and self.has_started:
            self.animate()
            self.animation.new_frame_seq()

    def reset_animation(self, event=None):
        if self.animation_paused:
            # If triggered while paused
            self.animation_paused = False
            self.animation.event_source.start()
            self.start_animation()

        else:
            # If triggered while running
            self.animation_paused = False
            self.animation.event_source.start()
            self.start_animation()

    def pause_animation(self, event):
        if not self.animation_paused:
            self.animation.event_source.stop()
            self.animation_paused = True

        else:
            self.animation.event_source.start()
            self.animation_paused = False

    def animate(self):
        if not self.animation_paused:
            for _ in range(self.num_car):
                carv = Carviz(lifetime=self.car_lifetime)
                carv_placed = False
                while not carv_placed:
                    row = random.randint(0, self.num_cells - 1)
                    column = random.randint(0, self.num_cells - 1)

                    if (
                        row < self.num_cells and column < self.num_cells
                        and row < len(self.cellsList) and column < len(self.cellsList[row])
                        and self.cellsList[row][column].terrainType != "Water"
                    ):
                        carv.row = row
                        carv.column = column
                        self.cellsList[row][column].pride.append(carv)
                        carv_placed = True

            for _ in range(self.num_erb):
                erb = Erbast(lifetime=self.erb_lifetime)
                erb_placed = False
                while not erb_placed:
                    row = random.randint(0, self.num_cells - 1)
                    column = random.randint(0, self.num_cells - 1)
                    if (
                            row < self.num_cells and column < self.num_cells
                            and row < len(self.cellsList) and column < len(self.cellsList[row])
                            and self.cellsList[row][column].terrainType != "Water"
                            and len(self.cellsList[row][column].erbast) == 0
                    ):
                        erb.row = row
                        erb.column = column
                        self.cellsList[row][column].erbast.append(erb)
                        erb_placed = True

    def get_init_values(self):
        init_values = {
            'interval'    : self.slider1.val,
            'num_cells'   : self.slider2.val,
            'num_car'     : self.slider3.val,
            'car_lifetime': self.slider4.val,
            'num_erb'     : self.slider5.val,
            'erb_lifetime': self.slider6.val,
            'water_scale' : self.slider7.val
        }
        return init_values

    def get_final_values(self):
        final_values = {
            'run_amount'  : self.run_flag,
            'tot_carv'    : self.car_tot,
            'tot_erb'     : self.erb_tot,
            'max_carviz'  : self.car_max,
            'max_erbast'  : self.erb_max,
            'tot_kills'   : self.hunt_tot
        }
        return final_values
    
    def save_simulation_data(self):
        # Get the initial and final values
        init_values = self.get_init_values()
        final_values = self.get_final_values()

        # Combine the values into a single dictionary
        simulation_data = {
            'Initial Values': init_values,
            'Final Values': final_values
        }

        try:
            with open('simulation_data.pickle', 'rb') as file:
                data = pickle.load(file)
                if isinstance(data, dict):
                    prev_values = data
                else:
                    prev_values = {}
        except FileNotFoundError:
            prev_values = {}

        # Update the previous values with the new values
        updated_values = {**prev_values, **simulation_data}

        # Save the updated values to the file
        with open('simulation_data.pickle', 'wb') as file:
            pickle.dump(updated_values, file)

        print("Simulation data saved successfully.\n")

    def read_pickle_file(self, file_path):
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            self.content = data

        for title, content in self.content.items():
            print(title + ":")
            print(content)
            print()

if __name__ == '__main__':
    sim = SimulationInterface()
    plt.show()

