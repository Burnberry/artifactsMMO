from goal_base import *
from goals import *


def create_temp_goals(players):
    StockFightGoal(Item.feather, Monster.chicken, 20, 60, priority=5)
    # StockFightGoal(Item.green_cloth, Monster.highwayman, 300, priority=5)
    StockFightGoal(Item.flying_wing, Monster.flying_serpent, 200, priority=6)

    StockCraftGoal(Item.hardwood_plank, 250, role="forager", priority=7)
    StockGatherGoal(Item.iron_ore, Resource.iron_rocks, 360, role="miner", priority=7)
    StockGatherGoal(Item.nettle_leaf, Resource.nettle, 4700, role="witch", priority=7)
    StockCraftGoal(Item.iron, 400, role="miner", priority=7)
    StockCraftGoal(Item.steel, 500, role="miner", priority=8)
    StockCraftGoal(Item.cooked_trout, 1500, role="witch", priority=8)
    StockCraftGoal(Item.cooked_bass, 1000, role="witch", priority=8)
    StockCraftGoal(Item.cooked_salmon, 1000, role="witch", priority=8)
    # StockFightGoal(Item.green_cloth, Monster.highwayman, 2, use_potions=True, priority=5)
    TaskGoal(priority=7)
    # CraftLevelGoal(Item.adventurer_pants, 21, "Noppe", True, priority=4)
    CraftLevelGoal(Item.life_ring, 20, "Noppe", True, priority=5)
    CraftLevelGoal(Item.water_ring, 20, "Noppe", True, priority=5)
    # CraftLevelGoal(Item.iron_sword, 20, "Noppe", True, priority=6)
    # CraftLevelGoal(Item.iron_boots, 20, "Noppe", True, priority=7)
    return


def create_main_goals(players):
    StandardGoal()
    GatherGoal(Resource.iron_rocks, role="fighter", priority=8)
    GatherGoal(Resource.strange_rocks, role="miner", priority=4)
    GatherGoal(Resource.magic_tree, role="forager", priority=4)
    SellGoal([NpcItem.golden_egg, NpcItem.golden_shrimp, NpcItem.silver_chalice], {NpcItem.silver_chalice: 5})
