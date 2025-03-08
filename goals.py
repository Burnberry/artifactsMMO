from goal_base import *
from player import Player


class StandardGoal(Goal):
    def __init__(self):
        super().__init__(priority=9)

    def __repr__(self):
        return "Standard Role Goal"

    def _could_perform(self, player) -> bool:
        return True

    def requirements_met(self) -> bool:
        return True

    def _perform(self, player):
        if player.role == 'miner':
            player.gather_batch(Items.copper_ore.skill)
        elif player.role == 'forager':
            player.gather_batch(Items.ash_wood.skill)
        elif player.role == 'hunter':
            player.gather_batch(Items.gudgeon.skill)
        elif player.role == 'witch':
            player.gather_batch(Items.sunflower.skill)
        elif player.role == 'fighter':
            player.gather_batch(Items.iron_ore)


class CraftGoal(Goal):
    def __init__(self, items: list[tuple[Item, int]], **kwargs):
        super().__init__(**kwargs)
        self.items = items

    def _could_perform(self, player):
        for item, qty in self.items:
            if player.get_level(item.craft.skill) < item.craft.level:
                return False
        return True

    def requirements_met(self):
        inventory = Player.bank_inventory
        materials = Player.get_required_crafting_materials(self.items)
        for item, qty in materials.items():
            if inventory.get(item, 0) < qty:
                return False
        return True

    def create_sub_goals(self, items):
        print("Requesting materials:", items)

    def _perform(self, player):
        print(player.name, "performing craft:", self.items)
        player.craft_items(self.items)


class LevelCraftGoal(Goal):
    def __init__(self, item, level, player):
        super().__init__()
        self.item = item
        self.level = level
        self.player = player

    def _could_perform(self, player) -> bool:
        return player.get_level(self.item.craft.skill) >= self.item.craft.level

    def requirements_met(self) -> bool:
        return 0 < self.player.item_sets_available(self.item.craft.materials)

    def _perform(self, player):
        player.craft_skill_batch(self.item, self.level)
        print(player.name, self.item.craft.skill, player.get_level(self.item.craft.skill))

    def is_needed(self):
        return self.player.get_level(self.item.craft.skill) < self.level
