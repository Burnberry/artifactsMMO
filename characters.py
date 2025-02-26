from player import Player


class Noppe(Player):
    def __init__(self):
        super().__init__("Noppe")

    def script_main(self):
        self.script_mine_copper()


class Rubius(Player):
    def __init__(self):
        super().__init__("Rubius")

    def script_main(self):
        self.script_gather_wood()


class Leandra(Player):
    def __init__(self):
        super().__init__("Leandra")

    def script_main(self):
        self.script_gather_alchemy()


class Hella(Player):
    def __init__(self):
        super().__init__("Hella")

    def script_main(self):
        self.script_gather_fish()


class Pebbleboy(Player):
    def __init__(self):
        super().__init__("Pebbleboy")

    def script_main(self):
        self.script_mine_copper()
