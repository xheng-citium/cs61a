"""The ants module implements game logic for Ants Vs. SomeBees."""

import random
import sys
from ucb import main, interact, trace
from collections import OrderedDict
import copy, pdb

################
# Core Classes #
################

class Place:
    """A Place holds insects and has an exit to another Place."""

    def __init__(self, name, exit=None):
        """Create a Place with the given exit.
        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit
        if self.exit:
            self.exit.entrance = self

    def get_name(self):
        return self.name

    def add_insect(self, insect):
        """Add an Insect to this Place.
        There can be at most one Ant in a Place, unless exactly one of them is
        a BodyguardAnt (Phase 4), in which case there can be two. If add_insect
        tries to add more Ants than is allowed, an assertion error is raised.
        There can be any number of Bees in a Place.
        """
        if insect.is_ant:
            # Phase 4: Special handling for BodyguardAnt
            if self.ant is None:
                self.ant = insect
            else:
                if self.ant.can_contain(insect): # self.ant can contain
                    self.ant.contain_ant(insect)

                elif insect.can_contain(self.ant): 
                    insect.contain_ant(self.ant)
                    self.ant = insect
                else:
                    raise AssertionError('{0} is full. Cannot insert new ant.'.format(self))
        else:
            self.bees.append(insect)
        insect.place = self

    def remove_insect(self, insect):
        """
        Remove an Insect from this Place.
            Do nothing on 1st QueenAnt -> pass
            If Bodyguard is alone, not protecting anything -> pass
            If Bodyguard protects a fellow ant, it drops first and then its fellow -> pass 
        """

        if insect.is_ant:
            assert self.ant == insect, '{0} is not in {1}'.format(insect, self)

            # Phase 4: Special handling for BodyguardAnt and QueenAnt
            if isinstance(insect, QueenAnt) and insect.firstQueenAnt:
                return # cannot drop the first QueenAnt
            if insect.container and insect.ant: # insect is a Bodyguard and is protecting other
                self.ant = insect.ant
            else:
                self.ant = None # remove the ant 
        else:
            self.bees.remove(insect)

        insect.place = None

    def __str__(self):
        return self.name

class Insect:
    """An Insect, the base class of Ant and Bee, has armor and a Place."""
    name = ""
    is_ant = False
    watersafe = False

    def __init__(self, armor, place=None):
        """Create an Insect with an armor amount and a starting Place."""
        self.armor = armor
        self.place = place  # set by Place.add_insect and Place.remove_insect
    
    def is_watersafe(self):
        return self.watersafe

    def get_armor(self):
        return self.armor

    def get_name(self):
        return self.name

    def reduce_armor(self, amount):
        self.armor -= amount
        if self.armor <= 0:
            print('{0} ran out of armor and expired'.format(self))
            self.place.remove_insect(self)

    def action(self, colony):
        """The action performed each turn.

        colony -- The AntColony, used to access game state information.
        """

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.armor, self.place)

class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'Bee'
    watersafe = True

    def __init__(self, armor, place=None):
        Insect.__init__(self, armor, place)
        self.orig_action = self.action

    def sting(self, ant):
        """Attack an Ant, reducing the Ant's armor by 1."""
        ant.reduce_armor(1)

    def move_to(self, place):
        """Move from the Bee's current Place to a new Place."""
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""
        # Phase 3: Special handling for NinjaAnt
        return self.place.ant is not None and self.place.ant.blocks_path

    def action(self, colony):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        colony -- The AntColony, used to access game state information.
        """
        if self.blocked():
            self.sting(self.place.ant)
        elif self.place is not colony.hive and self.armor > 0:
            self.move_to(self.place.exit)

class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    is_ant = True
    damage = 0
    food_cost = 0
    blocks_path = True # True except for Ninja
    container   = False # Can contain other ants or not
    implemented = False  # Only implemented Ant classes should be instantiated

    def __init__(self, armor=1):
        """Create an Ant with an armor quantity."""
        Insect.__init__(self, armor)
    
    def can_contain(self, other): # problem 8 
        """self is a container, other is not and self's container is empty
        i.e. even if self is a container, it ma not be able to contain other right now"""
        return self.container and (not other.container) and (self.ant is None)
    
    def get_food_cost(self):
        return self.food_cost

    def get_damage(self):
        return self.damage

class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony."""

    name = 'Harvester'
    food_cost = 2
    implemented = True

    def action(self, colony):
        """Produce 1 additional food for the colony.
        colony -- The AntColony, used to access game state information.
        """
        colony.food += 1 

