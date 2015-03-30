#!/usr/bin/python3

import unittest
import pdb
import ants

class phase_1(unittest.TestCase):
    def test_Harvester(self):
        harv = ants.HarvesterAnt()
        self.assertEqual(2, harv.get_food_cost())
        self.assertEqual(1, harv.get_armor())
       
        colony = create_colony()
        orig_food = colony.colony_food
        harv.action(colony)
        self.assertEqual(orig_food+1, colony.colony_food) # Harvester add colony food by 1
    
    def test_Thrower(self):        
        """ To test action(): Create a colony and put an ant and several bees in tunnel cells
        Note:
          I use colony.places["tunnel_0_0"].add_insect(thrower_0) to add a ThrowerAnt. There seems an equivalent way: colony.deploy_ant('tunnel_0_0', 'Thrower')"""
        
        colony = create_colony() 
        thrower = ants.ThrowerAnt()
        bee = ants.Bee(armor=2)
        
        colony.places["tunnel_0_6"].add_insect(bee)
        colony.places["tunnel_0_1"].add_insect(thrower)

        self.assertEqual(4, thrower.get_food_cost())

        # test action()
        orig_armor = bee.get_armor()
        thrower.action(colony)
        self.assertEqual(orig_armor-thrower.get_damage(), bee.get_armor())
        
        # NB: action range test is combined with LongThrower and ShortThrower(phase 2)
        # NB: nearest_bee() is tested in phase_2

    def test_Place(self):
        p_1 = ants.Place(name = "1")
        self.assertTrue(p_1.entrance is None)
        self.assertTrue(p_1.exit is None)

        p_2 = ants.Place(name = "2", exit = p_1) # connecting 2 Place objects
        self.assertTrue(p_2.entrance is None)
        self.assertTrue(p_2 == p_2.exit.entrance)
        self.assertTrue("1" == p_2.exit.get_name())
        
        # NB: testing add_insect, remove_insect is in later phases with BodyguardAnt

