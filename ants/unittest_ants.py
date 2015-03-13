#!/usr/bin/python3

import argparse
import unittest
import pdb
import ants

class test_phase_1(unittest.TestCase):
    def test_Harvester_and_Thrower(self):
        harv = ants.HarvesterAnt()
        self.assertEqual(harv.food_cost, 2)
        self.assertEqual(harv.armor, 1)
       
        colony = create_colony()
        orig_food = colony.food
        harv.action(colony)
        self.assertEqual(colony.food, orig_food + 1 ) # Harvester add colony food by 1

        thrower = ants.ThrowerAnt()
        self.assertEqual(thrower.food_cost, 4) # testing action() is more meaningful later with LongThrower and ShortThrower
        # nearest_bee() is tested in phase 2

    def test_Place(self):
        p_1 = ants.Place(name = "1")
        self.assertTrue(p_1.entrance is None)
        self.assertTrue(p_1.exit is None)

        p_2 = ants.Place(name = "2", exit = p_1) # connecting 2 Place objects
        self.assertTrue(p_2.entrance is None)
        self.assertTrue(p_2.exit.entrance is not None)
        
        # test add_insect, remove_insect are in later phases with an BodyguardAnt

class test_phase_2(unittest.TestCase):
    def test_Water(self):
        bee = ants.Bee(armor = 1)
        self.assertTrue(bee.watersafe)
        waterplace = ants.Water("A")
        waterplace.add_insect(bee)
        self.assertTrue(bee.armor == 1)

        harv = ants.HarvesterAnt()
        waterplace = ants.Water("A")
        waterplace.add_insect(harv)
        self.assertTrue(harv.armor == 0)

    def test_FireAnt(self):
        """Procedure: Create a Place, and put a FireAnt and a Bee inside. When FireAnt is dead, Bee armor is reduced by a certain damage level"""
        place = ants.Place(name = "A")
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
        Randomness has been verified by running unit test several times
        Note:
          I use colony.places["tunnel_0_0"].add_insect(thrower_0) to add a ThrowerAnt
          There seems an equivalent way: colony.deploy_ant('tunnel_0_0', 'Thrower')"""
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
            if k == "tunnel_0_3": colony.places[k].add_insect(bee_0)
        self.assertTrue(longthrower.nearest_bee(colony.hive) == None) # bee_0 is too close 
        self.assertEqual(shortthrower.nearest_bee(colony.hive), bee_0)
        
        colony.places["tunnel_0_3"].remove_insect(bee_0)
        colony.places["tunnel_0_4"].add_insect(bee_1)
        self.assertEqual(longthrower.nearest_bee(colony.hive), bee_1)
        self.assertEqual(shortthrower.nearest_bee(colony.hive), None) # bee_1 is too far

class test_phase_3(unittest.TestCase):
    def test_WallAnt(self):
        wall = ants.WallAnt()
        self.assertEqual(wall.armor, 4)
        self.assertEqual(wall.food_cost, 4)

        colony = create_colony()
        bee = ants.Bee(armor=1)
        colony.places["tunnel_0_3"].add_insect(wall)
        colony.places["tunnel_0_3"].add_insect(bee)
        ctr = 0
        while ctr < 4+1: # 4+1 b/c it takes 4 stings to kill WallAnt amd 1 action to move bee to next place
            bee.action(colony)
            ctr += 1
        self.assertEqual(wall.armor, 0)
        self.assertEqual(bee.place.name, "tunnel_0_2")

    def test_NinjaAnt(self):
        ninja = ants.NinjaAnt()
        self.assertEqual(ninja.food_cost, 6)        
        
        colony = create_colony()
        bee_0 = ants.Bee(armor=1)
        thrower = ants.ThrowerAnt()
        colony.places["tunnel_0_7"].add_insect(thrower)
        colony.places["tunnel_0_7"].add_insect(bee_0)
        self.assertTrue(bee_0.blocked())

        bee_1 = ants.Bee(armor=1)
        colony.places["tunnel_0_2"].add_insect(ninja)
        colony.places["tunnel_0_2"].add_insect(bee_1)
        self.assertFalse(bee_1.blocked())

        orig_armor_0, orig_armor_1 = bee_0.armor, bee_1.armor
        ninja.action(colony)
        self.assertEqual(bee_0.armor, orig_armor_0)
        self.assertEqual(bee_1.armor, orig_armor_1 - ninja.damage) # Colocated bee is damaged
   
    def test_Scuba(self):
        scuba = ants.ScubaThrower()
        self.assertTrue(scuba.watersafe)
        waterplace = ants.Water("A")
        orig_armor = scuba.armor
        waterplace.add_insect(scuba)
        self.assertTrue(scuba.armor == orig_armor)

    def test_Hungry(self):
        hungry = ants.HungryAnt()
        bee_0, bee_1 = ants.Bee(armor=1), ants.Bee(armor=1)
        colony = create_colony()
        colony.places["tunnel_0_1"].add_insect(hungry)
        colony.places["tunnel_0_1"].add_insect(bee_0)
        hungry.action(colony)
        self.assertTrue(bee_0.armor <= 0)
        self.assertEqual(hungry.digesting, ants.HungryAnt.time_to_digest)
        
        orig_digesting = hungry.digesting
        colony.places["tunnel_0_1"].add_insect(bee_1) # Add another bee
        orig_armor_1 = bee_1.armor
        counter = 0
        while counter <= orig_digesting:
            hungry.action(colony)
            if counter < orig_digesting:
                self.assertEqual(bee_1.armor, orig_armor_1) # bee_1 armor should not reduce
            if counter == orig_digesting:
                self.assertEqual(bee_1.armor, 0) 
            counter += 1
        
class test_phase_4(unittest.TestCase):
    def test_Bodyguard(self):
        body = ants.BodyguardAnt()
        thrower, thrower_1 = ants.ThrowerAnt(), ants.ThrowerAnt()
        self.assertEqual(body.armor, 2)
        self.assertTrue(body.container)
        self.assertTrue(body.can_contain(thrower))
        self.assertFalse(body.can_contain(ants.BodyguardAnt())) # cannot contain another BodyguardAnt
        self.assertFalse(thrower.container)
        self.assertFalse(thrower.can_contain(body))
        self.assertFalse(thrower.can_contain(thrower_1))
        
        # Insert Bodyguard first
        place = ants.Place(name = "A")
        place.add_insect(body)
        place.add_insect(thrower)
        self.assertFalse(body.can_contain(thrower_1)) # already protecting thrower
        self.assertEqual(body.ant, thrower)
        
        # Insert HarvesterAnt first, and then Bogyguard
        place = ants.Place(name = "B")
        body, harv = ants.BodyguardAnt(), ants.HarvesterAnt()
        place.add_insect(harv)
        place.add_insect(body)
        self.assertEqual(place.ant, body) # body is the ant, harv is protected/hidden
        self.assertEqual(body.ant, harv)
        
        # Bodyguard should protect until it dies
        colony = create_colony()
        bee, body, harv = ants.Bee(armor=1), ants.BodyguardAnt(), ants.HarvesterAnt()
        colony.places["tunnel_0_5"].add_insect(bee)
        colony.places["tunnel_0_5"].add_insect(harv)
        colony.places["tunnel_0_5"].add_insect(body)
        orig_armor_body, orig_armor_harv = body.armor, harv.armor
        counter = 0 
        while body.armor > 0:
            bee.action(colony)
            counter += 1
        self.assertEqual(counter, orig_armor_body)
        self.assertEqual(body.armor, 0)
        self.assertTrue(colony.places["tunnel_0_5"].ant == harv) # Now body is dead, harv takes its place
        self.assertEqual(harv.armor, orig_armor_harv)
        bee.action(colony)
        self.assertEqual(harv.armor, 0)
    
    def test_imposter_and_unmovable_first_queen(self): 
        ants.QueenAnt.ctr_QueenAnt = 0 # ensure queenant is first queen
        queenant = ants.QueenAnt()
        self.assertTrue(queenant.firstQueenAnt)
        colony = create_colony()
        colony.places["tunnel_0_4"].add_insect(queenant)

        imposter = ants.QueenAnt()
        self.assertFalse(imposter.firstQueenAnt)
        colony.places["tunnel_0_5"].add_insect(imposter)
        self.assertEqual(imposter.armor, 1)
        imposter.action(colony)
        self.assertEqual(imposter.armor, 0) # die upon taking the first action()

        colony.places["tunnel_0_4"].remove_insect(queenant) # Unmovable first queen
        self.assertEqual(colony.places["tunnel_0_4"].ant, queenant)

    def test_dying_QueenAnt(self):
        ants.QueenAnt.ctr_QueenAnt = 0 # ensure queenant is first queen
        queenant = ants.QueenAnt()
        colony = create_colony()
        colony.places["tunnel_0_4"].add_insect(queenant)
        colony.places["tunnel_0_5"].add_insect(ants.Bee(armor=5))
        queenant.action(colony) # part of action() is to update colony.queen and search bees
        self.assertTrue(type(colony.queen), ants.QueenPlace)
        self.assertEqual(len(colony.queen.bees), 0)

        colony.places["tunnel_0_4"].add_insect(ants.BodyguardAnt() ) # Bodyguard should not help
        colony.places["tunnel_0_4"].add_insect(ants.Bee(armor=10))
        queenant.action(colony)
        self.assertTrue(len(colony.queen.bees) > 0)

    def test_double_damage(self):  
        ants.QueenAnt.ctr_QueenAnt = 0 # ensure queenant is first queen
        queenant = ants.QueenAnt()
        self.assertTrue(queenant.firstQueenAnt)
        thrower, ninja, body = ants.ThrowerAnt(), ants.NinjaAnt(), ants.BodyguardAnt()
        orig_damages = [queenant.damage, thrower.damage, ninja.damage, body.damage]
        
        colony = create_colony()
        colony.places["tunnel_0_5"].add_insect(thrower)
        colony.places["tunnel_0_5"].add_insect(body)
        colony.places["tunnel_0_1"].add_insect(ninja)
        colony.places["tunnel_0_3"].add_insect(queenant)
        
        queenant.action(colony)
        self.assertEqual(queenant.damage, orig_damages[0]) # QueenAnt should not double herself
        self.assertEqual(thrower.damage,2*orig_damages[1])
        self.assertEqual(ninja.damage,  2*orig_damages[2])
        
        for ant in queenant.doubled_ants: # Ensure doubled_ants list is correct
            self.assertTrue(ant.name in ["Thrower", "Ninja"])
            self.assertFalse(ant.name=="Bodyguard") # Bodyguard should not be in, b/s it protects ThrowerAnt
            self.assertFalse(ant.name=="Queen")
        
        # Damage levels should not double again in the 2nd action()
        queenant.action(colony)
        self.assertEqual(queenant.damage, orig_damages[0]) 
        self.assertEqual(thrower.damage,2*orig_damages[1])
        self.assertEqual(ninja.damage,  2*orig_damages[2])

        queenant.check_ants_damage_levels() # Nothing to assert but to verify Thrower and Ninja damage doubled to 2

    def test_run_fn_over_entire_tunnel(self):    
        ants.QueenAnt.ctr_QueenAnt = 0 # ensure queenant is first queen
        queenant = ants.QueenAnt()
        
        colony = create_colony()
        colony.places["tunnel_0_3"].add_insect(queenant)
        
        print("\nVerify the run_fn_over_entire_tunnel() follows the right sequence")
        print_place = lambda p: print(p.name)
        queenant.run_fn_over_entire_tunnel(print_place) # Nothing to assert but to ensure the sequence is 3,4,5,6,7, Hive,3,2,1,0,AntQueen

class test_extra_credit(unittest.TestCase):
    def test_make_slow_make_stun(self):
        slow = ants.SlowThrower()
        bee = ants.Bee(armor=1)
        colony = create_colony()
        colony.places["tunnel_0_3"].add_insect(slow)
        colony.places["tunnel_0_3"].add_insect(bee)
        
        colony.time = 3
        self.assertEqual( ants.make_slow(bee.action)(colony), "make_slow: do nothing") # do nothing
        
        colony.time = 4
        self.assertEqual( ants.make_slow(bee.action)(colony), None) # do bee.action(colony)
        self.assertEqual( slow.armor, 0) # should subsequently kill the colocated SlowThrower
        
        self.assertEqual( ants.make_stun(bee.action)(colony), "make_stun: do nothing") 

    def test_apply_effect(self):
        pass
        


##############################################################
# Utilities and helpers
def create_colony():
    assault_plan = ants.make_test_assault_plan()
    hive = ants.Hive(assault_plan)
    ant_types = [ants.HarvesterAnt, ants.ThrowerAnt, ants.FireAnt, ants.ShortThrower, ants.LongThrower, 
                 ants.WallAnt, ants.NinjaAnt, ants.ScubaThrower, ants.HungryAnt, ants.BodyguardAnt,
                 ants.QueenAnt, ants.SlowThrower, ants.StunThrower]
    return ants.AntColony(None, hive, ant_types, ants.test_layout, 10)


if __name__ == "__main__":
    # unittest.main(verbosity=0, buffer=True, exit=False) # If want to suppress stdout
    unittest.main()
