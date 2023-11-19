<<<<<<< HEAD
=======
import sys
sys.path.append(".")
from Model.Creatures import Vegetob
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
from Model.Herd import Herd
from Model.Pride import Pride


class Cell:
<<<<<<< HEAD

    """
    class Cell is a base unit of the world in Planissus world simulation.
    It stores a row and a column, in order to allow for an easier navigation.
    It's terrainType affects whether a cell can have erbast or not.
    (If the cell terrainType is "Water" or "Ground")
    """

    def __init__(self, row, column, terrainType, vegetob):
        """

        :param row:
        :param column:
        :param terrainType:
        :param vegetob:
        """
=======
    def __init__(self, row, column, terrainType, vegetob):
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
        self.row = row
        self.column = column
        self.terrainType = terrainType
        self.vegetob = vegetob
        self.erbast = Herd(row, column)
        self.pride = Pride(row, column)

    def lenOfErbast(self):
<<<<<<< HEAD
        """
        :return: amount of all erbast on this cell
        """
        amountOfErbast = len(self.erbast)
        return amountOfErbast

    def delErbast(self, erb):
        """
        removes a specific erbast from the cell
        :param erb:
        :return:
        """
        self.erbast.remove(erb)

    def lenOfCarviz(self):
        """
        :return: amount of all Carviz on this cell
        """
=======
        amountOfErbast = len(self.erbast)
        return amountOfErbast

    def appendErbast(self, erb):
        self.erbast.append(erb)

    def delErbast(self, erb):
        self.erbast.remove(erb)

    def lenOfCarviz(self):
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
        amountOfCarviz = len(self.pride)
        return amountOfCarviz

    def appendPride(self, pride):
<<<<<<< HEAD
        """
        Appends a list of Carviz to the cell
        :param pride:
        :return:
        """
        self.pride.append(pride)

    def delPride(self, pride):
        """
        Deletes a pride from the current cell
        :param pride:
        :return:
        """
        self.pride.remove(pride)


    def death_from_vegetob(self, listOfVegetobs):

        """
        Kills all creatures which are surrounded by full density vegetobs
        Since there can be at most 8 neighbouring cells, method loops through each of them
        and check for two factors:
        1. if the cell contains any Vegetob at all and if so,
        2. if its density is equal to 100.

        If the amount of neighbouring cells matches the number of cells with maximum Vegetob value (vegetob_full_density_counter),
        clear a list of creatures on that cell.

        :param listOfVegetobs: neede to get the amount of surrounding cells with maximum vegetob density
        :return:
        """

=======
        self.pride.append(pride)

    def delPride(self, pride):
        self.pride.remove(pride)

    def genVegetob(self):
        if self.terrainType == "Ground":
            return Vegetob()
        else:
            return "Water"

    def death_from_vegetob(self, listOfVegetobs):

>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
        vegetob_full_density_counter = 0

        if self.erbast:
            erb = self.erbast[0]
            kernel = erb.get_adjacent_cells(self.row, self.column)
            if len(kernel) == 8:

                for i in range(len(kernel)):
                    if listOfVegetobs[kernel[i][0]][kernel[i][1]].vegetob:
                        if listOfVegetobs[kernel[i][0]][kernel[i][1]].vegetob.density == 100:
                            vegetob_full_density_counter += 1

                if vegetob_full_density_counter == 8:
                    if self.erbast:
                        self.erbast.clear()

                vegetob_full_density_counter = 0

        if self.pride:
            carv = self.pride[0]
            kernel = carv.get_adjacent_cells(self.row, self.column)

            if len(kernel) == 8:

                for i in range(len(kernel)):
                    if listOfVegetobs[kernel[i][0]][kernel[i][1]].vegetob:
                        if listOfVegetobs[kernel[i][0]][kernel[i][1]].vegetob.density == 100:
                            vegetob_full_density_counter += 1

                if vegetob_full_density_counter == 8:
                    if self.pride:
                        self.pride.clear()

    def __str__(self):
        if self.terrainType == "Ground":
            return f"({self.row}, {self.column}, {self.terrainType}, {self.vegetob.density}, {self.erbast}, {self.pride})"
<<<<<<< HEAD

        return f"({self.row}, {self.column}, {self.terrainType}, {self.vegetob}, erbast: {self.erbast}, carviz: {self.pride})"
=======
        else:
            return f"({self.row}, {self.column}, {self.terrainType}, {self.vegetob}, erbast: {self.erbast}, carviz: {self.pride})"
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d

    def __repr__(self):
        return self.__str__()