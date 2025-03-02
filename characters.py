from player import *


class Noppe(Player):
    def __init__(self):
        super().__init__("Noppe")

    def task_loop(self):
        bank_data = self.get_bank_data()
        while True:
            if not self.task:
                self.get_task('items')
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


    def fight_loop(self, n=-1):
        heal_items = 50
        self.move(Grid.chicken.tiles)
        while heal_items > 0 and n != 0:
            if self.max_hp - self.hp >= 75:
                self.use(Items.cooked_gudgeon)
            else:
                n -= 1
                self.fight()
        self.script_main()

    def level_craft_loop(self):
        self.deposit_all()

    def script_main(self):
        self.task_loop()
        self.auto = True
        self.gather_loop(Resources.copper_rocks.skill)


class Rubius(Player):
    def __init__(self):
        super().__init__("Rubius")

    def script_main(self):
        # self.craft_loop(Item.ash_plank, (-2, -3), 80)
        self.gather_loop(Resources.ash_tree.skill)


class Pebbleboy(Player):
    def __init__(self):
        super().__init__("Pebbleboy")

    def script_main(self):
        self.gather_loop(Resources.copper_rocks.skill)


class Leandra(Player):
    def __init__(self):
        super().__init__("Leandra")

    def script_main(self):
        # self.craft_loop(Item.small_health_potion, (2, 3), 800)
        self.gather_loop(Resources.gudgeon_fishing_spot.skill)


class Hekate(Player):
    def __init__(self):
        super().__init__("Hekate")

    def script_main(self):
        self.gather_loop(Resources.sunflower_field.skill)
