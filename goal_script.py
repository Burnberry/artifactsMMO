from goal_base import *
from goals import *


def create_temp_goals(players):
    StockCraftGoal(Item.iron, 15, 40, role="miner", priority=7)
    StockCraftGoal(Item.spruce_plank, 15, 40, role="forager", priority=7)
    StockFightGoal(Item.feather, Monster.chicken, 20, 60, priority=5)
    # StockFightGoal(Item.mushroom, Monster.mushmush, 6, use_potions=True, priority=5)
    CraftLevelGoal(Item.iron_sword, 20, "Noppe", True, priority=6)
    CraftLevelGoal(Item.iron_boots, 20, "Noppe", True, priority=7)
    return


def create_main_goals(players):
    StandardGoal()
    GatherGoal(Resource.iron_rocks, role="fighter", priority=8)
    GatherGoal(Resource.strange_rocks, role="miner", priority=4)
    GatherGoal(Resource.magic_tree, role="forager", priority=4)
    SellGoal([NpcItem.golden_egg, NpcItem.golden_shrimp, NpcItem.silver_chalice], {NpcItem.silver_chalice: 5})
