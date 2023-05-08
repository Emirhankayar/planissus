import time
import cProfile
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
from Model.Creatures import Erbast, Carviz, Vegetob
from Model.WorldModel import Cell, Herd, Pride

matplotlib.use('TkAgg')

NUM_CELLS = 100



cellsList = np.empty((NUM_CELLS, NUM_CELLS), dtype=object)
for i in range(NUM_CELLS):
    for j in range(NUM_CELLS):
        vg = Vegetob()
        vg.row = i
        vg.column = j
        vg.density = vg.generateDensity()
        cellsList[i][j] = Cell(i, j, "Ground", vg)

erb = Erbast()
erb.row = 50
erb.column = 50
cellsList[50][50].erbast.append(erb)

carv = Carviz()
carv.row = 54
carv.column = 54

carv2 = Carviz()
carv2.row = 60
carv2.column = 60

day = 0
max_days = 1000

colorsList = [[0 for q in range(NUM_CELLS)] for w in range(NUM_CELLS)]
cmap = colors.ListedColormap(['blue', 'green', 'yellow', 'red', 'black'])
bounds = [0, 10, 20, 30, 40, 50]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig = plt.figure(figsize=(10, 6))
ax   = fig.add_subplot(121)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(224)

ax.minorticks_off()
ax2.minorticks_off()
ax3.minorticks_off()

# Adjust the position and size of each subplot
fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, wspace=0.2, hspace=0.2)
ax.set_position([0.05, 0.05, 0.45, 0.9])
ax2.set_position([0.55, 0.55, 0.4, 0.4])
ax3.set_position([0.55, 0.05, 0.4, 0.4])

x_erb_data = [0]
ydata = [1]
populations_erbast = [ydata]
ax2.plot(x_erb_data, ydata, color='yellow')
ax2.set_xlim(0, max_days)
ax2.set_ylim(0, 1000)
ax2.set_xlabel('Days')
ax2.set_ylabel('Population')
ax2.set_title('Population of Erbast over time')

x_carv_data = [0]
y_carv_data = [1]
populations_carviz = [y_carv_data]
ax3.plot(x_carv_data, y_carv_data, color='yellow')
ax3.set_xlim(0, max_days)
ax3.set_ylim(0, 1000)
ax3.set_xlabel('Days')
ax3.set_ylabel('Population')
ax3.set_title('Population of Carviz over time')

im = ax.imshow(colorsList, cmap=cmap, norm=norm)

erb_counter = 0
carv_counter = 0

avg_time = 0


def update(day):#
    t1 = time.perf_counter()

    erb_counter = 0
    carv_counter = 0

    movementList = cellsList.copy()

    # GROWING
    if day == 200:
        cellsList[54][54].pride.append(carv)
        cellsList[60][60].pride.append(carv2)

    for sublist in cellsList:
        # Iterate over each object in the sublist
        for veg in sublist:
            # Apply the method to the object
            veg.vegetob.grow()

    # MOVEMENT
    for row in range(len(cellsList)):
        for column in range(len(cellsList[row])):
            if len(cellsList[row][column].erbast) > 0:
                cellsList[row][column].erbast.herdDecision(movementList)
            if len(cellsList[row][column].pride) > 0:
                cellsList[row][column].pride.prideDecision(movementList)

    # STRUGGLE

    for row in range(len(cellsList)):
        for column in range(len(cellsList[row])):
            if len(cellsList[row][column].pride) > 0:
                cellsList[row][column].pride.fight_between_prides(cellsList[row][column].pride, cellsList)

    # GRAZING

    for row in range(len(cellsList)):
        for column in range(len(cellsList[row])):
            if len(cellsList[row][column].erbast) > 0:
                cellsList[row][column].erbast.herdGraze(cellsList)

                cellsList[row][column].erbast.groupAging()

            if len(cellsList[row][column].pride) > 0:
                for cr in cellsList[row][column].pride:
                    if len(cellsList[row][column].erbast) > 0:
                        cr.hunt(cellsList)
            cellsList[row][column].pride.groupAging()

    for v in range(NUM_CELLS):
        for n in range(NUM_CELLS):
            if cellsList[v][n].erbast and cellsList[v][n].pride:
                carv_counter += 1
                erb_counter += 1
                colorsList[v][n] = 45
            elif cellsList[v][n].erbast:
                erb_counter += 1
                colorsList[v][n] = 25

            elif cellsList[v][n].pride:
                colorsList[v][n] = 35
                carv_counter += 1
            else:
                colorsList[v][n] = 15



    im.set_data(colorsList)
    ax.set_title(f"Day {day}")

    x_erb_data.append(day)
    new_pop = [erb_counter]
    prev_pop = populations_erbast[-1]
    populations_erbast.append(np.concatenate([prev_pop, new_pop]))
    ydata = populations_erbast[-1]

    ax2.clear()
    ax2.plot(x_erb_data, ydata, color='yellow')
    ax2.set_xlim(0, 1000)
    ax2.set_ylim(0, 80)
    ax2.set_xlabel('Days')
    ax2.set_ylabel('Population')
    ax2.set_title('Population of Erbast over time')

    x_carv_data.append(day)
    new_pop_carv = [carv_counter]
    prev_pop_carv = populations_carviz[-1]
    populations_carviz.append(np.concatenate([prev_pop_carv, new_pop_carv]))
    y_carv_data = populations_carviz[-1]

    ax3.clear()
    ax3.plot(x_carv_data, y_carv_data, color='red')
    ax3.set_xlim(0, 1000)
    ax3.set_ylim(0, 80)
    ax3.set_xlabel('Days')
    ax3.set_ylabel('Population')
    ax3.set_title('Population of Carviz over time')


from functools import partial

update_frame = partial(update, cellsList.copy())

ani = FuncAnimation(fig, update, frames=max_days, interval=60, blit=False)

plt.show()
