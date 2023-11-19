import random
import numpy as np


class Creatures:

    """
    This class is a parent class to Erbast and Carviz,
    it provides the position of the creature via row and column.
    kernel is used to be later filled with get_adjacent_cells() method.
    """

    NUM_CELLS = None

    def __init__(self):
        self._row = 0
        self._column = 0
        self.kernel = np.empty((0, 0), dtype=object)

    @classmethod
    def update_num_cells(cls, num_cells):
        """
        Used to update the value of the maximum amount of cells in the world grid,
        when the user resizes the world.
        This is used in get_adjacent_cells upper boundaries (max_row and max_col).
        :param num_cells:
        :return:
        """
        cls.NUM_CELLS = num_cells

    def get_adjacent_cells(self, row, col):

        """
        The method uses a double loop with ranges in order to include the neighbouring cells
        :param row:
        :param col:
        :return: A list of neighbouring cells as a list, where each item is a list with two elements,
        row and column respectively.

        """
        adjacent_cells = []
        max_row, max_col = Creatures.NUM_CELLS, Creatures.NUM_CELLS
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (
                        (i >= 0 and j >= 0 and i < max_row and j < max_col)
                        and (i != row or j != col)
                ):
                    adjacent_cells.append([i, j])
        return np.array(adjacent_cells)

    @property
    def row(self):
        """
        :return: current row
        """
        return self._row

    @row.setter
    def row(self, newRow):
        """
        set new row
        :param newRow:
        :return:
        """
        self._row = newRow

    @property
    def column(self):
        """
        :return: current column
        """
        return self._column

    @column.setter
    def column(self, newColumn):
        """
        set a new column
        :param newColumn:
        :return:
        """
        self._column = newColumn


class Vegetob(Creatures):

    """
    A Vegetob is a class inherited from Creatures.
    It has a density, which is usually set using a value of the
    generateDenstity() function
    """

    def __init__(self):
        super().__init__()
        self._density = 0

    @property
    def density(self):
        """
        :return: current density
        """
        return self._density

    @density.setter
    def density(self, newDensity):
        """
        Set a new density, usually used when eaten by Erbast
        :param newDensity:
        :return:
        """
        self._density = int(newDensity)

    def generateDensity(self):
        """
        :return: random int value betwen 1 and 100
        """
        return np.random.randint(1, 100)

    def grow(self):
        """
        Increases the density of this Vegetob by 1,
        restricting the maximum value by 100.
        :return:
        """
        if self.density < 100:
            self.density += 1


