# planisuss_constants.py
"""
Collection of the main constants defined for the
"Planisuss" project.

Values can be modified according to the envisioned behavior of the
simulated world.

---
v 1.00
Stefano Ferrari
2023-02-07
"""

import sys
sys.path.append(".")

### Game constants
# Length of the simulation in days
MAX_DAYS = 10000   
# Size of the (square) grid (NUMCELLS x NUMCELLS)
NUM_CELLS = 50       
# Max life span of Carviz
MAX_LIFE_C = 10
# Max life span of Erbast
MAX_LIFE_E = 10

# Colours for terminal
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
<<<<<<< HEAD
RESET = '\033[1m'

# geometry
NUMCELLS_R = 1000    # number of rows of the (potentially non-square) grid
NUMCELLS_C = 1000    # number of columns of the (potentially non-square) grid

# social groups
NEIGHBORHOOD = 1     # radius of the region that a social group can evaluate to decide the movement
NEIGHBORHOOD_E = 1   # radius of the region that a herd can evaluate to decide the movement
NEIGHBORHOOD_C = 1   # radius of the region that a pride can evaluate to decide the movement

MAX_HERD = 1000      # maximum numerosity of a herd
MAX_PRIDE = 100      # maximum numerosity of a pride

=======
RESET = '\033[1m'
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
