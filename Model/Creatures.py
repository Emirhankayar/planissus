import numpy as np


class Creatures:
    def __init__(self):
        self._row = 0
        self._column = 0
        self.kernel = self.get_adjacent_cells(self.row, self.column)

    # Generates a list of adjacent cells
    def get_adjacent_cells(self, row, col):
        adjacent_cells = []
        max_row, max_col = 100, 100
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i >= 0 and j >= 0 and i < max_row and j < max_col and (i != row or j != col)):
                    adjacent_cells.append([i, j])
        return np.array(adjacent_cells)

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, newRow):
        self._row = newRow

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, newColumn):
        self._column = newColumn


class Vegetob(Creatures):
    def __init__(self):
        super().__init__()
        self._density = 0

    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, newDensity):
        self._density = newDensity

    def generateDensity(self):
        return np.random.randint(1, 100)

    def grow(self):
        if self.density < 100:
            self.density += 1


class Erbast(Creatures):
    def __init__(self):
        super().__init__()
        self._energy = np.random.randint(20, 100)
        self.lifetime = 10
        self.age = 0
        self.soc_attitude = 1
        self.inHerd = False
        self.previouslyVisited = None
        self.hasMoved = False

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, newEnergy):
        self._energy = newEnergy

    def aging(self, listOfCreatures):
        a = self
        self.age += 1
        if self.energy <= 0:
            listOfCreatures.remove(a)
        elif self.age % 10 == 0:
            self.energy -= 1
        elif self.age >= self.lifetime:
            if self.energy > 20:
                self.spawnOffsprings(listOfCreatures)
            listOfCreatures.remove(a)

    def spawnOffsprings(self, listOfCreatures):
        energyOfOffsprings = int(self.energy / 2)
        erb1 = Erbast()
        erb1.energy = energyOfOffsprings
        erb1.row, erb1.column = self.row, self.column
        erb2 = Erbast()
        erb2.energy = energyOfOffsprings
        erb2.row, erb2.column = self.row, self.column
        listOfCreatures.extend([erb1, erb2])

    def findHerd(self, listOfHerds):
        self.kernel = self.get_adjacent_cells(self.row, self.column)

        amountOfErbast = listOfHerds[self.row][self.column].lenOfErbast()
        row, column = self.row, self.column

        for (r, c), _ in np.ndenumerate(self.kernel):
            if listOfHerds[r][c].terrainType == "Ground":
                if amountOfErbast < listOfHerds[r][c].lenOfErbast():
                    amountOfErbast = listOfHerds[r][c].lenOfErbast()
                    row, column = listOfHerds[r][c].row, listOfHerds[r][c].column

        return np.array([row, column])

    def findFood(self, listOfVegetobs):
        self.kernel = self.get_adjacent_cells(self.row, self.column)
        maxDensity = 0
        row, column = self.row, self.column
        for kernel_idx in range(self.kernel.shape[0]):
            kernel_row, kernel_col = self.kernel[kernel_idx]
            if listOfVegetobs[kernel_row][kernel_col].terrainType == "Ground":
                if maxDensity < listOfVegetobs[kernel_row][kernel_col].vegetob.density:
                    maxDensity = listOfVegetobs[kernel_row][kernel_col].vegetob.density
                    row, column = listOfVegetobs[kernel_row][kernel_col].row, listOfVegetobs[kernel_row][
                        kernel_col].column
        return np.array([row, column])

    def changeSocAttitude(self):
        if self.energy >= 20 or self.energy >= 80:
            self.soc_attitude = 0
        else:
            self.soc_attitude = 1

    def move(self, listOfVegetobs, coordinates):
        a = self
        oldRow, oldCol = self.row, self.column
        self.row, self.column = coordinates
        listOfVegetobs[self.row][self.column].appendErbast(self)
        listOfVegetobs[oldRow][oldCol].delErbast(a)
        self.energy -= 1

    def graze(self, listOfVegetobs):
        energy_to_eat = min(100 - self.energy, listOfVegetobs[self.row][self.column].vegetob.density)
        # Update the energy levels of the creature and plant
        self.energy += energy_to_eat
        listOfVegetobs[self.row][self.column].vegetob.density -= energy_to_eat
        self.changeSocAttitude()