class phase_2(unittest.TestCase):
    def test_Water(self):
        bee = ants.Bee(armor = 1)
        self.assertTrue(bee.is_watersafe())
        waterplace = ants.Water("A")
        waterplace.add_insect(bee)
        self.assertEqual(1, bee.get_armor()) # bee is watersafe

        harv = ants.HarvesterAnt()
        waterplace = ants.Water("A")
        waterplace.add_insect(harv)
        self.assertEqual(0, harv.get_armor()) # Harvester is dead in water

        thrower = ants.HarvesterAnt()
        waterplace = ants.Water("A")
        waterplace.add_insect(thrower)
        self.assertEqual(0, thrower.get_armor())

    def test_FireAnt(self):
        """Procedure: Create a Place, and put a FireAnt and a Bee inside. When FireAnt is dead, Bee armor is reduced by a certain damage level"""
        place = ants.Place(name = "A")
        fire  = ants.FireAnt(armor=2)
        bee_1 = ants.Bee(armor = 3, place=place)
        bee_2 = ants.Bee(armor = 3, place=place)
        self.assertEqual(2, fire.get_armor() )
        self.assertEqual(3, bee_1.get_armor() )
        
        place.add_insect(fire)
        place.add_insect(bee_1)
        place.add_insect(bee_2)
        orig_armor_1 = bee_1.get_armor()
        
        fire.reduce_armor(1)
        self.assertEqual(orig_armor_1, bee_1.get_armor()) # No effect on bee_1 yet
                
        fire.reduce_armor(1) # FireAnt is dead, both bees's armer is reduced
        self.assertEqual(orig_armor_1 - fire.get_damage(), bee_1.get_armor())
        self.assertEqual(orig_armor_1 - fire.get_damage(), bee_2.get_armor())
   
    
    def test_nearest_bee(self):
        colony = create_colony() 
        thrower_0, thrower_1 = ants.ThrowerAnt(), ants.ThrowerAnt()
        
        bees = [ants.Bee(armor=1) for _ in range(0,4)]
        for k in colony.places.keys():
            if k == 'Hive': colony.places[k].add_insect(bees[0])
            if k == "tunnel_0_6": colony.places[k].add_insect(thrower_0)
            if k == "tunnel_0_0": colony.places[k].add_insect(thrower_1)
            if k == "tunnel_0_1": 
                colony.places[k].add_insect(bees[1])
                colony.places[k].add_insect(bees[2])
            if k == "tunnel_0_2": colony.places[k].add_insect(bees[3])

        selected = thrower_0.nearest_bee(colony.hive) # Only bees[0] in front of thrower_0 but it is in hive
        self.assertTrue(selected == None)
        
        # Test randomness
        ctr_1, ctr_2 = 0, 0        
        for _ in range(1000):
            self.assertFalse(selected == bees[3])
            selected = thrower_1.nearest_bee(colony.hive)
            if selected == bees[1]: # selected is either bee_1 or bee_2, but cannot be bee_3
                ctr_1 += 1
            elif selected == bees[2]:
                ctr_2 += 1
            else:
                raise AssertionError("Selected bee is unknown")

        self.assertTrue( abs(500-ctr_1) <= 47 ) # 3 standard deviation approximately
        self.assertTrue( abs(500-ctr_2) <= 47 )

    def test_long_short_thrower(self):
        longthrower  = ants.LongThrower()  
        shortthrower = ants.ShortThrower()
        thrower      = ants.ThrowerAnt()
        colony       = create_colony()   
        bee_0, bee_1 = ants.Bee(armor=3), ants.Bee(armor=3)
        for k in colony.places:
            if k == "tunnel_0_0": colony.places[k].add_insect(longthrower)
            if k == "tunnel_0_1": colony.places[k].add_insect(shortthrower)
            if k == "tunnel_0_2": colony.places[k].add_insect(thrower)
            if k == "tunnel_0_3": colony.places[k].add_insect(bee_0)
        self.assertTrue( longthrower.nearest_bee(colony.hive) == None) # bee_0 is too close  for long thrower
        self.assertEqual(bee_0, shortthrower.nearest_bee(colony.hive)) # ok for short thrower
        self.assertEqual(bee_0, thrower.nearest_bee(colony.hive)) # ok for thrower
        
        colony.places["tunnel_0_3"].remove_insect(bee_0)
        colony.places["tunnel_0_4"].add_insect(bee_1)
        self.assertEqual( bee_1, longthrower.nearest_bee(colony.hive))
        self.assertEqual( bee_1, thrower.nearest_bee(colony.hive))
        self.assertEqual( None, shortthrower.nearest_bee(colony.hive)) # bee_1 is too far

