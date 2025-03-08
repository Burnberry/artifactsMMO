from player import *


class Noppe(Player):
    def __init__(self):
        super().__init__("Noppe")

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
        self.starter_achievement_loop()
        # self.craft_skill_loop(Items.iron_sword, 15)
        # self.craft_skill_loop(Items.greater_wooden_staff, 15)
        self.monster_task_loop()
        self.main_skills_loop()
        self.gather_loop(skill=Resources.gudgeon_fishing_spot.skill)


class Rubius(Player):
    def __init__(self):
        super().__init__("Rubius")

    def script_main(self):
        self.starter_achievement_loop()
        self.equip_lvl1()
        self.ensure_equipment(Items.iron_axe)
        # self.monster_task_loop()
        if (n := self.bank_inventory.get(Items.spruce_wood, 0)) > 100:
            self.craft_items([(Items.spruce_plank, n//10)])
        self.main_skills_loop()
        # self.craft_loop(Item.ash_plank, (-2, -3), 80)
        self.gather_loop(skill=Resources.ash_tree.skill)
        # self.gather_loop(Resources.ash_tree.skill)


class Pebbleboy(Player):
    def __init__(self):
        super().__init__("Pebbleboy")

    def script_main(self):
        self.starter_achievement_loop()
        self.equip_lvl1()
        self.ensure_equipment(Items.iron_pickaxe)
        if (n := self.bank_inventory.get(Items.iron_ore, 0)) > 100:
            self.craft_items([(Items.iron, n//10)])
        # self.monster_task_loop()
        self.main_skills_loop()
        self.gather_loop(skill=Resources.copper_rocks.skill)
        # self.gather_loop(resource=Resources.copper_rocks)


class Leandra(Player):
    def __init__(self):
        super().__init__("Leandra")

    def script_main(self):
        self.starter_achievement_loop()
        self.equip_lvl1()
        self.ensure_equipment(Items.spruce_fishing_rod)
        # self.monster_task_loop()
        self.main_skills_loop()
        # self.craft_loop(Item.small_health_potion, (2, 3), 800)
        self.gather_loop(skill=Resources.gudgeon_fishing_spot.skill)
        # self.gather_loop(Resources.gudgeon_fishing_spot.skill)


class Hekate(Player):
    def __init__(self):
        super().__init__("Hekate")

    def script_main(self):
        self.starter_achievement_loop()
        self.ensure_equipment(Items.spruce_fishing_rod)
        self.equip_lvl1()
        # self.monster_task_loop()
        self.main_skills_loop()
        self.gather_loop(skill=Resources.gudgeon_fishing_spot.skill)
