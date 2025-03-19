from data_wrappers.data_manager import *
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from player_new import Player


class Goal:
    def __init__(self, priority=8, role=None, **kwargs):
        self.priority = priority
        self.role = role

        GoalManager.add_goal(self)

    def perform(self, player):
        player.set_goal(self)
        self._perform(player)

    def _perform(self, player):
        raise NotImplementedError

    def can_trigger(self, player):
        if self.role and self.role != player.role:
            return False
        return self._can_trigger(player)

    def can_perform(self, player):
        if self.role and self.role != player.role:
            return False
        return self._can_perform(player)

    def _can_trigger(self, player):
        return True

    def _can_perform(self, player):
        return True


class GoalManager:
    goals: list[list[Goal]] = [[] for _ in range(10)]

    @staticmethod
    def find_goal(player, max_priority=10) -> Goal:
        for p, goals in enumerate(GoalManager.goals):
            if p >= max_priority:
                return player.goal
            for goal in goals:
                if goal.can_trigger(player) and goal.can_perform(player):
                    return goal

    @staticmethod
    def perform(player):
        goal = GoalManager.find_goal(player)
        if goal:
            goal.perform(player)
            return True
        return False

    @staticmethod
    def add_goal(goal):
        GoalManager.goals[goal.priority].append(goal)

    @staticmethod
    def remove_goal(goal):
        if goal in GoalManager.goals[goal.priority]:
            GoalManager.goals[goal.priority].remove(goal)

    @staticmethod
    def goal_loop(player):
        while True:
            if not GoalManager.perform(player):
                return


class StockGoal(Goal):
    def __init__(self, item, trigger_qty, replenish_qty=None, monster=None, utility=None, **kwargs):
        super().__init__(**kwargs)
        self.item = item
        self.trigger_qyt = trigger_qty
        self.replenish_qty = replenish_qty or trigger_qty
        self.current_stock = 0
        self.resource = item.resource
        self.craft = item.craft
        self.monster = monster
        self.utility: Item = utility

    def __repr__(self):
        if self.resource:
            return "Gathering %s for %s %s->%s" % (self.resource, self.item, self.current_stock, self.replenish_qty)
        if self.monster:
            return "Monster %s for %s %s->%s" % (self.monster, self.item, self.current_stock, self.replenish_qty)
        return "Stocking %s %s->%s" % (self.item, self.current_stock, self.replenish_qty)

    def _can_trigger(self, player: 'Player'):
        self.current_stock = player.stock_total(self.item)
        if player.goal is self and self.current_stock < self.replenish_qty:
            return True
        triggered = self.current_stock < self.trigger_qyt
        return triggered

    def _can_perform(self, player):
        if self.resource:
            return self.resource.level <= player.get_level(self.resource.skill) and self.resource.tile_content.is_active(player.get_server_time(), player.get_cooldown_time())
        if self.craft:
            return self.craft.level <= player.get_level(self.craft.skill) and player.items_available(self.craft.materials)
        return True

    def _perform(self, player: 'Player'):
        if self.resource:
            return player.perform_gather(self.resource)
        if self.monster:
            return player.perform_fight(self.monster, self.utility)
        if self.craft:
            return player.perform_craft(self.item, batch=True)
        return


class LevelGoal(Goal):
    def __init__(self, skill, level, craft_item=None, batch=1, use_level_gear=True, recycle=False, **kwargs):
        super().__init__(**kwargs)
        self.skill = skill
        self.level = level
        self.craft_item: Item = craft_item
        self.batch = batch
        self.use_level_gear = use_level_gear
        self.recycle = recycle

    def __repr__(self):
        if self.craft_item:
            return "Leveling %s to lvl%s by crafting %s" % (self.skill, self.level, self.craft_item)
        return "Leveling %s to lvl%s" % (self.skill, self.level)

    def _can_trigger(self, player: 'Player'):
        if self.level <= player.get_level(self.skill):
            return False
        if self.craft_item:
            return self.can_trigger_craft(player)
        return False

    def _can_perform(self, player):
        if self.craft_item:
            return self.can_perform_craft(player)
        return True

    def _perform(self, player: 'Player'):
        if self.use_level_gear:
            player.equip_gear_effect(Effect.wisdom)
        if self.craft_item:
            player.perform_craft(self.craft_item, self.recycle)

    def can_trigger_craft(self, player):
        if player.goal is self:
            n = 1
        else:
            n = self.batch
        items = [(item, qty*n) for item, qty in self.craft_item.craft.materials]
        return player.items_available(items)

    def can_perform_craft(self, player):
        return self.craft_item.craft.level <= player.get_level(self.skill)


class TaskGoal(Goal):
    def __init__(self, max_level, **kwargs):
        super().__init__(**kwargs)
        self.max_level = max_level

    def __repr__(self):
        return "Doing tasks lvl%s" % self.max_level

    def _can_trigger(self, player):
        return True

    def _can_perform(self, player):
        return True

    def _perform(self, player: 'Player'):
        player.perform_monster_task(self.max_level)


class SellGoal(Goal):
    def __init__(self, items, items_to_keep=None, **kwargs):
        super().__init__(**kwargs)
        self.items = items
        self.items_to_keep = items_to_keep or {}

    def __repr__(self):
        return "selling %s" % self.items

    def _can_trigger(self, player: 'Player'):
        for item in self.items:
            if item.npc_item.npc.tile_content.is_active(player.get_server_time(), player.get_cooldown_time()) and player.stock_available(item) > self.items_to_keep.get(item, 0):
                return True
        return False

    def _perform(self, player: 'Player'):
        items_to_ensure = []
        for item in self.items:
            if item.npc_item.npc.tile_content.is_active(player.get_server_time(), player.get_cooldown_time()) and player.stock_available(item) > self.items_to_keep.get(item, 0):
                items_to_ensure.append((item, player.stock_available(item) - self.items_to_keep.get(item, 0)))
        player.ensure_items(items_to_ensure)
        for item, n in items_to_ensure:
            player.npc_sell(item)