class phase_3(unittest.TestCase):
    def test_WallAnt(self):
        wall = ants.WallAnt()
        self.assertEqual(4, wall.get_armor())
        self.assertEqual(4, wall.get_food_cost())

        colony = create_colony()
        bee = ants.Bee(armor=1)
        colony.places["tunnel_0_3"].add_insect(wall)
        colony.places["tunnel_0_3"].add_insect(bee)
        for _ in range(4+1): # 4+1 b/c it takes 4 stings to kill the WallAnt and 1 more action for bee to next place
            bee.action(colony)
        self.assertEqual(0, wall.get_armor())
        self.assertEqual("tunnel_0_2", bee.place.get_name())

    def test_NinjaAnt(self):
        ninja = ants.NinjaAnt()
        self.assertEqual(6, ninja.get_food_cost())      
        bees = [ants.Bee(armor=2) for _ in range(3)]
        
        # Testing thrower blocks a bee
        colony = create_colony()
        thrower = ants.ThrowerAnt()
        colony.places["tunnel_0_7"].add_insect(thrower)
        colony.places["tunnel_0_7"].add_insect(bees[0])
        self.assertTrue(bees[0].blocked()) # thrower blocks bee_0
        bees[0].action(colony)
        self.assertEqual("tunnel_0_7", bees[0].place.get_name() ) # bees[0] did not move
        
        # Testing that ninja damages a bee but does not block it
        colony.places["tunnel_0_2"].add_insect(ninja)
        colony.places["tunnel_0_2"].add_insect(bees[1])
        colony.places["tunnel_0_2"].add_insect(bees[2])
        self.assertFalse(bees[1].blocked()) # ninja does not block

        orig_armor_0, orig_armor_1 = bees[0].get_armor(), bees[1].get_armor()
        
        ninja.action(colony)
        bees[1].action(colony)
        self.assertEqual("tunnel_0_1", bees[1].place.get_name()) # bees[1] moved forward
        self.assertEqual(orig_armor_0, bees[0].get_armor()) # no harm on bee_0
        self.assertEqual(orig_armor_1 - ninja.get_damage(), bees[1].get_armor()) # Colocated bees are damaged
        self.assertEqual(orig_armor_1 - ninja.get_damage(), bees[2].get_armor()) # Colocated bees are damaged
   
    def test_Scuba(self):
        scuba      = ants.ScubaThrower()
        self.assertTrue(scuba.is_watersafe())
        waterplace = ants.Water("A")
        orig_armor = scuba.get_armor()
        waterplace.add_insect(scuba)
        self.assertEqual(orig_armor, scuba.get_armor())
        self.assertIs(waterplace, scuba.place)


    def test_Hungry(self):
        hungry = ants.HungryAnt()
        bee_0, bee_1 = ants.Bee(armor=1), ants.Bee(armor=1)
        colony = create_colony()
        colony.places["tunnel_0_1"].add_insect(hungry)
        colony.places["tunnel_0_1"].add_insect(bee_0)
        hungry.action(colony)
        self.assertTrue(bee_0.get_armor() <= 0)
        self.assertEqual(hungry.digesting, ants.HungryAnt.time_to_digest)
        
        orig_digesting = hungry.digesting
        colony.places["tunnel_0_1"].add_insect(bee_1) # Add another bee
        orig_armor_1 = bee_1.get_armor()

        # Test the timing of Hungry after it just consumed bee_0
        counter = 0
        while counter <= orig_digesting:
            hungry.action(colony)
            if counter < orig_digesting:
                self.assertEqual( orig_armor_1, bee_1.get_armor()) # bee_1 armor should not reduce
            if counter == orig_digesting:
                self.assertEqual( 0, bee_1.get_armor()) 
            counter += 1
        