def random_or_none(s):
    """Return a random element of sequence s, or return None if s is empty."""
    if s:
        return random.choice(s)


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'
    damage = 1
    food_cost = 4 
    min_range, max_range = 0, 10
    implemented = True

    def nearest_bee(self, hive):
        """Return the nearest Bee in a Place that is not the Hive, connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        this_place = self.place
        curr_range = 0 # the current distance
        while this_place != hive:
            if (self.min_range <= curr_range <= self.max_range) and len(this_place.bees) > 0:
                return random_or_none(this_place.bees)
            curr_range += 1
            this_place = this_place.entrance


    def throw_at(self, target):
        """Throw a leaf at the target Bee, reducing its armor."""
        if target: 
            target.reduce_armor(self.damage)

    def action(self, colony):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee(colony.hive))


class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees:
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, colony):
        exits = [p for p in colony.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(colony.time, []):
            bee.move_to(random.choice(exits))

class AntColony:
    """An ant collective that manages global game state and simulates time.
    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    queen -- the place where the queen resides
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, strategy, hive, ant_types, create_places, food=2):
        """Create an AntColony for simulating a game.

        Arguments:
        strategy -- a function to deploy ants to places
        hive -- a Hive full of bees
        ant_types -- a list of ant constructors
        create_places -- a function that creates the set of places
        """
        self.time = 0
        self.food = food
        self.strategy = strategy
        self.hive = hive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.configure(hive, create_places)
    
    @property
    def colony_food(self):
        return self.food

    def get_time(self):
        return self.time

    def inc_time(self, v=1):
        self.time += v

    def set_time(self, value):
        assert value >= 0 and type(value) == int, "Input value must be a non-negative integer"
        self.time = value
        
    def configure(self, hive, create_places):
        """Configure the places in the colony."""
        self.queen = Place('AntQueen')
        self.places = OrderedDict()
        self.bee_entrances = [] # 
        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = hive
                self.bee_entrances.append(place)
        register_place(self.hive, False)
        create_places(self.queen, register_place)

    def simulate(self):
        """Simulate an attack on the ant colony (i.e., play the game)."""
        while len(self.queen.bees) == 0 and len(self.bees) > 0:
            #print("Colony time", self.time)
            self.hive.strategy(self)    # Bees invade
            self.strategy(self)         # Ants deploy
            for ant in self.ants:       # Ants take actions. from def ants(self)
                if ant.get_armor() > 0:
                    ant.action(self)
            for bee in self.bees:       # Bees take actions
                if bee.get_armor() > 0:
                    bee.action(self)
            self.time += 1
        if len(self.queen.bees) > 0:
            print('The ant queen has perished. Please try again.')
        else:
            print('All bees are vanquished. You win!')

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        constructor = self.ant_types[ant_type_name]
        if self.food < constructor.food_cost:
            print('Not enough food remains to place ' + ant_type_name)
        else:
            self.places[place_name].add_insect(constructor())
            self.food -= constructor.food_cost

    def remove_ant(self, place_name):
        """Remove an Ant from the Colony."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status


def ant_types():
    """Return a list of all implemented Ant classes."""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]

def interactive_strategy(colony):
    """A strategy that starts an interactive session and lets the user make
    changes to the colony.

    For example, one might deploy a ThrowerAnt to the first tunnel by invoking
    colony.deploy_ant('tunnel_0_0', 'Thrower')
    """
    print('colony: ' + str(colony))
    msg = '<Control>-D (<Control>-Z <Enter> on Windows) completes a turn.\n'
    interact(msg)

def start_with_strategy(args, strategy):
    """Reads command-line arguments and starts a game with those options."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Ants vs. SomeBees")
    parser.add_argument('-f', '--full', action='store_true',
                        help='loads a full layout and assault plan')
    parser.add_argument('-w', '--water', action='store_true',
                        help='loads a full layout with water')
    parser.add_argument('-i', '--insane', action='store_true',
                        help='loads a difficult assault plan')
    parser.add_argument('--food', type=int,
                        help='number of food to start with', default=2)
    args = parser.parse_args()

    assault_plan = make_test_assault_plan()
    layout = test_layout
    food = args.food
    if args.full:
        assault_plan = make_full_assault_plan()
        layout = dry_layout
    if args.water:
        layout = wet_layout
    if args.insane:
        assault_plan = make_insane_assault_plan()
    hive = Hive(assault_plan)
    AntColony(strategy, hive, ant_types(), layout, food).simulate()


###########
# Layouts #
###########

def wet_layout(queen, register_place, length=8, tunnels=3, moat_frequency=3):
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)

def dry_layout(queen, register_place, length=8, tunnels=3):
    """Register dry tunnels."""
    wet_layout(queen, register_place, length, tunnels, 0)

def test_layout(queen, register_place, length=8):
    """Register a single dry tunnel."""
    dry_layout(queen, register_place, length, 1)


