import numpy as np
from collections import defaultdict

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
            return "Water"

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

        foodGroup = []
        findHerdGroup = []
        randomMovementGroup = []

        population = cellsList[self.row][self.column].lenOfErbast()
        movementCoords = np.array([self.row, self.column])

        print(population, "population")
        for erbast in self:

            if population == 100:
                populationInvers = 1
            else:
                populationInvers = 100 - population
            socialAttitude = populationInvers * erbast.energy / 100

            movementCoords = erbast.decideMovement(cellsList, socialAttitude >= 50)

            grazeCoords = np.array([self.row, self.column])

            if movementCoords[0] == grazeCoords[0] and movementCoords[1] == grazeCoords[1]:
                erbast.hasMoved = False
            else:
                if movementCoords[0] == erbast.findHerd(cellsList)[0] and movementCoords[1] == \
                        erbast.findHerd(cellsList)[1]:
                    erbast.move(cellsList, movementCoords)
                elif movementCoords[0] == erbast.findFood(cellsList)[0] and movementCoords[1] == \
                        erbast.findFood(cellsList)[1]:
                    erbast.move(cellsList, movementCoords)
                else:
                    erbast.move(cellsList, movementCoords)



    def herdMove(self, group, listOfCells, coordinates):
        if len(group) > 0:
            for erb in group:
                erb.move(listOfCells, coordinates)

    # TODO: decrease @soc_attitude
    def herdGraze(self, listOfCells):

        startvingErbasts = []
        i = 0
        for erb in self:
            if erb.energy <= 40 and not erb.hasMoved:
                startvingErbasts.append(i)
            i += 1

        energyToEat = 0
        population = listOfCells[self.row][self.column].lenOfErbast()

        if len(startvingErbasts) >= 1:
            energyToEat = listOfCells[self.row][self.column].vegetob.density / len(startvingErbasts)

        else:
            energyToEat = listOfCells[self.row][self.column].vegetob.density / population

        if len(startvingErbasts) < listOfCells[self.row][self.column].vegetob.density:
            for erb in range(len(startvingErbasts)):
                listOfCells[self.row][self.column].erbast[erb].graze(listOfCells, energyToEat)

        elif len(startvingErbasts) > listOfCells[self.row][self.column].vegetob.density:
            for erb in range(int(listOfCells[self.row][self.column].vegetob.density)):
                listOfCells[self.row][self.column].erbast[erb].graze(listOfCells, energyToEat)
        else:
            for erb in self:
                erb.graze(listOfCells, energyToEat)

    def groupAging(self):
        for erbast in self:
            erbast.aging(self)


class Pride(list):

    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column

    def calculate_social_attitude(self, pride_obj, cellsList):
        social_attitudes = []
        for carviz in pride_obj:
            population = cellsList[carviz.row][carviz.column].lenOfCarviz()
            population_invers = 100 - population if population != 100 else 1
            social_attitude = population_invers * carviz.energy / 100
            social_attitudes.append(social_attitude)
        return social_attitudes

    def fight_between_prides(self, carviz_list, cellsList):

        prides = self.group_carviz_into_prides(carviz_list)

        if len(prides) < 2:
            return prides
        # The rest of the fight_between_prides function remains the same.

        # Calculate the median social attitude of each pride
        median_social_attitudes = [np.median(self.calculate_social_attitude(pride, cellsList)) for pride in prides]

        # Find the pride with the lowest median social attitude
        lowest_median_social_attitude_index = np.argmin(median_social_attitudes)
        lowest_median_social_attitude_pride = prides[lowest_median_social_attitude_index]

        # Find the pride with the lowest number of carviz
        num_carviz = [len(pride) for pride in prides]
        smallest_pride_index = np.argmin(num_carviz)
        smallest_pride = prides[smallest_pride_index]

        # Calculate the winning probabilities based on the energy of their components
        energy_prides = [sum(carviz.energy for carviz in pride) for pride in prides]
        winning_probabilities = [energy / sum(energy_prides) for energy in energy_prides]

        # Perform the fight
        winner_index = np.random.choice(len(prides), p=winning_probabilities)
        loser_index = 1 - winner_index
        # Remove the losing pride
        prides.pop(loser_index)

        # Check if the remaining prides decide to join
        remaining_prides = len(prides)
        if remaining_prides > 1:
            median_social_attitudes = [np.median(self.calculate_social_attitude(pride, cellsList)) for pride in prides]
            # You can adjust this threshold according to your desired condition to join prides
            join_threshold = 10
            if all(median_social_attitude >= join_threshold for median_social_attitude in median_social_attitudes):
                # Join the prides
                joined_pride = Pride(0, 0)  # Use appropriate row and column values
                for pride in prides:
                    joined_pride.extend(pride)
                prides = [joined_pride]
        newPride = Pride(self.row, self.column)
        newPride.append(prides)
        return newPride

    def averageEnergy(self):
        cumulativeEnergy = 0
        for erb in self:
            cumulativeEnergy += erb.energy
        return int(cumulativeEnergy / len(self))

    def prideDecision(self, cellsList):

        foodGroup = []
        findHerdGroup = []
        randomMovementGroup = []

        population = cellsList[self.row][self.column].lenOfErbast()
        movementCoords = np.array([self.row, self.column])


        for carv in self:

            if population == 100:
                populationInvers = 1
            else:
                populationInvers = 100 - population
            socialAttitude = populationInvers * carv.energy / 100

            movementCoords = carv.decideMovement(cellsList, socialAttitude >= 50)

            grazeCoords = np.array([self.row, self.column])

            if movementCoords[0] == grazeCoords[0] and movementCoords[1] == grazeCoords[1]:
                carv.hasMoved = False
            else:
                if movementCoords[0] == carv.findHerd(cellsList)[0] and movementCoords[1] == \
                        carv.findHerd(cellsList)[1]:
                    carv.move(cellsList, movementCoords)
                elif movementCoords[0] == carv.trackHerd(cellsList)[0] and movementCoords[1] == \
                        carv.trackHerd(cellsList)[1]:
                    carv.move(cellsList, movementCoords)
                else:
                    carv.move(cellsList, movementCoords)



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

    def group_carviz_into_prides(self, carviz_list):
        prides_dict = {}
        for carviz in carviz_list:
            if carviz.previouslyVisited not in prides_dict:
                prides_dict[carviz.previouslyVisited] = Pride(carviz.row, carviz.column)
            prides_dict[carviz.previouslyVisited].append(carviz)

        prides = list(prides_dict.values())
        return prides