class phase_4(unittest.TestCase):
    def test_Bodyguard(self):
        body = ants.BodyguardAnt()
        thrower, thrower_1 = ants.ThrowerAnt(), ants.ThrowerAnt()
        self.assertEqual(2, body.get_armor())
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
        self.assertEqual(thrower, body.ant)
        
        # Insert HarvesterAnt first, and then Bogyguard
        place = ants.Place(name = "B")
        body, harv = ants.BodyguardAnt(), ants.HarvesterAnt()
        place.add_insect(harv)
        place.add_insect(body)
        self.assertEqual(body, place.ant) # body is the ant, harv is protected
        self.assertEqual(harv, body.ant)

    def test_Bodyguard_protects_until_dead(self): 
        colony = create_colony()
        bee, body, harv = ants.Bee(armor=1), ants.BodyguardAnt(), ants.HarvesterAnt()
        colony.places["tunnel_0_5"].add_insect(bee)
        colony.places["tunnel_0_5"].add_insect(harv)
        colony.places["tunnel_0_5"].add_insect(body)
        orig_armor_body, orig_armor_harv = body.get_armor(), harv.get_armor()
        
        counter = 0 
        while body.get_armor() > 0:
            bee.action(colony)
            counter += 1
        self.assertEqual(orig_armor_body, counter)
        self.assertEqual(0, body.get_armor())
        self.assertTrue(colony.places["tunnel_0_5"].ant == harv) # Now body is dead, harv takes its place
        self.assertEqual(orig_armor_harv, harv.get_armor())
        bee.action(colony)
        self.assertEqual(0, harv.get_armor())
    
    def test_imposter_and_unmovable_firstQueen(self): 
        ants.QueenAnt.ctr_QueenAnt = 0 # ensure queenant is first queen
        queenant = ants.QueenAnt()
        imposter = ants.QueenAnt()
        
        self.assertTrue(queenant.firstQueenAnt)
        self.assertTrue(queenant.is_watersafe())
        self.assertFalse(imposter.firstQueenAnt)

        colony = create_colony()
        colony.places["tunnel_0_4"].add_insect(queenant)
        colony.places["tunnel_0_5"].add_insect(imposter)
        
        self.assertEqual(1, imposter.get_armor())
        imposter.action(colony)
        self.assertEqual(0, imposter.get_armor()) # die upon taking the first action()
        
        # Unmovable first queen
        colony.places["tunnel_0_4"].remove_insect(queenant) 
        self.assertEqual(queenant, colony.places["tunnel_0_4"].ant)

    def test_dying_QueenAnt(self):
        ants.QueenAnt.ctr_QueenAnt = 0 # ensure queenant is first queen
        queenant = ants.QueenAnt()
        colony   = create_colony()
        colony.places["tunnel_0_4"].add_insect(queenant)
        colony.places["tunnel_0_5"].add_insect(ants.Bee(armor=5))
        queenant.action(colony) # part of action() is to update colony.queen and search bees
        self.assertTrue(ants.QueenPlace, type(colony.queen), )
        self.assertEqual(0, len(colony.queen.bees))

        colony.places["tunnel_0_4"].add_insect(ants.BodyguardAnt() ) # Bodyguard should not help
        colony.places["tunnel_0_4"].add_insect(ants.Bee(armor=10))
        queenant.action(colony)
        self.assertTrue(len(colony.queen.bees) > 0, "Ants not lost yet") # this is the condtion in AntColony.simulate() to stop the game

    def test_double_damage(self):  
        ants.QueenAnt.ctr_QueenAnt = 0 # ensure queenant is first queen
        queenant = ants.QueenAnt()
        self.assertTrue(queenant.firstQueenAnt)
        thrower, ninja, body = ants.ThrowerAnt(), ants.NinjaAnt(), ants.BodyguardAnt()
        orig_damages = [queenant.get_damage(), thrower.get_damage(), ninja.get_damage(), body.get_damage()]
        
        colony = create_colony()
        colony.places["tunnel_0_5"].add_insect(thrower)
        colony.places["tunnel_0_5"].add_insect(body)
        colony.places["tunnel_0_1"].add_insect(ninja)
        colony.places["tunnel_0_3"].add_insect(queenant)
        
        queenant.action(colony)
        self.assertEqual(orig_damages[0], queenant.get_damage()) # QueenAnt should not double herself
        self.assertEqual(2*orig_damages[1], thrower.get_damage())
        self.assertEqual(2*orig_damages[2], ninja.get_damage())
        
        for ant in queenant.doubled_ants: # Ensure doubled_ants list is correct
            self.assertTrue(ant.get_name() in ["Thrower", "Ninja"])
            self.assertFalse(ant.get_name() == "Bodyguard") # Bodyguard should not be in the list
            self.assertFalse(ant.get_name() == "Queen")
        
        # Damage levels should not double again in the 2nd action()
        queenant.action(colony)
        self.assertEqual(orig_damages[0], queenant.get_damage()) 
        self.assertEqual(2*orig_damages[0], thrower.get_damage())
        self.assertEqual(2*orig_damages[0], ninja.get_damage())

    def test_run_fn_over_entire_tunnel(self):    
        ants.QueenAnt.ctr_QueenAnt = 0 # ensure queenant is first queen
        queenant = ants.QueenAnt()
        
        colony = create_colony()
        colony.places["tunnel_0_3"].add_insect(queenant)
        
        # Verify the run_fn_over_entire_tunnel() follows the right sequence
        placeName = lambda p: p.get_name()
        places = ants.run_fn_over_entire_tunnel(placeName, colony.places["tunnel_0_3"])
        self.assertEqual(['tunnel_0_3', 'tunnel_0_4', 'tunnel_0_5', 'tunnel_0_6', 
                          'tunnel_0_7', 'Hive', 'tunnel_0_3', 'tunnel_0_2', 'tunnel_0_1', 
                          'tunnel_0_0', 'AntQueen'], places)


