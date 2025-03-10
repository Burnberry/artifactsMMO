from goal_base import *
from goals import *


def create_temp_goals(players):
    # CraftLevelGoal(Item.feather_coat, 10, "Noppe", True, priority=6)
    CraftLevelGoal(Item.health_potion, 40, "Hekate", False, priority=6)
    CraftLevelGoal(Item.cooked_trout, 30, "Hekate", False, priority=7)
    CraftLevelGoal(Item.cooked_bass, 40, "Hekate", False, priority=7)


def create_main_goals(players):
    StandardGoal()
    GatherGoal(Resource.iron_rocks, role="fighter", priority=8)
    GatherGoal(Resource.strange_rocks, role="miner", priority=4)
    GatherGoal(Resource.magic_tree, role="forager", priority=4)
    SellGoal([NpcItem.golden_egg, NpcItem.golden_shrimp, NpcItem.silver_chalice], {NpcItem.silver_chalice: 5})