class Erbast(Creatures):

    """
    Erbast is a Creature that harvests on Vegetob
    """

    def __init__(self, lifetime=10):
        """
        Energy is a random value between 35 and 95, used for movements
        age: used to determine when should Erbast die of old age.
        soc_attitude: The value here does not really play a role, this parameter is recalculated.
        :param lifetime: can be changed by the user, determines how quickly the creature will age
        hasMoved: used to determine whether to deduct energy on movement
        """
        super().__init__()
        self._energy = np.random.randint(35, 95)
        self.lifetime = lifetime
        self.age = 0
        self.soc_attitude = 1
        self.hasMoved = False

    @property
    def energy(self):
        """
        :return: current energy
        """
        return self._energy

    @energy.setter
    def energy(self, newEnergy):
        """
        sets new energy level, used when grazing
        :param newEnergy:
        :return:
        """
        self._energy = newEnergy

    def aging(self, listOfCreatures):
        """
        Determines whether a creature should die of old age,
        energy exhaustion and whether to leave offsprings or not
        :param listOfCreatures:
        :return:
        """
        self.age += 1

        if self.energy <= 1.0:
            listOfCreatures.remove(self)
        elif self.age >= self.lifetime:
            if self.energy >= 20:
                self.spawnOffsprings(listOfCreatures)
            listOfCreatures.remove(self)
        elif self.age % self.lifetime == 0:
            self.energy -= 1

    def decideMovement(self, listOfHerd, isSocAttitudeHigh):

        """
        Described in the report on Figure 5, as a diagram.
        Method is used to determine where the Erbast should go, based on their parameters.
        :param listOfHerd:
        :param isSocAttitudeHigh:
        :return:
        """

        movement_coordinates = self.findHerd(listOfHerd)
        notFound = movement_coordinates[0] == self.row and movement_coordinates[1] == self.column

        if isSocAttitudeHigh and self.energy >= 30:
            if notFound:
                movement_coordinates = self.findFood(listOfHerd)
                notFound = movement_coordinates[0] == self.row and movement_coordinates[1] == self.column

            if notFound:
                if listOfHerd[self.row][self.column].vegetob.density >= 35:
                    return np.array([self.row, self.column])
                else:
                    if len(self.kernel) > 0:
                        rnd = np.random.randint(0, len(self.kernel))
                        return np.array(self.kernel[rnd])

        else:
            movement_coordinates = self.findFood(listOfHerd)
            notFound = movement_coordinates[0] == self.row and movement_coordinates[1] == self.column

            if notFound and listOfHerd[self.row][self.column].vegetob.density >= 15:
                return np.array([self.row, self.column])

        return movement_coordinates

    def spawnOffsprings(self, listOfCreatures):

        """
        Creates two offsprings, with energy levels of the parent divided by 2
        and places them on the same cell.
        :param listOfCreatures:
        :return:
        """

        energyOfOffsprings = self.energy // 2  # Use floor division for integer result
        erb1 = Erbast()
        erb1.energy = energyOfOffsprings
        erb1.row, erb1.column = self.row, self.column
        erb2 = Erbast()
        erb2.energy = energyOfOffsprings
        erb2.row, erb2.column = self.row, self.column
        listOfCreatures.extend([erb1, erb2])

    def findHerd(self, listOfHerds):

        """
        Finds an adjacent cell with the most amount of Erbasts.
        Default value returns the current coordinates.
        :param listOfHerds:
        :return:
        """

        self.kernel = self.get_adjacent_cells(self.row, self.column)
        maxErbast = 0
        maxErbastCells = []

        for kernel_row, kernel_col in self.kernel:
            if listOfHerds[kernel_row][kernel_col].terrainType == "Ground":
                lenOfErbast = listOfHerds[kernel_row][kernel_col].lenOfErbast()

                if lenOfErbast > maxErbast:
                    maxErbast = lenOfErbast
                    maxErbastCells = [(kernel_row, kernel_col)]
                elif lenOfErbast == maxErbast:
                    maxErbastCells.append((kernel_row, kernel_col))

        return np.array(random.choice(maxErbastCells)) if maxErbastCells else np.array([self.row, self.column])

    def findFood(self, listOfVegetobs):

        """
        Finds an adjacent cell with the most amount of Vegetob density.
        Default value returns the current coordinates.
        :param listOfVegetobs:
        :return:
        """

        self.kernel = self.get_adjacent_cells(self.row, self.column)
        maxDensity = 0
        maxDensityCells = []

        for kernel_row, kernel_col in self.kernel:
            if listOfVegetobs[kernel_row][kernel_col].terrainType == "Ground":
                density = listOfVegetobs[kernel_row][kernel_col].vegetob.density

                if density > maxDensity:
                    maxDensity = density
                    maxDensityCells = [(kernel_row, kernel_col)]
                elif density == maxDensity:
                    maxDensityCells.append((kernel_row, kernel_col))

        return np.array(random.choice(maxDensityCells)) if maxDensityCells else np.array([self.row, self.column])


    def move(self, listOfVegetobs, coordinates):

        """
        Creates a copy of this Erbast, deletes the
        current reference and adds a copy to the
        selected coordinate.
        :param listOfVegetobs:
        :param coordinates:
        :return:
        """

        oldRow, oldCol = self.row, self.column
        newRow, newCol = coordinates

        oldCell = listOfVegetobs[oldRow][oldCol]
        newCell = listOfVegetobs[newRow][newCol]

        oldCell.erbast.remove(self)
        newCell.erbast.append(self)

        self.row, self.column = newRow, newCol
        self.energy -= 1

    def graze(self, listOfVegetobs, amountToEat):
        energyLimit = 100 - self.energy
        energyToEat = min(energyLimit, amountToEat)

        self.energy += energyToEat
        listOfVegetobs[self.row][self.column].vegetob.density -= energyToEat