class extra_credit(unittest.TestCase):
    def test_destroyer(self):       
        colony = create_colony()
        body = [ ants.BodyguardAnt() for _ in range(2)] 
        thrower, queen = ants.ThrowerAnt(), ants.QueenAnt()
        harv     = ants.HarvesterAnt()
        destroyer = ants.AntDestroyer()
        self.assertEqual(10, destroyer.get_food_cost())

        colony.places["tunnel_0_0"].add_insect(body[0])
        colony.places["tunnel_0_0"].add_insect(queen)
        colony.places["tunnel_0_2"].add_insect(harv)
        colony.places["tunnel_0_5"].add_insect(thrower)
        colony.places["tunnel_0_5"].add_insect(body[1])
        
        colony.places["tunnel_0_6"].add_insect(destroyer)
        destroyer.action(colony)
        
        # Test if all ants are gone except the queen ant
        find_ant = lambda place: place.ant
        antlist = ants.run_fn_over_entire_tunnel(find_ant, colony.places["tunnel_0_0"])
        self.assertEqual(set([None, queen]), set(antlist))

    def test_slow_stun_params(self):
        slow = ants.SlowThrower()
        stun = ants.StunThrower()
        self.assertEqual(4, slow.get_food_cost(), "SlowThrower has wrong cost")
        self.assertEqual(6, stun.get_food_cost())
        self.assertEqual(1, slow.get_armor(), "SlowThrower has wrong armor")
        self.assertEqual(1, stun.get_armor())

    def test_make_slow_make_stun(self):
        slow   = ants.SlowThrower()
        bee    = ants.Bee(armor=1)
        colony = create_colony()
        colony.places["tunnel_0_3"].add_insect(slow)
        colony.places["tunnel_0_3"].add_insect(bee)
        
        colony.set_time(3)
        self.assertEqual(None, ants.make_slow(bee.action)(colony)) # do nothing
        self.assertEqual(1, slow.get_armor()) # colocated SlowThrower armor should not change
        
        colony.inc_time()
        self.assertEqual(None, ants.make_slow(bee.action)(colony)) # do bee.action(colony)
        self.assertEqual(0, slow.get_armor()) # subsequently kills the colocated SlowThrower
        
        # Test make_stun
        stun = ants.StunThrower()
        bee  = ants.Bee(armor=1)
        self.assertEqual(None, ants.make_stun(bee.action)(colony)) 

        colony = create_colony()
        colony.places["tunnel_0_0"].add_insect(stun)
        colony.places["tunnel_0_3"].add_insect(bee)

        stun.action(colony)
        bee.action(colony)
        self.assertEqual("tunnel_0_3", bee.place.name) # bee does not move
        bee.action(colony)
        self.assertEqual("tunnel_0_2", bee.place.name) # bee moves

    def test_apply_effect(self): 
        slow = ants.SlowThrower()
        bee = ants.Bee(armor=1)
        self.assertRaises(AssertionError, ants.apply_effect, "ants.make_slow", bee, 3)
        self.assertRaises(AssertionError, ants.apply_effect, ants.make_slow, slow, 3)
        self.assertRaises(AssertionError, ants.apply_effect, ants.make_slow, bee, 3.0) # float number not ok
       

    def test_slow_effect(self):
        # Test SlowTrhower stuns the bee for 3 turns and on the every other turn
        slow = ants.SlowThrower()
        slow_duration = 3
        bee = ants.Bee(armor=1)
        colony = create_colony()
        colony.places["tunnel_0_0"].add_insect(slow)
        colony.places["tunnel_0_7"].add_insect(bee)
        
        slow.action(colony)
        while colony.get_time() < 8:
            colony.inc_time() 
            prev_loc = int((bee.place.get_name()[-1])) # previous bee location
            
            bee.action(colony)
            if colony.get_time() > slow_duration or colony.get_time() % 2 == 0:
                self.assertEqual(prev_loc-1, int(bee.place.get_name()[-1]))# bee should have moved one step
            else:
                self.assertEqual(prev_loc , int(bee.place.get_name()[-1])) # bee does not move

    def test_stun_effect(self):
        # Test StunThrower stuns the bee for 1 turn
        stun = ants.StunThrower()
        bee = ants.Bee(armor=1)
        colony = create_colony()
        colony.places["tunnel_0_0"].add_insect(stun)
        colony.places["tunnel_0_7"].add_insect(bee)

        stun.action(colony)
        while colony.get_time() < 8:
            colony.inc_time() 
            prev_loc = int((bee.place.get_name()[-1])) # previous bee location
            
            bee.action(colony)
            if colony.get_time() == 1:
                # bee should not move
                self.assertEqual(prev_loc, int(bee.place.get_name()[-1]))
            else:
                self.assertEqual(prev_loc-1, int(bee.place.get_name()[-1]))

    def test_multiple_stun(self):
        stun = ants.StunThrower()
        bee = ants.Bee(1)
        colony = create_colony()
        colony.places["tunnel_0_0"].add_insect(stun)
        colony.places["tunnel_0_4"].add_insect(bee)
        
        # If bee is stunned for 3 times, it will not move for 3 times
        num = 3
        for _ in range(num): 
            stun.action(colony)

        for _ in range(num):
            bee.action(colony)
            self.assertEqual("tunnel_0_4", bee.place.get_name())

    def test_slow_stun_stack(self):
        """This is a translation of the autograder: tests/qEC.py """

        stun = ants.StunThrower()
        slow = ants.SlowThrower()
        bee = ants.Bee(armor=1)
        colony = create_colony()
        colony.places["tunnel_0_0"].add_insect(stun)
        colony.places["tunnel_0_1"].add_insect(slow)
        colony.places["tunnel_0_4"].add_insect(bee)
        
        # slow bee 3 times and stun it once
        for _ in range(3):
            slow.action(colony)
        stun.action(colony) 
 
        colony.set_time(0)
        bee.action(colony) # stunned
        self.assertEqual("tunnel_0_4", bee.place.get_name() )
 
        colony.inc_time()
        bee.action(colony) # slowed thrice
        self.assertEqual("tunnel_0_4", bee.place.get_name() )
 
        colony.inc_time()
        bee.action(colony) # slowed thrice
        self.assertEqual("tunnel_0_3", bee.place.get_name())
 
        colony.inc_time()
        bee.action(colony) # slowed thrice
        self.assertEqual("tunnel_0_3", bee.place.get_name() )
 
        colony.inc_time()
        bee.action(colony) # slowed twice
        self.assertEqual("tunnel_0_2", bee.place.get_name())
 
        colony.inc_time()
        bee.action(colony) # slowed twice
        self.assertEqual("tunnel_0_2", bee.place.get_name())
 
        colony.inc_time()
        bee.action(colony) # slowed once
        self.assertEqual("tunnel_0_1", bee.place.get_name())
 
        colony.inc_time()
        bee.action(colony) # no effect any more
        self.assertEqual(0, slow.get_armor()) # slow is killed by bee
 


##############################################################
# Utility functions
def create_colony():
    assault_plan = ants.make_test_assault_plan()
    hive = ants.Hive(assault_plan)
    ant_types = [ants.HarvesterAnt, ants.ThrowerAnt, ants.FireAnt,   ants.ShortThrower, 
                 ants.LongThrower,  ants.WallAnt,    ants.NinjaAnt,  ants.ScubaThrower, 
                 ants.HungryAnt,    ants.BodyguardAnt, ants.QueenAnt,ants.SlowThrower, 
                 ants.StunThrower,  ants.AntDestroyer]
    return ants.AntColony(None, hive, ant_types, ants.test_layout, 10)


if __name__ == "__main__":
    # unittest.main(verbosity=0, buffer=True, exit=False) # If want to suppress stdout
    unittest.main()
