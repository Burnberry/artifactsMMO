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
            player.gather_batch(Resource.gudgeon_fishing_spot.skill)
        elif player.role == 'fighter':
            player.gather_batch(Item.iron_ore)


class TaskGoal(Goal):
    def __init__(self, **kwargs):
        super().__init__(role="fighter", **kwargs)

    def __repr__(self):
        return "Doing Monster Tasks"

    def requirements_met(self) -> bool:
        return True

    def _could_perform(self, player) -> bool:
        if not player.task:
            return player.get_available_qty(Item.tasks_coin) > 0
        return self.has_healing(player)

    def _perform(self, player):
        if not player.task:
            return player.get_task("monsters")
        if self.should_reroll(player):
            player.ensure_items([(Item.tasks_coin, 1)], 5)
            return player.reroll_task()
        if player.task_total <= player.task_progress:
            return player.complete_task()
        if player.inventory_max_items <= player.inventory_count:
            return player.deposit_all()
        self.ensure_healing(player)
        player.move(player.task.monster.tile_content.tiles)
        self.heal(player)
        player.fight()

    def has_healing(self, player: Player):
        has_food = player.get_available_qty(Item.cooked_shrimp) > 0
        has_potions = player.task.level <= 8 or player.get_available_qty(Item.small_health_potion) > 10
        return has_food and has_potions

    def ensure_healing(self, player: Player):
        if not player.task.level <= 15 and (not player.utility1_slot or player.utility1_slot_quantity < 10):
            n = 100 - (player.utility1_slot_quantity or 0)
            player.ensure_items([(Item.small_health_potion, n)])
            player.equip(Item.small_health_potion, n, "utility1")
        else:
            if n := player.utility1_slot_quantity:
                player.deposit_all()
                player.unequip("utility1", n)

        if not player.inventory.get(Item.cooked_shrimp, 0) > 0:
            player.ensure_items([(Item.cooked_shrimp, 50)])

    def heal(self, player: Player):
        n = 150
        if player.task.level > 8:
            n = 0
        while player.max_hp > player.hp + n:
            player.use(Item.cooked_shrimp)

    def should_reroll(self, player):
        if player.task.level > 18:
            return True
        if player.task.level >= 8 and player.task_total > 250:
            return True
        return False


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


class StockGoal(Goal):
    def __init__(self, item, trigger_quantity, stock_quantity=None, **kwargs):
        super().__init__(**kwargs)
        self.item = item
        self.trigger_quantity = trigger_quantity
        self.stock_quantity = stock_quantity or trigger_quantity

    def __repr__(self):
        return "Stocking %s to %s" % (self.item, self.stock_quantity)

    def _could_perform(self, player) -> bool:
        trigger = player.get_available_qty(self.item) < self.trigger_quantity
        busy = player.goal is self and player.get_available_qty(self.item) < self.stock_quantity
        return trigger or busy

    def requirements_met(self) -> bool:
        return True


class StockCraftGoal(StockGoal):
    def __init__(self, item, trigger_quantity, stock_quantity=None, **kwargs):
        super().__init__(item, trigger_quantity, stock_quantity, **kwargs)
        self.level = item.craft.level
        self.skill = item.craft.skill

    def _could_perform(self, player) -> bool:
        res = super()._could_perform(player)
        can_craft = player.get_level(self.skill) >= self.level
        has_mats = player.item_sets_available(self.item.craft.materials) > 0
        return res and can_craft and has_mats

    def _perform(self, player):
        qty_to_craft = self.stock_quantity - player.get_available_qty(self.item)
        qty_to_craft = min(qty_to_craft, player.item_sets_available(self.item.craft.materials))
        player.craft_items([(self.item, qty_to_craft)])


class StockFightGoal(StockGoal):
    def __init__(self, item, monster, trigger_quantity, stock_quantity=None, use_potions=False, **kwargs):
        super().__init__(item, trigger_quantity, stock_quantity, role="fighter", **kwargs)
        self.monster = monster
        self.use_potions = use_potions

    def _could_perform(self, player: Player) -> bool:
        res = super()._could_perform(player)
        has_healing = player.get_available_qty(Item.cooked_shrimp) > 50
        return res and has_healing

    def requirements_met(self) -> bool:
        return True

    def _perform(self, player: Player):
        if not player.utility1_slot or player.utility1_slot_quantity < 10:
            n = 100-(player.utility1_slot_quantity or 0)
            player.ensure_items([(Item.small_health_potion, n)])
            return player.equip(Item.small_health_potion, n, "utility1")
        if not player.inventory.get(Item.cooked_shrimp, 0) > 0:
            return player.ensure_items([(Item.cooked_shrimp, 50)])
        if player.max_hp - player.hp >= 150:
            return player.use(Item.cooked_shrimp)
        if player.inventory_max_items <= player.inventory_count:
            return player.deposit_all()
        player.move(self.monster.tile_content.tiles)
        player.fight()


class StockGatherGoal(StockGoal):
    def __init__(self, item, resource, trigger_quantity, stock_quantity=None, use_potions=False, **kwargs):
        super().__init__(item, trigger_quantity, stock_quantity, **kwargs)
        self.resource = resource

    def _could_perform(self, player: Player) -> bool:
        res = super()._could_perform(player)
        has_level = player.get_level(self.resource.skill) >= self.resource.level
        return res and has_level

    def requirements_met(self) -> bool:
        return True

    def _perform(self, player: Player):
        if player.inventory_max_items <= player.inventory_count:
            return player.deposit_all()
        return player.gather_resource(self.resource)


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
