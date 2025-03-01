from player import *


class Noppe(Player):
    def __init__(self):
        super().__init__("Noppe")

    def fight_loop(self):
        heal_items = 90
        self.move(0, -1)
        while heal_items > 0:
            if self.max_hp - self.hp >= 75:
                self.use(Items.cooked_gudgeon)
            else:
                self.fight()
        self.script_main()

    def script_main(self):
        self.gather_loop(Resources.copper_rocks.skill)


class Rubius(Player):
    def __init__(self):
        super().__init__("Rubius")

    def script_main(self):
        # self.craft_loop(Item.ash_plank, (-2, -3), 80)
        self.gather_loop(Resources.ash_tree.skill)


class Leandra(Player):
    def __init__(self):
        super().__init__("Leandra")

    def script_main(self):
        # self.craft_loop(Item.small_health_potion, (2, 3), 800)
        self.gather_loop(Resources.sunflower_field.skill)


class Hella(Player):
    def __init__(self):
        super().__init__("Hella")

    def script_main(self):
        self.gather_loop(Resources.gudgeon_fishing_spot.skill)


class Pebbleboy(Player):
    def __init__(self):
        super().__init__("Pebbleboy")

    def script_main(self):
        self.gather_loop(Resources.copper_rocks.skill)
