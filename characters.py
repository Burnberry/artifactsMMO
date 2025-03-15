from player import *
from goal_base import GoalManager


class Noppe(Player):
    def __init__(self):
        super().__init__("Noppe", "fighter")

    def script_main(self):
        # self.withdraw(Item.air_and_water_amulet)
        # self.withdraw(Item.water_ring, 2)
        # self.equip(Item.air_and_water_amulet)
        # self.equip(Item.water_ring, slot="ring1")
        # self.equip(Item.water_ring, slot="ring2")
        # self.withdraw(Item.steel_battleaxe)
        # self.withdraw(Item.fire_and_earth_amulet)
        # self.equip(Item.steel_battleaxe)
        # self.equip(Item.fire_and_earth_amulet)
        GoalManager.goal_loop(self)
        self.gather_loop(resource_forced=Resource.iron_rocks)


class Rubius(Player):
    def __init__(self):
        super().__init__("Rubius", "forager")

    def script_main(self):
        GoalManager.goal_loop(self)
        self.gather_loop(resource_forced=Resource.spruce_tree)


class Pebbleboy(Player):
    def __init__(self):
        super().__init__("Pebbleboy", 'miner')

    def script_main(self):
        GoalManager.goal_loop(self)
        self.gather_loop(Resource.gold_rocks.skill)


class Leandra(Player):
    def __init__(self):
        super().__init__("Leandra", "hunter")
        self.goal_manager = None

    def script_main(self):
        GoalManager.goal_loop(self)
        self.gather_loop(skill=Resource.gudgeon_fishing_spot.skill)


class Hekate(Player):
    def __init__(self):
        super().__init__("Hekate", "witch")
        self.goal_manager = None

    def script_main(self):
        GoalManager.goal_loop(self)
        self.gather_loop(skill=Resource.sunflower_field.skill)
