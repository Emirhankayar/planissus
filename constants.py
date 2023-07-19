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
RESET = '\033[1m'