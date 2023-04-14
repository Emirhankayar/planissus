import numpy as np

from Model.Creatures import Erbast, Vegetob, Carviz


class Cell:
    def __init__(self, row, column, terrainType, vegetob):
        self.row = row
        self.column = column
        self.terrainType = terrainType
        self.vegetob = vegetob
        self.erbast = Herd(row, column)
        self.pride = Pride(row, column)

    def lenOfErbast(self):
        amountOfErbast = len(self.erbast)
        return amountOfErbast

    def appendErbast(self, erb):
        self.erbast.append(erb)

    def delErbast(self, erb):
        self.erbast.remove(erb)

    def lenOfCarviz(self):
        amountOfCarviz = len(self.pride)
        return amountOfCarviz

    def appendPride(self, pride):
        self.pride.append(pride)

    def delPride(self, pride):
        self.pride.remove(pride)

    def genVegetob(self):
        if self.terrainType == "Ground":
            return Vegetob()
        else:
            return None

    def __str__(self):
        if self.terrainType == "Ground":
            return f"({self.row}, {self.column}, {self.terrainType}, {self.vegetob.density}, {self.erbast}, {self.pride})"
        else:
            return f"({self.row}, {self.column}, {self.terrainType}, {self.vegetob}, {self.erbast}, {self.pride})"

    def __repr__(self):
        return self.__str__()


class Herd(list):

    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column

    # evaluates movement or stay based on four parameters
    # 1. Is it alone or in a herd?
    # 2. Is carviz on the same cell?
    # 3. Does the cell has vegetob?
    # 4. What is the average energy?

    def averageEnergy(self):
        cumulativeEnergy = 0
        for erb in self:
            cumulativeEnergy += erb.energy
        return int(cumulativeEnergy / len(self))

    def herdDecision(self, cellsList):

        individual = self[0]

        foodGroup = []
        foodCoords = individual.findFood(cellsList)

        grazeGroup = []
        grazeCoords = np.array([self.row, self.column])

        findHerdGroup = []
        herdCoords = individual.findHerd(cellsList)

        for erbast in self:
            soc_value = np.random.randint(0, 100)

            if len(cellsList[self.row][self.column].pride) > 0:
                if erbast.energy >= 50 and soc_value > 50:
                    erbast.hasMoved = True
                    findHerdGroup.append(erbast)
                elif self.averageEnergy() < 50 and soc_value > 20:
                    erbast.hasMoved = True
                    foodGroup.append(erbast)
            else:
                if cellsList[self.row][self.column].vegetob.density > 60 and soc_value > 10:
                    erbast.hasMoved = False
                    grazeCoords = np.array([self.row, self.column])
                    grazeGroup.append(erbast)
                elif soc_value > 40:
                    erbast.hasMoved = True
                    foodGroup.append(erbast)

        if len(grazeGroup) > 0:
            self.herdMove(group=grazeGroup, listOfCells=cellsList, coordinates=grazeCoords)
        if len(findHerdGroup) > 0:
            self.herdMove(group=findHerdGroup, listOfCells=cellsList, coordinates=herdCoords)
        if len(foodGroup) > 0:
            self.herdMove(group=foodGroup, listOfCells=cellsList, coordinates=foodCoords)

    def herdMove(self, group, listOfCells, coordinates):
        if len(group) > 0:
            for erb in group:
                erb.move(listOfCells, coordinates)

    # TODO: decrease @soc_attitude
    def herdGraze(self, listOfCells):
        lowestEnergy = 0
        er = Erbast()
        for erb in self:
            if lowestEnergy <= erb.energy:
                er = erb
        er.graze(listOfCells)

    def groupAging(self):
        for erbast in self:
            erbast.aging(self)


class Pride(list):

    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column
        self.previous_coordinates = np.array([self.row, self.column])

    def appendCarviz(self, carv):
        self.append(carv)

    def delCarviz(self, carv):
        self.remove(carv)

    def averageEnergy(self):
        cumulativeEnergy = 0
        for carv in self:
            cumulativeEnergy += carv.energy
        return int(cumulativeEnergy / len(self))

    def prideDecision(self, cellsList):

        indiv = self[0]

        prideGroup = Pride(row=self.row, column=self.column)
        prideCoords = indiv.findPride(cellsList)

        huntGroup = Pride(row=self.row, column=self.column)
        huntCoords = np.array([self.row, self.column])

        findHerdGroup = Pride(row=self.row, column=self.column)
        herdCoords = indiv.findHerd(cellsList)

        trackHerdGroup = Pride(row=self.row, column=self.column)
        trackHerdCoords = indiv.trackHerd(cellsList)

        for carv in self:
            soc_value = np.random.randint(0, 100)
            if len(cellsList[self.row][self.column].erbast) > 0:
                if carv.energy <= 20 and soc_value > 30:
                    carv.hasMoved = False
                    huntGroup.append(carv)
            else:
                if carv.energy >= 40:
                    carv.hasMoved = True
                    if (herdCoords[0] == self.row and herdCoords[1] == self.column) or (
                            soc_value < 20 and carv.energy >= 40):
                        trackHerdGroup.append(carv)
                        self.remove(carv)
                    else:
                        findHerdGroup.append(carv)
                        self.remove(carv)
                elif soc_value > 80:
                    prideGroup.append(carv)
                    self.remove(carv)

        if len(prideGroup) > 0:
            print("decision to FIND PRIDE")
            self.prideMove(group=prideGroup, listOfCells=cellsList, coordinates=prideCoords)
        if len(huntGroup) > 0:
            print("decision to HUNT")
            self.prideMove(group=huntGroup, listOfCells=cellsList, coordinates=huntCoords)
        if len(findHerdGroup) > 0:
            print("decision to FIND HERD")
            self.prideMove(group=findHerdGroup, listOfCells=cellsList, coordinates=herdCoords)
        if len(trackHerdGroup) > 0:
            print("decision to TRACK HERD")
            self.prideMove(group=trackHerdGroup, listOfCells=cellsList, coordinates=trackHerdCoords)

    def prideMove(self, group, listOfCells, coordinates):
        self.previous_coordinates = np.array([self.row, self.column])
        if len(group) > 0:
            group.row = coordinates[0]
            group.column = coordinates[1]
            for carv in group:
                carv.row = group.row
                carv.column = group.column
            listOfCells[group.row][group.column].appendPride(group)

    # def struggle(self, cellsList):

    def prideHunt(self, listOfCells):
        if len(listOfCells[self.row][self.column].erbast) > 0:
            lowestEnergy = 0
            carvSwap = None
            for carv in self:
                if lowestEnergy <= carv.energy:
                    lowestEnergy = carv.energy
                    carvSwap = carv
            carvSwap.hunt(listOfCells)

    def groupAging(self):
        for group in self:
            for cr in group:
                cr.aging(group)

    def struggle(self, cellsList):

        prides = cellsList[self.row][self.column]

        cumulative_energy = 0
        carv_counter = 0

        energies_list = []

        for carv in self:
            cumulative_energy += carv.energy
            carv_counter += 1
        average_energy = int(cumulative_energy / carv_counter)
        energies_list.append(average_energy)

        for i in range(len(self) - 1):
            if energies_list[self[i]] > energies_list[self[i + 1]]:
                self.remove(self[i + 1])
            else:
                self.remove(self[i])
