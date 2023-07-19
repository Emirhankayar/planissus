import numpy as np


class Herd(list):

    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column

    def averageEnergy(self):
        totalEnergy = sum(erb.energy for erb in self)
        return int(totalEnergy / len(self))

    def herdDecision(self, cellsList):
        population = cellsList[self.row][self.column].lenOfErbast()

        herd_coords = np.array([self.row, self.column])

        for erbast in self:
            populationInvers = 100 - population if population != 100 else 1
            socialAttitude = populationInvers * erbast.energy / 100

            movementCoords = erbast.decideMovement(cellsList, socialAttitude >= 50)

            if np.array_equal(movementCoords, herd_coords):
                erbast.hasMoved = False
            else:
                if np.array_equal(movementCoords, erbast.findHerd(cellsList)):
                    erbast.move(cellsList, movementCoords)
                elif np.array_equal(movementCoords, erbast.findFood(cellsList)):
                    erbast.move(cellsList, movementCoords)
                else:
                    erbast.move(cellsList, movementCoords)

    def herdMove(self, group, listOfCells, coordinates):
        for erb in group:
            erb.move(listOfCells, coordinates)

    def herdGraze(self, listOfCells):
        startvingErbasts = []
        for erb_idx, erb in enumerate(self):
            if erb.energy <= 40 and not erb.hasMoved:
                startvingErbasts.append(erb_idx)

        population = listOfCells[self.row][self.column].lenOfErbast()
        vegetob_density = listOfCells[self.row][self.column].vegetob.density

        if len(startvingErbasts) >= 1:
            energyToEat = vegetob_density / len(startvingErbasts)
        else:
            energyToEat = vegetob_density / population

        erbasts_in_cell = listOfCells[self.row][self.column].erbast

        if len(startvingErbasts) < vegetob_density:
            for erb_idx in startvingErbasts:
                if erb_idx < len(erbasts_in_cell):
                    erbasts_in_cell[erb_idx].graze(listOfCells, energyToEat)

        elif len(startvingErbasts) > vegetob_density:
            for erb_idx in range(vegetob_density):
                if erb_idx < len(erbasts_in_cell):
                    erbasts_in_cell[erb_idx].graze(listOfCells, energyToEat)
        else:
            for erb in self:
                erb.graze(listOfCells, energyToEat)

    def groupAging(self):
        [erb.aging(self) for erb in self]