class Carviz(Creatures):

    """
    Carviz is a Creature that hunts on Erbast
    """

    def __init__(self, lifetime=10):

        """
        Energy is a random value between 35 and 95, used for movements
        age: used to determine when should Erbast die of old age.
        soc_attitude: The value here does not really play a role, this parameter is recalculated.
        :param lifetime: can be changed by the user, determines how quickly the creature will age
        hasMoved: used to determine whether to deduct energy on movement
        previouslyVisited: stores coordinates of the previous position of the carviz.
                           Used in struggle method.
        :param lifetime:
        """

        super().__init__()
        self.previous_position = None
        self._energy = np.random.randint(35, 95)
        self.lifetime = lifetime
        self._age = 0
        self.soc_attitude = 1
        self.previouslyVisited = None
        self.hasMoved = False

    @property
    def energy(self):
        """
        :return: current energy level
        """
        return self._energy

    @energy.setter
    def energy(self, newEnergy):
        """
        sets a new energy level
        :param newEnergy:
        :return:
        """
        self._energy = newEnergy

    @property
    def age(self):
        """
        :return: age
        """
        return self._age

    @age.setter
    def age(self, newAge):
        """
        sets an age of the creature
        :param newAge:
        :return:
        """
        self._age = newAge

    def aging(self, listOfCreatures):

        """
        Determines whether a creature should die of old age,
        energy exhaustion and whether to leave offsprings or not
        :param listOfCreatures:
        :return:
        """

        self.age += 1

        if self.energy <= 1.0:
            listOfCreatures.remove(self)
        elif self.age >= self.lifetime:
            if self.energy >= 20:
                self.spawnOffsprings(listOfCreatures)
            listOfCreatures.remove(self)
        elif self.age % self.lifetime == 0:
            self.energy -= 1

    def spawnOffsprings(self, listOfCreatures):

        """
        Creates two offsprings, with energy levels of the parent divided by 2
        and places them on the same cell.
        :param listOfCreatures:
        :return:
        """

        energyOfOffsprings = self.energy // 2  # Use floor division for integer result

        carv1 = Carviz()
        carv1.energy = energyOfOffsprings
        carv1.row, carv1.column = self.row, self.column

        carv2 = Carviz()
        carv2.energy = energyOfOffsprings
        carv2.row, carv2.column = carv1.row, carv1.column  # Assign row and column from carv1

        listOfCreatures.extend([carv1, carv2])

    def findHerd(self, listOfHerds):

        """
        Find the coordinates of the herd with the most amount of Erbast.
        Default value returns current cell coordinates

        :param listOfHerds:
        :return:
        """

        self.kernel = self.get_adjacent_cells(self.row, self.column)
        maxErbast = 0
        maxErbastCells = []

        for kernel_row, kernel_col in self.kernel:
            herd = listOfHerds[kernel_row][kernel_col]

            if herd.terrainType == "Ground":
                lenOfErbast = herd.lenOfErbast()

                if lenOfErbast > maxErbast:
                    maxErbast = lenOfErbast
                    maxErbastCells = [(herd.row, herd.column)]
                elif lenOfErbast == maxErbast:
                    maxErbastCells.append((herd.row, herd.column))

        return np.array(random.choice(maxErbastCells)) if maxErbastCells else np.array([self.row, self.column])

    def findPride(self, listOfPrides):

        """
        Find the coordinates of the pride with the most number of Carviz.
        Default value returns current cell coordinates.

        :param listOfHerds:
        :return:
        """

        self.kernel = self.get_adjacent_cells(self.row, self.column)
        pride = listOfPrides[self.row][self.column]
        amountOfPride = pride.lenOfCarviz()
        row, column = self.row, self.column

        for kernel_row, kernel_col in self.kernel:
            pride_cell = listOfPrides[kernel_row][kernel_col]

            if pride_cell.terrainType == "Ground":
                lenOfErbast = pride_cell.lenOfErbast()

                if amountOfPride < lenOfErbast:
                    amountOfPride = lenOfErbast
                    row, column = pride_cell.row, pride_cell.column

        return np.array([row, column])



    def move(self, listOfVegetobs, coordinates):

        """
        Creates a copy of this Carviz, deletes the
        current reference and adds a copy to the
        selected coordinate.
        :param listOfVegetobs:
        :param coordinates:
        :return:
        """

        oldRow, oldCol = self.row, self.column
        self.previous_position = (oldRow, oldCol)  # Save the previous position
        self.row, self.column = coordinates

        newCell = listOfVegetobs[self.row][self.column]
        newCell.appendPride(self)
        listOfVegetobs[oldRow][oldCol].delPride(self)

        self.energy -= 1

    def hunt(self, listOfVegetobs):
        """
        This method used by Carviz to hunt of Erbast and increase energy of the Carviz
        1. Finds the list of all erbast on the current cell
        2. Finds an erbast with the maximum energy via a lambda function
        3. If an erbast is found, carviz gains it's energy, such that the resulting
        energy of the carviz does not exceed 100.
        4. Erbast gets deleted/dies
        :param listOfVegetobs:
        :return:
        """
        erbast = listOfVegetobs[self.row][self.column].erbast
        erbSwap = max(erbast, key=lambda erb: erb.energy, default=None)

        if erbSwap is not None:
            maxEnergy = erbSwap.energy
            energy_to_eat = min(100 - self.energy, maxEnergy)

            # Update the energy levels of the creature and plant
            self.energy += energy_to_eat
            erbast.remove(erbSwap)

    def decideMovement(self, listOfPride, isSocAttitudeHigh):

        """
        This method is a navigation procedure for Carviz,
        it's processs is illustrated on figure xx of the report.
        :param listOfPride:
        :param isSocAttitudeHigh:
        :return:
        """

        movement_coordinates = np.array([self.row, self.column])

        if listOfPride[self.row][self.column].lenOfErbast() > 0:
            if isSocAttitudeHigh and self.energy >= 40:
                movement_coordinates = self.findPride(listOfPride)
                if not np.array_equal(movement_coordinates, [self.row, self.column]):
                    return movement_coordinates
            elif not isSocAttitudeHigh and self.energy >= 40:
                movement_coordinates = self.findHerd(listOfPride)
                if not np.array_equal(movement_coordinates, [self.row, self.column]):
                    return movement_coordinates
        else:
            if isSocAttitudeHigh:
                movement_coordinates = self.findPride(listOfPride)
                if not np.array_equal(movement_coordinates, [self.row, self.column]):
                    return movement_coordinates
            else:
                movement_coordinates = self.findHerd(listOfPride)
                if not np.array_equal(movement_coordinates, [self.row, self.column]):
                    return movement_coordinates

        if self.kernel.size > 0:
            movement_coordinates = self.kernel[np.random.choice(self.kernel.shape[0])]

        return movement_coordinates
