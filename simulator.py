import matplotlib.pyplot as plt
import numpy as np
from data_wrappers.data_manager import *

plt.rcParams.update({'font.size': 10})


class Entity:
    def __init__(self, hp, damage, crit_chance, **kwargs):
        self.hp = hp
        self.damage = damage
        self.crit_chance = crit_chance


class Simulation:
    turns = 50

    def __init__(self, entity1: Entity, entity2: Entity):
        self.entity1: Entity = entity1
        self.entity2: Entity = entity2
        self.turn, self.player_turn = 0, True
        self.win_states = {}
        self.loss_states = {}
        self.states = {(0, self.entity1.hp, self.entity2.hp): 1}
        self.new_states = {}

        self.simulate()

        self.win_rate = 0
        self.loss_rate = 0

        self.process_results()
        print(self.win_rate, self.loss_rate)

    def simulate(self):
        while self.turn < self.turns and self.states:
            self.simulate_turn()

    def process_results(self):
        self.win_rate = sum(self.win_states.values())
        self.loss_rate = sum(self.loss_states.values())

    def simulate_turn(self):
        self.turn += 1
        self.player_turn = self.turn%2
        self.new_states = {}

        for (turn, hp1, hp2), p in self.states.items():
            self.update_states(hp1, hp2, p)

        self.states = self.new_states

    def update_states(self, hp1, hp2, p):
        e1, e2 = self.entity1, self.entity2
        if not self.player_turn:
            hp1, hp2 = hp2, hp1
            e1, e2 = e2, e1
        for dmg, p2 in self.get_damages(e1, e2):
            hp = hp2 - dmg
            hp = max(0, hp)

            if self.player_turn:
                key = (self.turn, hp1, hp)
            else:
                key = (self.turn, hp, hp1)

            if hp <= 0:
                if self.player_turn:
                    self.win_states[key] = p*p2 + self.win_states.get(key, 0)
                else:
                    self.loss_states[key] = p * p2 + self.loss_states.get(key, 0)
            else:
                self.new_states[key] = p*p2 + self.new_states.get(key, 0)

    def get_damages(self, entity1, entity2):
        if entity1.crit_chance <= 0:
            return [(entity1.damage, 1)]
        return [(entity1.damage, 1-entity1.crit_chance), (int(1.5*entity1.damage), entity1.crit_chance)]

    def plot_win_loss(self):
        x = [i+1 for i in range(self.turns)]
        tick_label = [['', str(i+1)][i%5 == 4 or i == 0] for i in range(self.turns)]
        win_y = [0 for _ in range(25)]
        loss_y = [0 for _ in range(25)]
        for (turn, hp, mhp), p in self.win_states.items():
            win_y[turn//2] += p
        for (turn, hp, mhp), p in self.loss_states.items():
            print(turn, turn//2 - 1)
            loss_y[turn//2 - 1] += p
        y, color = [], []
        for w, l in zip(win_y, loss_y):
            color.append('g')
            y.append(w)
            color.append('r')
            y.append(l)
        plt.bar(x, y, color=color, tick_label=tick_label)
        plt.xlabel("turn")
        plt.ylabel("win/loss chance")
        plt.show()
