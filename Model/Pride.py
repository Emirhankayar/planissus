import statistics
import random
import numpy as np
#from _collections import defaultdict # this import is different on different OS
from collections import defaultdict


class Pride(list):
    """
    This class is inherited from a python list and stores an list of Carviz on the same cell.
    """

    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column

    def calculate_social_attitude(self, pride_obj, cellsList):

        """
        This method calculates a social attitude value for each carviz in Pride.
        This value is practically inversely proportional to the population and the energy of a creature.
        High social attitude: low to no amount of Carviz on the same cell + high energy value
        Low social attitude: high amount of Carviz on the same cell (crowding effect) + low energy value

        :param pride_obj:
        :param cellsList:
        :return:
        """

        social_attitudes = [
            (100 - cellsList[carviz.row][carviz.column].lenOfCarviz()) * carviz.energy / 100
            if cellsList[carviz.row][carviz.column].lenOfCarviz() != 100 else carviz.energy / 100
            for carviz in pride_obj
        ]
        return social_attitudes

    def fight_between_prides(self, carviz_list, cellsList):

        """
        Fight between prides is possible due to
        group_carviz_into_prides(), since it splits carviz into the different prides.

        :param carviz_list:
        :param cellsList:
        :return:
        """
        prides = self.group_carviz_into_prides(carviz_list)

        if len(prides) < 2:
            return prides

        # Calculate the median social attitude of each pride
        median_social_attitudes = [statistics.median(self.calculate_social_attitude(pride, cellsList)) for pride in prides]

        # Find the pride with the lowest median social attitude
        lowest_median_social_attitude_index = median_social_attitudes.index(min(median_social_attitudes))
        lowest_median_social_attitude_pride = prides[lowest_median_social_attitude_index]

        # Find the pride with the lowest number of carviz
        num_carviz = [len(pride) for pride in prides]
        smallest_pride_index = num_carviz.index(min(num_carviz))
        smallest_pride = prides[smallest_pride_index]

        # Perform the fight
        winner_index = random.choices(range(len(prides)), k=1)[0]
        loser_index = 1 - winner_index

        # Create a new list excluding the losing pride
        remaining_prides = [pride for i, pride in enumerate(prides) if i != loser_index]

        # Check if the remaining prides decide to join
        if len(remaining_prides) > 1:
            median_social_attitudes = [statistics.median(self.calculate_social_attitude(pride, cellsList)) for pride in remaining_prides]
            # You can adjust this threshold according to your desired condition to join prides
            join_threshold = 10
            if all(median_social_attitude >= join_threshold for median_social_attitude in median_social_attitudes):
                # Join the prides
                joined_pride = Pride(self.row, self.column)  # Use appropriate row and column values
                for pride in remaining_prides:
                    joined_pride.extend(pride)
                remaining_prides = [joined_pride]

        newPride = Pride(self.row, self.column)
        newPride.extend(remaining_prides)
        return newPride

    def averageEnergy(self):
        """
        :return: The average energy of the pride
        """
        total_energy = sum(carv.energy for carv in self)
        return int(total_energy / len(self))

    def prideDecision(self, cellsList):

        """
        This method calls decideMovement method for all of the Carviz creatures in this Pride.
        :param cellsList:
        :return:
        """

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

            if np.array_equal(movementCoords, grazeCoords):
                carv.hasMoved = False
            else:
                carv.move(cellsList, movementCoords)

    def prideMove(self, group, listOfCells, coordinates):
        [carv.move(listOfCells, coordinates) for carv in group if len(group) > 0]

    def groupAging(self):
        """
        An interface to call aging for all prides on the same cell.
        :return:
        """
        for carv in self:
            carv.aging(self)

    def group_carviz_into_prides(self, carviz_list):

        """
        This method groups carviz into different prides based on the
        parameter of where they came from.
        :param carviz_list:
        :return:
        """

        prides_dict = defaultdict(lambda: Pride(0, 0))
        for carviz in carviz_list:
            prides_dict[carviz.previouslyVisited].append(carviz)

        prides = list(prides_dict.values())
        return prides