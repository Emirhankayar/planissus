class SimulationController:
<<<<<<< HEAD
    """
    SimulationController class is only used in FuncAnimation update method
    of the View module, since the simulate method requires an updating cellsList
    """

=======
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d

    def simulate(self, cellsList):
        """
        This methods processes the day on planissus in the following order:
        1. Vegetob grows
        2. If any creatures are surrounded by full density cells of Vegetob, they die
        3. Herds, Prides and individuals make a decision of whether they should eat
        or graze/hunt. They either move, or in latter case, stay at the same spot.
        4. Carviz make a fight or join a pride decision
        5. Erbast graze and Carviz hunt
        6. Erbast and Carviz age

        :param cellsList:
        :return:
        """
        for sublist in cellsList:
            for veg in sublist:
                if veg.terrainType != "Water":
                    veg.vegetob.grow()

        for row in cellsList:
            for cell in row:
                if cell.erbast:
                    cell.death_from_vegetob(cellsList)
                if cell.pride:
                    cell.death_from_vegetob(cellsList)

<<<<<<< HEAD

=======
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
        for row in cellsList:
            for cell in row:
                if cell.erbast:
                    cell.erbast.herdDecision(cellsList)
                if cell.pride:
                    cell.pride.prideDecision(cellsList)


        for row in cellsList:
            for cell in row:
                if cell.pride:
                    cell.pride.fight_between_prides(cell.pride, cellsList)

        for row in cellsList:
            for cell in row:
                if cell.erbast:
                    cell.erbast.herdGraze(cellsList)
                if cell.pride:
                    for cr in cell.pride:
                        if cell.erbast:
                            cr.hunt(cellsList)

        for row in cellsList:
            for cell in row:
                if cell.erbast:
                    cell.erbast.groupAging()
                if cell.pride:
<<<<<<< HEAD
                    cell.pride.groupAging()
=======
                    cell.pride.groupAging()
>>>>>>> b81903c3b19e67e4587139dde4129109c10c279d
