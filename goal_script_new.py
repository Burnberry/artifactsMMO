from goal_new import *


def create_level_goals():
    pass
    # crafting
    # LevelGoal(Skill.jewelrycrafting, 20, Item.water_ring, recycle=True, use_level_gear=True, priority=7)


def create_task_goals():
    TaskGoal(9, role="forager", priority=7)
    TaskGoal(19, role="fighter", priority=7)


def create_misc_goals():
    sell_items = [Item.golden_egg, Item.golden_shrimp, Item.highwayman_dagger, Item.silver_chalice, Item.golden_chalice]
    keep_items = {Item.silver_chalice: 5, Item.golden_chalice: 5}
    SellGoal(sell_items, keep_items, role="fighter", priority=3)


def create_gather_goal():
    # fight goal
    # StockGoal(Item.skeleton_bone, 500, monster=Monster.skeleton, role="fighter", priority=7)
    # StockGoal(Item.spider_leg, 2, monster=Monster.spider, role="fighter", utility=Item.small_health_potion, priority=7)

    # craft goals
    StockGoal(Item.cooked_shrimp, 500, role="witch", priority=6)
    StockGoal(Item.cooked_trout, 1000, role="witch", priority=6)
    StockGoal(Item.cooked_bass, 1000, role="witch", priority=6)

    # event gather goals
    StockGoal(Item.magic_wood, 30000, role="forager", priority=3)
    StockGoal(Item.strange_ore, 30000, role="miner", priority=3)

    # general goals
    StockGoal(Item.iron_ore, 30000, role="fighter")
    StockGoal(Item.maple_wood, 30000, role="forager")
    StockGoal(Item.iron_ore, 30000, role="miner")
    StockGoal(Item.bass, 100000, role="witch")
    StockGoal(Item.salmon, 100000, role="hunter")
