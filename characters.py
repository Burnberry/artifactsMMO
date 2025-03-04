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

    def fight_loop(self, monster, n):
        for _ in range(n):
            if self.max_hp - self.hp >= 75:
                if self.inventory.get(Items.cooked_gudgeon, 0) <= 0:
                    self.ensure_items([(Items.cooked_gudgeon, 90)])
                else:
                    self.use(Items.cooked_gudgeon, 1)
            else:
                self.move(monster.tile_content.tiles)
                self.fight()

    def monster_task_loop(self):
        while True:
            if not self.task:
                self.get_task('monsters')
            while self.task.level > 7:
                if not self.inventory.get(Items.tasks_coin, 0) > 0:
                    return False
                self.action("action/task/cancel")
            self.fight_loop(self.task.monster, self.task_total-self.task_progress)

    def script_main(self):
        self.starter_achievement_loop()
        self.monster_task_loop()
        self.main_skills_loop()
        # self.craft_skill_loop(Items.copper_dagger, 5)
        # self.craft_skill_loop(Items.wooden_shield, 5)
        # self.craft_skill_loop(Items.copper_ring, 5)
        self.gather_loop(skill=Resources.gudgeon_fishing_spot.skill)
        # self.gather_loop(Resources.copper_rocks.skill)


class Rubius(Player):
    def __init__(self):
        super().__init__("Rubius")

    def script_main(self):
        self.starter_achievement_loop()
        self.cook_fish(Items.cooked_gudgeon)
        self.main_skills_loop()
        # self.craft_loop(Item.ash_plank, (-2, -3), 80)
        self.gather_loop(skill=Resources.ash_tree.skill)
        # self.gather_loop(Resources.ash_tree.skill)


class Pebbleboy(Player):
    def __init__(self):
        super().__init__("Pebbleboy")

    def script_main(self):
        self.starter_achievement_loop()
        self.cook_fish(Items.cooked_gudgeon)
        self.main_skills_loop()
        self.gather_loop(skill=Resources.copper_rocks.skill)
        # self.gather_loop(resource=Resources.copper_rocks)


class Leandra(Player):
    def __init__(self):
        super().__init__("Leandra")

    def script_main(self):
        self.starter_achievement_loop()
        self.cook_fish(Items.cooked_shrimp)
        self.main_skills_loop()
        # self.craft_loop(Item.small_health_potion, (2, 3), 800)
        self.gather_loop(skill=Resources.gudgeon_fishing_spot.skill)
        # self.gather_loop(Resources.gudgeon_fishing_spot.skill)


class Hekate(Player):
    def __init__(self):
        super().__init__("Hekate")

    def script_main(self):
        self.starter_achievement_loop()
        self.cook_fish(Items.cooked_shrimp)
        self.main_skills_loop()
        self.gather_loop(skill=Resources.gudgeon_fishing_spot.skill)
