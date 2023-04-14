import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_tools import ToolBase, ToolToggleBase
import time
from Model.Creatures import Erbast

plt.rcParams['toolbar'] = 'toolmanager'


class NewDayTool(ToolToggleBase):
    """Show lines with a given gid."""
    default_keymap = 'S'
    description = 'Show by gid'
    default_toggled = True

    def __init__(self, *args, data, ax, norm, cmap, **kwargs):
        self.data = data
        self.a = ax
        self.cmap = cmap
        self.norm = norm
        super().__init__(*args, **kwargs)

    def enable(self, *args):

        self.update()

    def disable(self, *args):
        self.update()

    def update(self):
        self.a.set_data()
        self.figure.canvas.draw()