#################
# Assault Plans #
#################


class AssaultPlan(dict):
    """The Bees' plan of attack for the Colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def __init__(self, bee_armor=3):
        self.bee_armor = bee_armor

    def add_wave(self, time, count):
        """Add a wave at time with count Bees that have the specified armor."""
        bees = [Bee(self.bee_armor) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    @property
    def all_bees(self):
        """Place all Bees in the hive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]

def make_test_assault_plan():
    return AssaultPlan().add_wave(2, 1).add_wave(3, 1)

def make_full_assault_plan():
    plan = AssaultPlan().add_wave(2, 1)
    for time in range(3, 15, 2):
        plan.add_wave(time, 1)
    return plan.add_wave(15, 8)

def make_insane_assault_plan():
    plan = AssaultPlan(4).add_wave(1, 2)
    for time in range(3, 15):
        plan.add_wave(time, 1)
    return plan.add_wave(15, 20)

##############
# Extensions #
##############

class Water(Place):
    """Water is a place that can only hold 'watersafe' insects."""

    def add_insect(self, insect):
        """Add insect if it is watersafe, otherwise reduce its armor to 0."""
        print('added', insect, insect.is_watersafe() )
        Place.add_insect(self, insect)
        if not insect.is_watersafe():
            insect.reduce_armor(insect.get_armor())


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""

    name = 'Fire'
    damage = 3
    food_cost = 4 
    implemented = True

    def reduce_armor(self, amount):
        self.armor -= amount
        if self.armor <= 0:
            for b in list(self.place.bees):
                b.reduce_armor(self.damage)
            self.place.remove_insect(self) # remove FireAnt itself


class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 4 places away."""
    name = 'Long'
    food_cost = 3
    min_range = 4
    implemented = True

class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees less than 3 places away."""
    name = 'Short'
    food_cost = 3
    max_range = 2
    implemented = True

# The WallAnt class
class WallAnt(Ant):       
    name = 'Wall' 
    food_cost = 4
    implemented = True    
    def __init__(self, armor=4):
        Ant.__init__(self, armor) # thick armor to hold off bees longer