class Carviz(Creatures):

    def __init__(self):
        super().__init__()
        self._energy = np.random.randint(20, 100)
        self.lifetime = 20
        self._age = 0
        self.soc_attitude = 1
        self.previouslyVisited = None
        self.hasMoved = False

    # def __str__(self):
    #     return f"(coordinates: {self.row}, {self.column}, Energy: {self.energy}, Age: {self.age}, SocAtt: {self.soc_attitude}, {self.previouslyVisited}, {self.hasMoved})"
    #
    # def __repr__(self):
    #     return self.__str__()

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, newEnergy):
        self._energy = newEnergy

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, newAge):
        self._age = newAge

    def aging(self, listOfCreatures):
        a = self
        self.age += 1
        if self.energy <= 0:
            listOfCreatures.remove(a)
        elif self.age >= self.lifetime:
            if self.energy > 20:
                self.spawnOffsprings(listOfCreatures)
            listOfCreatures.remove(a)
        elif self.age % 10 == 0:
            self.energy -= 1

    def spawnOffsprings(self, listOfCreatures):

        energyOfOffsprings = int(self.energy / 2)

        carv1 = Carviz()
        carv1.energy = energyOfOffsprings
        carv1.row = self.row
        carv1.column = self.column
        carv2 = Carviz()
        carv2.energy = energyOfOffsprings
        carv2.row = self.row
        carv2.column = self.column
        listOfCreatures.append(carv1)
        listOfCreatures.append(carv2)

    def findHerd(self, listOfHerds):
        # TODO ERROR HERE
        self.kernel = self.get_adjacent_cells(self.row, self.column)

        amountOfErbast = listOfHerds[self.row][self.column].lenOfErbast()
        row, column = self.row, self.column

        for (r, c), _ in np.ndenumerate(self.kernel):
            if listOfHerds[r][c].terrainType == "Ground":
                if amountOfErbast < listOfHerds[r][c].lenOfErbast():
                    amountOfErbast = listOfHerds[r][c].lenOfErbast()
                    row, column = listOfHerds[r][c].row, listOfHerds[r][c].column

        return np.array([row, column])

    def findPride(self, listOfPrides):
        self.kernel = self.get_adjacent_cells(self.row, self.column)
        amountOfPride = listOfPrides[self.row][self.column].lenOfCarviz()
        row, column = self.row, self.column
        for i in range(len(self.kernel)):
            if listOfPrides[self.kernel[i][0]][self.kernel[i][1]].terrainType == "Ground":
                if amountOfPride < listOfPrides[self.kernel[i][0]][self.kernel[i][1]].lenOfErbast():
                    amountOfPride = listOfPrides[self.kernel[i][0]][self.kernel[i][1]].lenOfErbast()
                    row = listOfPrides[self.kernel[i][0]][self.kernel[i][1]].row
                    column = listOfPrides[self.kernel[i][0]][self.kernel[i][1]].column
        return np.array([row, column])

    def trackHerd(self, listOfVegetobs):
        self.kernel = self.get_adjacent_cells(self.row, self.column)
        maxDensity = 0
        row, column = self.row, self.column
        for kernel_idx in range(self.kernel.shape[0]):
            kernel_row, kernel_col = self.kernel[kernel_idx]
            if listOfVegetobs[kernel_row][kernel_col].terrainType == "Ground":
                if maxDensity < listOfVegetobs[kernel_row][kernel_col].vegetob.density:
                    maxDensity = listOfVegetobs[kernel_row][kernel_col].vegetob.density
                    row, column = listOfVegetobs[kernel_row][kernel_col].row, listOfVegetobs[kernel_row][
                        kernel_col].column
        return np.array([row, column])

    def move(self, listOfVegetobs, coordinates):
        a = self
        oldRow, oldCol = self.row, self.column
        self.row, self.column = coordinates
        listOfVegetobs[self.row][self.column].appendPride(self)
        listOfVegetobs[oldRow][oldCol].delPride(a)
        self.energy -= 1

    def hunt(self, listOfVegetobs):
        erbSwap = None
        maxEnergy = 0
        for erb in listOfVegetobs[self.row][self.column].erbast:
            if maxEnergy <= erb.energy:
                maxEnergy = erb.energy
                erbSwap = erb
        if erbSwap is not None:
            energy_to_eat = min(100 - self.energy, maxEnergy)
            # Update the energy levels of the creature and plant
            self.energy += energy_to_eat
            listOfVegetobs[self.row][self.column].erbast.remove(erbSwap)


