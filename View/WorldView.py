import matplotlib
import numpy as np
from matplotlib import colors


matplotlib.rcParams["toolbar"] = "toolmanager"
import matplotlib.pyplot as plt


class WorldView:
    def __init__(self, cellsList):
        self.cellsList = cellsList

        self.bounds = [0, 10, 20, 30]

    def display(self):
        cmap = colors.ListedColormap(['blue', 'green', 'yellow'])
        norm = colors.BoundaryNorm(self.bounds, cmap.N)
        fig, ax = plt.subplots()
        im = ax.imshow(self.cellsList, cmap=cmap, norm=norm)

        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.03)
        ax.set_xticks(np.arange(-.5, 10, 1))
        ax.set_yticks(np.arange(-.5, 10, 1))
        plt.axis('off')

        plt.show()