class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place."""

    name = 'Ninja'
    damage = 1
    food_cost = 6
    blocks_path = False
    implemented = True

    def action(self, colony):  
        for b in list(self.place.bees): # deep-copy, b/c reduce_armor can remove a bee from self.place.bees
            b.reduce_armor(self.damage) 


# The ScubaThrower class
class ScubaThrower(ThrowerAnt):
    name = 'Scuba'
    food_cost = 5
    watersafe = True
    implemented = True


class HungryAnt(Ant):
    """HungryAnt will take three turns to digest a Bee in its place.
    While digesting, the HungryAnt can't eat another Bee.
    """
    name = 'Hungry'
    food_cost = 4
    time_to_digest = 3
    implemented = True

    def __init__(self):
        Ant.__init__(self)
        self.digesting = 0

    def eat_bee(self, bee):
        bee.reduce_armor(bee.get_armor())

    def action(self, colony):
        if self.digesting > 0:
            self.digesting -= 1
            return
        if self.place.bees:
            self.eat_bee(random_or_none(self.place.bees))
            self.digesting = self.time_to_digest

class BodyguardAnt(Ant):
    """BodyguardAnt provides protection to other Ants.
    damage level is 0"""
    name = 'Bodyguard'
    food_cost = 4
    container   = True # Can contain other ants
    implemented = True

    def __init__(self):
        Ant.__init__(self, armor=2)
        self.ant = None  # The Ant hidden in this bodyguard

    def contain_ant(self, ant):
        self.ant = ant

    def action(self, colony):
        if self.ant:
            self.ant.action(colony)


class QueenPlace:
    """A place that represents both places in which the bees find the queen.

    (1) The original colony queen location at the end of all tunnels, and
    (2) The place in which the QueenAnt resides.
    """
    def __init__(self, colony_queen, ant_queen):
        self._ant_queen = ant_queen
        self._colony_queen = colony_queen 

    @property
    def bees(self):
        return self._ant_queen.bees + self._colony_queen.bees

class QueenAnt(ScubaThrower):  
    """The Queen of the colony.  The game is over if a bee enters her place."""
    name = 'Queen'
    food_cost = 6
    ctr_QueenAnt = 0 # Counter of how many QueenAnt there are
    implemented = True

    def __init__(self):
        ScubaThrower.__init__(self, armor=1)
        QueenAnt.ctr_QueenAnt += 1
        self.firstQueenAnt = (QueenAnt.ctr_QueenAnt == 1) # first queen or an Imposter
        
        self.has_doubled_damage = False # track if QueenAnt has doubled damage of fellow ants
        self.doubled_ants = [] # track what ants have been doubled


    def action(self, colony):
        """ Main function of the class
        A queen ant throws a leaf, but also doubles the damage of ants in her tunnel.
        Impostor queens do only one thing: reduce their own armor to 0.
        Four steps:
            1: self-kill if is an imposter queen
            2: throw a leaf
            3: double damanges of fellow ants only once
            4: record locations of colony queen and QueenAnt -> needed by an early game over
        """
        # 1. self kill if imposter queen
        if not self.firstQueenAnt: 
            self.reduce_armor(self.armor)
            return
        
        # 2. Throws a leaf
        ScubaThrower.action(self, colony)
        
        # 3 double once and only once
        if not self.has_doubled_damage:
            run_fn_over_entire_tunnel(self.double_damage, self.place) # run function in entire tunnel starting from self.place
            self.has_doubled_damage = True
        
        # 4 Track both colony queen and QueenAnt; Trigger a game over if finding a bee
        colony.queen = QueenPlace(colony.queen, self.place)

    def double_damage(self, this_place):
        """ If found an ant at this place, Double its damage """
        if this_place.ant is None or isinstance(this_place.ant, QueenAnt): 
            return # do nothing if empty or QueenAnt herself

        # this_ant = the selected ant that will be doubled
        if this_place.ant.container:
            if this_place.ant.ant and (not isinstance(this_place.ant.ant, QueenAnt)):
                this_ant = this_place.ant.ant
            else:
                this_ant = None # A empty container
        else:
            this_ant = this_place.ant
        
        if this_ant:
            this_ant.damage *= 2
            assert this_ant not in self.doubled_ants, "{0} appears to be doubled twice".format(this_ant)
            self.doubled_ants.append(this_ant) # maintain a list of doubled ants

       
def run_fn_over_entire_tunnel(fn, curr_place):   
    """Run the given function over the tunnel in both directions sequentially"""
    this_place = curr_place
    output = []
    while this_place is not None:
        output.append( fn(this_place))
        this_place = this_place.entrance

    this_place = curr_place
    while this_place is not None:
        output.append( fn(this_place))
        this_place = this_place.exit
    
    return output


class AntRemover(Ant):
    """Allows the player to remove ants from the board in the GUI."""

    name = 'Remover'
    implemented = True

    def __init__(self):
        Ant.__init__(self, 0)

# NEW
class AntDestroyer(Ant):
    """ Remove all ants, except it is a QueenAnt"""
    name = "Destroyer"
    food_cost   = 10
    implemented = True

    def __init__(self):
        Ant.__init__(self)

    def action(self, colony):
        run_fn_over_entire_tunnel(self.remove_ant, self.place)

    def remove_ant(self, this_place):
        if this_place.ant is None or isinstance(this_place.ant, QueenAnt): 
            return

        if this_place.ant.container and isinstance(this_place.ant.ant, QueenAnt):
            this_place.ant = this_place.ant.ant
        else:
            this_place.ant = None


##################
# Status Effects #
##################

def make_slow(action):
    """Return a new action method that calls action every other turn.

    action -- An action method of some Bee
    """

    def new_action(colony):
        assert type(colony) == AntColony, "Input is not an AntColony object"
        return action(colony) if colony.time % 2 == 0 else None
    return new_action

def make_stun(action):
    """Return a new action method that does nothing.
    action -- An action method of some Bee
    """
    def new_action(colony):
        assert type(colony) == AntColony, "Input is not an AntColony object"
    return new_action

def apply_effect(effect, bee, duration):
    """Apply a status effect to a Bee that lasts for duration turns."""
    assert effect in [make_slow, make_stun], "Input: effect is not valid"
    assert type(duration) == int, "Input duration must be an int"
    assert isinstance(bee, Bee), "Input: bee must be of Bee type"

    orig_action = bee.action
    new_action  = effect(bee.action)

    def make_bee_action(colony):
        # This high-order function adds a necessary argument for action: colony 
        if duration <= 0:
            bee.action = orig_action
            bee.action(colony)
        else:
            nonlocal duration # make it nonlocal so that duraton can be decreased by 1
            duration -= 1
            new_action(colony)
    bee.action = make_bee_action

class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees."""

    name = 'Slow'
    food_cost = 4
    implemented = True

    def throw_at(self, target):
        if target:
            apply_effect(make_slow, target, 3)

class StunThrower(ThrowerAnt):
    """ThrowerAnt that causes Stun on Bees."""

    name = 'Stun'
    food_cost = 6
    implemented = True

    def throw_at(self, target):
        if target:
            apply_effect(make_stun, target, 1)


@main
def run(*args):
    start_with_strategy(args, interactive_strategy)
