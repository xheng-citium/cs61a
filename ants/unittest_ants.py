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

class test_phase_2(unittest.TestCase):
    def test_Water(self):
        bee = ants.Bee(armor = 1)
        self.assertTrue(bee.watersafe)
        waterplace = ants.Water("bla")
        waterplace.add_insect(bee)
        self.assertTrue(bee.armor == 1)

        harv = ants.HarvesterAnt()
        waterplace = ants.Water("bla")
        waterplace.add_insect(harv)
        self.assertTrue(harv.armor == 0)

    def test_FireAnt(self):
        """Procedure: Create a Place, and put a FireAnt and a Bee inside. When FireAnt is dead, Bee armor is reduced by a certain damage level"""
        place = ants.Place(name = "bla")
        fire = ants.FireAnt(armor=2)
        bee_1 = ants.Bee(armor = 3, place=place)
        
        place.add_insect(fire)
        place.add_insect(bee_1)
        orig_armor_1 = bee_1.armor
        
        fire.reduce_armor(1)
        self.assertEqual(bee_1.armor, orig_armor_1)
                
        fire.reduce_armor(1) # FireAnt is dead
        self.assertEqual(bee_1.armor, orig_armor_1 - fire.damage)
    
    def test_nearest_bee(self):
        """Create a colony and put a ThrowerAnt and several bees in tunnel cells
        Randomness has been verified by running unit test several times"""
        colony = create_colony() 
        thrower_0, thrower_1 = ants.ThrowerAnt(), ants.ThrowerAnt()
        bee_0, bee_1, bee_2, bee_3 = ants.Bee(armor=1), ants.Bee(armor=1), ants.Bee(armor=1), ants.Bee(armor=1)
        for k in colony.places.keys():
            if k == 'Hive': colony.places[k].add_insect(bee_0)
            if k == "tunnel_0_7": colony.places[k].add_insect(thrower_0)
            if k == "tunnel_0_0": colony.places[k].add_insect(thrower_1)
            if k == "tunnel_0_1": 
                colony.places[k].add_insect(bee_1)
                colony.places[k].add_insect(bee_2)
            if k == "tunnel_0_2": colony.places[k].add_insect(bee_3)

        selected = thrower_0.nearest_bee(colony.hive) # Only bee_0 in front of thrower_0 but it is in hive
        self.assertTrue(selected == None)

        selected = thrower_1.nearest_bee(colony.hive)
        self.assertTrue(selected in [bee_1, bee_2]) # selected is either bee_1 or bee_2, but cannot be bee_3
        self.assertFalse(selected == bee_3)

    def test_long_short_thrower(self):
        longthrower = ants.LongThrower()  
        shortthrower = ants.ShortThrower()
        colony = create_colony()   
        bee_0, bee_1 = ants.Bee(armor=1), ants.Bee(armor=1)
        for k in colony.places:
            if k == "tunnel_0_0": colony.places[k].add_insect(longthrower)
            if k == "tunnel_0_1": colony.places[k].add_insect(shortthrower)
            if k == "tunnel_0_2": colony.places[k].add_insect(bee_0)
        self.assertTrue(longthrower.nearest_bee(colony.hive) == None) # bee_0 is too close 
        self.assertEqual(shortthrower.nearest_bee(colony.hive), bee_0)
        
        colony.places["tunnel_0_2"].remove_insect(bee_0)
        colony.places["tunnel_0_4"].add_insect(bee_1)
        self.assertEqual(longthrower.nearest_bee(colony.hive), bee_1)
        self.assertEqual(shortthrower.nearest_bee(colony.hive), None) # bee_1 is too far



##############################################################
def create_colony():
    assault_plan = ants.make_test_assault_plan()
    hive = ants.Hive(assault_plan)
    ant_types = [ants.HarvesterAnt, ants.ThrowerAnt, ants.FireAnt, ants.ShortThrower, ants.LongThrower, 
                 ants.WallAnt, ants.NinjaAnt, ants.ScubaThrower, ants.HungryAnt, ants.BodyguardAnt,
                 ants.QueenAnt, ants.SlowThrower, ants.StunThrower]
    return (ants.AntColony(None, hive, ant_types, ants.test_layout, 1))


if __name__ == "__main__":
    unittest.main()
