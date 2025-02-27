from data.items import Item
from player import Player


class Noppe(Player):
    def __init__(self):
        super().__init__("Noppe")

    def fight_loop(self):
        heal_items = 90
        self.move(0, -1)
        while heal_items > 0:
            if self.max_hp - self.hp >= 75:
                self.use(Item.cooked_gudgeon)
            else:
                self.fight()
        self.script_main()

    def script_main(self):
        self.gather_loop((1, 7))


class Rubius(Player):
    def __init__(self):
        super().__init__("Rubius")

    def script_main(self):
        # self.craft_loop(Item.ash_plank, (-2, -3), 80)
        self.gather_loop((2, 6))


class Leandra(Player):
    def __init__(self):
        super().__init__("Leandra")

    def script_main(self):
        self.gather_loop((2, 2))


class Hella(Player):
    def __init__(self):
        super().__init__("Hella")

    def script_main(self):
        self.gather_loop((5, 2))


class Pebbleboy(Player):
    def __init__(self):
        super().__init__("Pebbleboy")

    def script_main(self):
        self.gather_loop((1, 7))
