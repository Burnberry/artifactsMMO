from player import *
from goal_base import GoalManager


class Noppe(Player):
    def __init__(self):
        super().__init__("Noppe", "fighter")

    def task_loop(self):
        bank_data = self.get_bank_data_deprecated()
        while True:
            if not self.task:
                break
                # self.get_task('items')
            item = self.task.item
            quantity = self.task_total - self.task_progress

            if bank_data.get(item, 0) >= quantity:
                self.task_from_bank(item, quantity, bank_data)
                self.complete_task()
            else:
                print("crafting:", quantity, item)
                self.craft_items([(item, quantity)])
                bank_data[item] = quantity + bank_data.get(item, 0)

    def task_from_bank(self, item, quantity, bank_data):
        while quantity > 0:
            self.deposit_all()
            self.withdraw(item, min(self.inventory_max_items, quantity))
            quantity -= self.inventory_count
            bank_data[item] -= self.inventory_count
            self.turn_in_items(item, self.inventory_count)

    def script_main(self):
        # self.craft_items([(Items.iron, 26)])
        # self.craft_skill_loop(Items.greater_wooden_staff, 20)
        GoalManager.goal_loop(self)
        self.starter_achievement_loop()
        # self.craft_skill_loop(Items.iron_sword, 15)
        # self.craft_skill_loop(Items.greater_wooden_staff, 15)
        self.monster_task_loop()
        self.main_skills_loop()
        self.gather_loop(resource_forced=Resource.iron_rocks)


class Rubius(Player):
    def __init__(self):
        super().__init__("Rubius", "forager")

    def script_main(self):
        self.starter_achievement_loop()
        self.equip_lvl1()
        self.ensure_equipment(Item.iron_axe)
        # self.monster_task_loop()
        # if (n := self.bank_inventory.get(Items.spruce_wood, 0)) > 100:
        #     self.craft_items([(Items.spruce_plank, n//10)])
        self.main_skills_loop()
        # self.craft_loop(Item.ash_plank, (-2, -3), 80)
        self.gather_loop(resource_forced=Resource.spruce_tree)
        # self.gather_loop(Resources.ash_tree.skill)


class Pebbleboy(Player):
    def __init__(self):
        super().__init__("Pebbleboy", 'miner')

    def script_main(self):
        self.starter_achievement_loop()
        self.equip_lvl1()
        self.ensure_equipment(Item.iron_pickaxe)
        # if (n := self.bank_inventory.get(Items.iron_ore, 0)) > 100:
        #     self.craft_items([(Items.iron, n//10)])
        # self.monster_task_loop()
        self.main_skills_loop()
        self.gather_loop(resource_forced=Resource.gold_rocks)
        # self.gather_loop(resource=Resources.copper_rocks)


class Leandra(Player):
    def __init__(self):
        super().__init__("Leandra", "hunter")
        self.goal_manager = None

    def script_main(self):
        self.starter_achievement_loop()
        self.equip_lvl1()
        self.ensure_equipment(Item.spruce_fishing_rod)
        # self.monster_task_loop()
        self.main_skills_loop()
        # self.craft_loop(Item.small_health_potion, (2, 3), 800)
        self.gather_loop(skill=Resource.gudgeon_fishing_spot.skill)
        # self.gather_loop(Resources.gudgeon_fishing_spot.skill)


class Hekate(Player):
    def __init__(self):
        super().__init__("Hekate", "witch")
        self.goal_manager = None

    def script_main(self):
        if self.goal_manager:
            print("Goaling")
            goaling = True
            while goaling:
                goaling = self.goal_manager._perform(self)
        self.starter_achievement_loop()
        self.ensure_equipment(Item.leather_gloves)
        self.equip_lvl1()
        # self.monster_task_loop()
        self.main_skills_loop()
        self.gather_loop(skill=Resource.sunflower_field.skill)
