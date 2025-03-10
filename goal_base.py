from data_wrappers.data_manager import *
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player


class Goal:
    def __init__(self, priority=8, role=None, required=1, progress=0, **kwargs):
        self.parent_goal: 'Goal' = kwargs.get('parent_goal', None)
        self.sub_goals: list['Goal'] = []
        self.priority = priority
        self.role = role
        self.required = required
        self.progress = progress
        self.assigned_player: Player = None

        GoalManager.add_goal(self)

    def __repr__(self):
        return "Goal"

    def log(self, player):
        print(player, "performing:", self)

    def perform(self, player):
        player.set_goal(self)
        self._perform(player)

    def _perform(self, player):
        raise NotImplementedError

    def requirements_met(self) -> bool:
        raise NotImplementedError

    def could_perform(self, player) -> bool:
        if self.role and self.role != player.role:
            return False
        if self.assigned_player and self.assigned_player is not player:
            return False
        return self._could_perform(player)

    def _could_perform(self, player) -> bool:
        raise NotImplementedError

    def can_perform(self, player) -> bool:
        return self.requirements_met() and self.could_perform(player)

    def assign(self, player):
        self.assigned_player = player

    def is_needed(self):
        return True

    def create_sub_goals(self, **kwargs):
        return False


class GoalManager:
    goals: list[list[Goal]] = [[] for _ in range(10)]

    @staticmethod
    def find_goal(player, max_priority=10) -> Goal:
        for p, goals in enumerate(GoalManager.goals):
            if p >= max_priority:
                return
            for goal in goals:
                if goal.is_needed() and goal.can_perform(player):
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
