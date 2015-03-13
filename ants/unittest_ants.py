#!/usr/bin/python3

import unittest
import pdb
import ants

class test_phase_1(unittest.TestCase):
    def test_Harvester_and_Thrower(self):
        harv = ants.HarvesterAnt()
        self.assertEqual(harv.food_cost, 2)
        self.assertEqual(harv.armor, 1)

        assault_plan = ants.make_test_assault_plan()
        hive = ants.Hive(assault_plan)
        colony = ants.AntColony(None, hive,[ants.HarvesterAnt], ants.test_layout, 1)
        curr_food = colony.food
        harv.action(colony)
        self.assertEqual(colony.food, curr_food + 1 ) # Harvester add colony food by 1

        thrower = ants.ThrowerAnt()
        self.assertEqual(thrower.food_cost, 4)

    def test_Place(self):
        p_1 = ants.Place(name = "1")
        self.assertTrue(p_1.entrance is None)
        self.assertTrue(p_1.exit is None)

        p_2 = ants.Place(name = "2", exit = p_1)
        self.assertTrue(p_2.entrance is None)
        self.assertTrue(p_2.exit.entrance is not None)
        
        # test add_insect
        # test remove_insect





if __name__ == "__main__":
    unittest.main()