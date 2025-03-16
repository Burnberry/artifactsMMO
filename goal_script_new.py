from goal_new import *


def create_level_goals():
    # crafting
    LevelGoal(Skill.jewelrycrafting, 20, Item.water_ring, recycle=True, use_level_gear=True, priority=7)


def create_gather_goal():
    # fight goal
    StockGoal(Item.skeleton_bone, 500, monster=Monster.skeleton, role="fighter", priority=7)

    # event gather goals
    StockGoal(Item.magic_wood, 30000, role="forager", priority=3)
    StockGoal(Item.strange_ore, 30000, role="miner", priority=3)

    # general goals
    StockGoal(Item.iron_ore, 30000, role="fighter")
    StockGoal(Item.maple_wood, 30000, role="forager")
    StockGoal(Item.iron_ore, 30000, role="miner")
    StockGoal(Item.sunflower, 100000, role="witch")
    StockGoal(Item.salmon, 100000, role="hunter")
