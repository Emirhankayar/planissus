import numpy as np


class Herd(list):
<<<<<<< HEAD
    """
    This class is inherited from a python list and stores an list of Erbast on the same cell.
    """
=======
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d

    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column

<<<<<<< HEAD
    def herdDecision(self, cellsList):

        """
        This method calculates a social attitude value for each erbast in herd.
        This value is practically inversely proportional to the population and the energy of a creature.
        High social attitude: low to no amount of Erbast on the same cell + high energy value
        Low social attitude: high amount of Erbast on the same cell (crowding effect) + low energy value
        Then, this method calls decideMovement method for all of the Erbast creatures in this Herd.
        :param cellsList:
        :return:
        """

=======
    def averageEnergy(self):
        totalEnergy = sum(erb.energy for erb in self)
        return int(totalEnergy / len(self))

    def herdDecision(self, cellsList):
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
        population = cellsList[self.row][self.column].lenOfErbast()

        herd_coords = np.array([self.row, self.column])

        for erbast in self:
            populationInvers = 100 - population if population != 100 else 1
            socialAttitude = populationInvers * erbast.energy / 100

            movementCoords = erbast.decideMovement(cellsList, socialAttitude >= 50)

            if np.array_equal(movementCoords, herd_coords):
                erbast.hasMoved = False
            else:
<<<<<<< HEAD
                erbast.move(cellsList, movementCoords)


    def herdGraze(self, listOfCells):

        """
        Finds the erbast with least energy values and let them graze on Vegetob.
        Also is adjusted for situations, where there is an abundance or deficit of vegetob.
        :param listOfCells:
        :return:
        """

=======
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
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
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
<<<<<<< HEAD
        """
        An interface to call aging for all erbasts on the same cell.
        :return:
        """
        [erb.aging(self) for erb in self]
=======
        [erb.aging(self) for erb in self]
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
