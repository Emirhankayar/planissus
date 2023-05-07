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

        randomStayGroup = []
        rnd = np.random.randint(0, len(individual.kernel)-1)
        randomCoords = np.array([individual.kernel[rnd][0], individual.kernel[rnd][0]])

        for erbast in self:
            soc_value = np.random.randint(0, 100)

            if erbast.energy >= 50:
                if cellsList[erbast.row][erbast.column].vegetob.density >= 60:
                    erbast.hasMoved = False
                    grazeGroup.append(erbast)
                else:
                    erbast.hasMoved = True
                    randomStayGroup.append(erbast)
            else:
                if cellsList[erbast.row][erbast.column].vegetob.density >= 30:
                    erbast.hasMoved = False
                    grazeGroup.append(erbast)
                else:
                    erbast.hasMoved = True
                    foodGroup.append(erbast)



        if len(findHerdGroup) > 0:
            self.herdMove(group=findHerdGroup, listOfCells=cellsList, coordinates=herdCoords)
        if len(foodGroup) > 0:
            self.herdMove(group=foodGroup, listOfCells=cellsList, coordinates=foodCoords)
        if len(randomStayGroup) > 0:
            self.herdMove(group=randomStayGroup, listOfCells=cellsList, coordinates=randomCoords)


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

    def prideDecision(self, cellsList):

        individual = self[0]

        findHerdGroup = []
        herdCoords = individual.findHerd(cellsList)
        print("herd coords", herdCoords)

        randomStayGroup = []
        rnd = np.random.randint(0, len(individual.kernel) - 1)
        randomCoords = np.array([individual.kernel[rnd][0], individual.kernel[rnd][0]])

        for carv in self:
            soc_value = np.random.randint(0, 100)

            if len(cellsList[carv.row][carv.column].erbast) > 0:
                carv.hasMoved = False
            else:
                if herdCoords[0] != carv.row and herdCoords[1] != carv.column and soc_value > 50:
                    carv.hasMoved = True
                    findHerdGroup.append(carv)
                else:
                    randomStayGroup.append(carv)

        print(self.row, self.column, "CURRENT")
        print(randomCoords, "random coords")
        print(herdCoords, "herd coords")
        print("--------------------------------------------")

        if len(findHerdGroup) > 0:
            self.prideMove(group=findHerdGroup, listOfCells=cellsList, coordinates=herdCoords)
        if len(randomStayGroup) > 0:
            self.prideMove(group=randomStayGroup, listOfCells=cellsList, coordinates=randomCoords)

    def prideMove(self, group, listOfCells, coordinates):
        if len(group) > 0:
            for erb in group:
                erb.move(listOfCells, coordinates)

    # TODO: adjust
    def prideGraze(self, listOfCells):
        a = None
        lowestEnergy = 0
        for erb in self:
            if lowestEnergy <= erb.energy:
                a = erb
        a.hunt(listOfCells)

    def groupAging(self):
        for carv in self:
            carv.aging(self)

