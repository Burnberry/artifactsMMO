import datetime

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
            player.gather_batch(Resource.iron_rocks.skill)
        elif player.role == 'forager':
            player.gather_batch(Resource.ash_tree.skill)
        elif player.role == 'hunter':
            player.gather_batch(Resource.gudgeon_fishing_spot.skill)
        elif player.role == 'witch':
            player.gather_batch(Resource.sunflower_field.skill)
        elif player.role == 'fighter':
            player.gather_batch(Item.iron_ore)


class GatherGoal(Goal):
    def __init__(self, resource, **kwargs):
        super().__init__(**kwargs)
        self.resource: Resource = resource

    def __repr__(self):
        return "Gather goal - %s" % self.resource

    def _could_perform(self, player):
        return self.resource.level <= player.get_level(self.resource.skill)

    def requirements_met(self):
        if self.resource.tile_content.is_event:
            return self.resource.tile_content.is_active(Player.get_server_time())
        return True

    def _perform(self, player):
        if player.inventory_max_items <= player.inventory_count:
            return player.deposit_all()
        player.move(resource=self.resource)
        if self.requirements_met():
            player.gather_resource(self.resource)


class SellGoal(Goal):
    def __init__(self, npc_items: list[NpcItem], save_items=None, **kwargs):
        super().__init__(role="fighter", **kwargs)
        if not save_items:
            save_items = {}
        self.save_items = save_items
        self.npc_items = npc_items
        self.items_by_npc = {}
        for npc_item in npc_items:
            npc_list = self.items_by_npc.get(npc_item.npc, [])
            self.items_by_npc[npc_item.npc] = npc_list
            npc_list.append(npc_item)

    def __repr__(self):
        return "Sell goal: %s" % self.npc_items

    def _could_perform(self, player) -> bool:
        return True

    def requirements_met(self) -> bool:
        for npc in self.items_by_npc:
            if npc.tile_content.is_active(Player.get_server_time() + datetime.timedelta(minutes=20)):
                for npc_item in self.items_by_npc[npc]:
                    if Player.bank_inventory.get(npc_item.item, 0) > 0:
                        return True
        return False

    def _perform(self, player):
        npc_items = []
        for npc in self.items_by_npc:
            if npc.tile_content.is_active(Player.get_server_time() + datetime.timedelta(minutes=20)):
                for npc_item in self.items_by_npc[npc]:
                    npc_items.append((npc_item, player.get_available_items(npc_item.item) - self.save_items.get(npc_item, 0)))
        player.ensure_items([(npc_item.item, qty) for (npc_item, qty) in npc_items])
        for npc_item, quantity in npc_items:
            player.sell_npc_item(npc_item, quantity)


class LevelGoal(Goal):
    def __init__(self, skill, level, player_name, **kwargs):
        super().__init__(**kwargs)
        self.skill = skill
        self.level = level
        self.player_name = player_name

    def __repr__(self):
        return "Leveling %s to lvl%s" % (self.skill, self.level)

    def _could_perform(self, player) -> bool:
        return not self.player_reached_level(player)

    def player_reached_level(self, player):
        return player.get_level(self.skill) >= self.level

    def requirements_met(self) -> bool:
        return True


class CraftLevelGoal(LevelGoal):
    def __init__(self, item, level, player_name, recycle, min_craft_qty=1, **kwargs):
        super().__init__(item.craft.skill, level, player_name, **kwargs)
        self.item = item
        self.min_craft_qty = min_craft_qty
        self.recycle = recycle

    def _could_perform(self, player: Player) -> bool:
        res = super()._could_perform(player)
        can_craft = player.get_level(self.item.craft.skill) >= self.item.craft.level
        has_materials = self.min_craft_qty <= player.item_sets_available(self.item.craft.materials)
        is_correct_player = not self.player_name or self.player_name == player.name
        return res and can_craft and has_materials and is_correct_player

    def _perform(self, player):
        n = player.inventory_max_items//self.item.craft.material_count
        n = min(n, player.item_sets_available(self.item.craft.materials))
        # player.deposit_all()
        player.ensure_items(self.item.craft.materials, n)
        player.move(TileContent.get(self.skill).tiles)
        while player.on_hand(self.item.craft.materials):
            if self.player_reached_level(player):
                return
            player.craft(self.item)
            if self.recycle:
                player.recycle(self.item)


# class to review
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


# class to review
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
