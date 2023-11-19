<<<<<<< HEAD
import statistics
import random
import numpy as np
#from _collections import defaultdict # this import is different on different OS
from collections import defaultdict


class Pride(list):
    """
    This class is inherited from a python list and stores an list of Carviz on the same cell.
    """
=======
import sys
sys.path.append(".")
import statistics
import random
import numpy as np
from collections import defaultdict



class Pride(list):
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d

    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column

    def calculate_social_attitude(self, pride_obj, cellsList):
<<<<<<< HEAD

        """
        This method calculates a social attitude value for each carviz in Pride.
        This value is practically inversely proportional to the population and the energy of a creature.
        High social attitude: low to no amount of Carviz on the same cell + high energy value
        Low social attitude: high amount of Carviz on the same cell (crowding effect) + low energy value

        :param pride_obj:
        :param cellsList:
        :return:
        """

=======
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
        social_attitudes = [
            (100 - cellsList[carviz.row][carviz.column].lenOfCarviz()) * carviz.energy / 100
            if cellsList[carviz.row][carviz.column].lenOfCarviz() != 100 else carviz.energy / 100
            for carviz in pride_obj
        ]
        return social_attitudes

    def fight_between_prides(self, carviz_list, cellsList):
<<<<<<< HEAD

        """
        Fight between prides is possible due to
        group_carviz_into_prides(), since it splits carviz into the different prides.

        :param carviz_list:
        :param cellsList:
        :return:
        """
=======
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
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
<<<<<<< HEAD
                joined_pride = Pride(self.row, self.column)  # Use appropriate row and column values
=======
                joined_pride = Pride(0, 0)  # Use appropriate row and column values
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
                for pride in remaining_prides:
                    joined_pride.extend(pride)
                remaining_prides = [joined_pride]

        newPride = Pride(self.row, self.column)
        newPride.extend(remaining_prides)
        return newPride

    def averageEnergy(self):
<<<<<<< HEAD
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

=======
        total_energy = sum(erb.energy for erb in self)
        return int(total_energy / len(self))

    def prideDecision(self, cellsList):
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
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
<<<<<<< HEAD
                carv.move(cellsList, movementCoords)

    def prideMove(self, group, listOfCells, coordinates):
        [carv.move(listOfCells, coordinates) for carv in group if len(group) > 0]

    def groupAging(self):
        """
        An interface to call aging for all prides on the same cell.
        :return:
        """
=======
                herdCoords = carv.findHerd(cellsList)
                trackCoords = carv.trackHerd(cellsList)

                if np.array_equal(movementCoords, herdCoords):
                    carv.move(cellsList, movementCoords)
                elif np.array_equal(movementCoords, trackCoords):
                    carv.move(cellsList, movementCoords)
                else:
                    carv.move(cellsList, movementCoords)

    def prideMove(self, group, listOfCells, coordinates):
        [erb.move(listOfCells, coordinates) for erb in group if len(group) > 0]


    def groupAging(self):
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
        for carv in self:
            carv.aging(self)

    def group_carviz_into_prides(self, carviz_list):
<<<<<<< HEAD

        """
        This method groups carviz into different prides based on the
        parameter of where they came from.
        :param carviz_list:
        :return:
        """

=======
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
        prides_dict = defaultdict(lambda: Pride(0, 0))
        for carviz in carviz_list:
            prides_dict[carviz.previouslyVisited].append(carviz)

        prides = list(prides_dict.values())
        return prides