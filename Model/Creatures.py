import random
import numpy as np

class Creatures():
    NUM_CELLS = None

    def __init__(self):
        self._row = 0
        self._column = 0
        self.kernel = np.empty((0, 0), dtype=object)

    @classmethod
    def update_num_cells(cls, num_cells):
        cls.NUM_CELLS = num_cells

    def get_adjacent_cells(self, row, col):
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
        self._density = int(newDensity)

    def generateDensity(self):
        return np.random.randint(1, 100)

    def grow(self):
        if self.density < 100:
            self.density += 1


class Erbast(Creatures):
    def __init__(self, lifetime=10):
        super().__init__()
        self._energy = np.random.randint(35, 95)
        self.lifetime = lifetime
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
        energyOfOffsprings = self.energy // 2  # Use floor division for integer result
        erb1 = Erbast()
        erb1.energy = energyOfOffsprings
        erb1.row, erb1.column = self.row, self.column
        erb2 = Erbast()
        erb2.energy = energyOfOffsprings
        erb2.row, erb2.column = self.row, self.column
        listOfCreatures.extend([erb1, erb2])


    def findHerd(self, listOfHerds):
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

    def changeSocAttitude(self):
        if self.energy >= 20 or self.energy >= 80:
            self.soc_attitude = 0
        else:
            self.soc_attitude = 1

    def move(self, listOfVegetobs, coordinates):
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
        
        self.changeSocAttitude()

class Carviz(Creatures):

    def __init__(self, lifetime=10):
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
        energyOfOffsprings = self.energy // 2  # Use floor division for integer result

        carv1 = Carviz()
        carv1.energy = energyOfOffsprings
        carv1.row, carv1.column = self.row, self.column

        carv2 = Carviz()
        carv2.energy = energyOfOffsprings
        carv2.row, carv2.column = carv1.row, carv1.column  # Assign row and column from carv1

        listOfCreatures.extend([carv1, carv2])

    def findHerd(self, listOfHerds):
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

    def trackHerd(self, listOfVegetobs):
        def density_key(idx):
            if listOfVegetobs[idx[0]][idx[1]].terrainType == "Ground":
                return listOfVegetobs[idx[0]][idx[1]].vegetob.density
            else:
                return -1

        self.kernel = self.get_adjacent_cells(self.row, self.column)
        row, column = max(self.kernel, key=density_key)
        return np.array([row, column])


    def move(self, listOfVegetobs, coordinates):
        oldRow, oldCol = self.row, self.column
        self.previous_position = (oldRow, oldCol)  # Save the previous position
        self.row, self.column = coordinates

        newCell = listOfVegetobs[self.row][self.column]
        newCell.appendPride(self)
        listOfVegetobs[oldRow][oldCol].delPride(self)

        self.energy -= 1



    def hunt(self, listOfVegetobs):
        erbast = listOfVegetobs[self.row][self.column].erbast
        erbSwap = max(erbast, key=lambda erb: erb.energy, default=None)
        
        if erbSwap is not None:
            maxEnergy = erbSwap.energy
            energy_to_eat = min(100 - self.energy, maxEnergy)
            
            # Update the energy levels of the creature and plant
            self.energy += energy_to_eat
            erbast.remove(erbSwap)

    def decideMovement(self, listOfPride, isSocAttitudeHigh):
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

