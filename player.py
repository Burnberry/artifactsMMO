import requests, threading
from time import sleep

from helpers import *
import positions as p


class Player:
    players = set()

    def __init__(self, name):
        Player.add_player(self)
        self.name = name
        self.base_path = url + "my/%s/" % self.name
        self.response = None
        self.get_character_data()
        self.auto = False
        self.thread = None

    def script_main(self):
        print("No main script made for", self.name)

    def script_gather_alchemy(self):
        self.gather_loop(p.sunflower)

    def script_gather_fish(self):
        self.gather_loop(p.fish)

    def script_gather_wood(self):
        self.gather_loop(p.tree)

    def script_mine_copper(self):
        self.gather_loop(p.copper)

    def gather_loop(self, location):
        while self.auto:
            if self.inventory_count >= self.inventory_max_items:
                self.deposit_all()
            else:
                self.gather(location)

    def gather(self, position):
        self.move(*position)
        self.post("action/gathering")

    def deposit_all(self):
        items = []
        for slot in self.inventory:
            code, quantity = slot.get('code'), slot.get('quantity')
            if code and quantity > 0:
                items.append((code, quantity))

        for item, quantity in items:
            self.deposit(item, quantity)

    def deposit(self, item, quantity):
        self.move(*p.bank)
        self.post("action/bank/deposit", {'code': item, 'quantity': quantity})

    def move(self, x, y):
        if self.x != x or self.y != y:
            self.post("action/move", {'x': x, 'y': y})

    def post(self, action, data=None):
        sleep(self.cooldown)
        self.response = requests.post(self.base_path+action, json=data, headers=headers)
        data = self.response.json()['data']
        if 'character' in data:
            self.set_player_data(data['character'])

    def start_thread(self, script=None, **kwargs):
        if not script:
            script = self.script_main
        self.thread = threading.Thread(target=script, kwargs=kwargs)
        self.auto = True
        self.thread.start()

    def stop_thread(self):
        if self.thread:
            self.auto = False
            self.thread.join()

    @staticmethod
    def add_player(player):
        Player.players.add(player)

    @staticmethod
    def remove_player(player):
        if player in Player.players:
            Player.players.remove(player)

    @staticmethod
    def get_player(name):
        for player in Player.players:
            if player.name == name:
                return player

    @staticmethod
    def stop_threads():
        for player in Player.players:
            player.stop_thread()

    @staticmethod
    def start_players(players):
        threads = []
        for player in players:
            threads.append(threading.Thread(target=player.script_main))
        i = 0
        for thread in threads:
            sleep(1)
            i += 1
            print("starting thread", i)
            thread.start()

    def get_character_data(self):
        response = requests.get(url + "characters/%s" % self.name)
        player_data = response.json()['data']
        self.set_player_data(player_data)

    def set_player_data(self, player_data):
        self._set_player_data(player_data)
        self.inventory_count = sum([slot['quantity'] for slot in self.inventory])

    def print_player_attributes(self, player_data):
        # used for _set_player_data
        for key in player_data:
            print("self.%s = player_data.get('%s', None)" % (key, key))

    def _set_player_data(self, player_data):
        self.name = player_data.get('name', None)
        self.account = player_data.get('account', None)
        self.skin = player_data.get('skin', None)
        self.level = player_data.get('level', None)
        self.xp = player_data.get('xp', None)
        self.max_xp = player_data.get('max_xp', None)
        self.gold = player_data.get('gold', None)
        self.speed = player_data.get('speed', None)
        self.mining_level = player_data.get('mining_level', None)
        self.mining_xp = player_data.get('mining_xp', None)
        self.mining_max_xp = player_data.get('mining_max_xp', None)
        self.woodcutting_level = player_data.get('woodcutting_level', None)
        self.woodcutting_xp = player_data.get('woodcutting_xp', None)
        self.woodcutting_max_xp = player_data.get('woodcutting_max_xp', None)
        self.fishing_level = player_data.get('fishing_level', None)
        self.fishing_xp = player_data.get('fishing_xp', None)
        self.fishing_max_xp = player_data.get('fishing_max_xp', None)
        self.weaponcrafting_level = player_data.get('weaponcrafting_level', None)
        self.weaponcrafting_xp = player_data.get('weaponcrafting_xp', None)
        self.weaponcrafting_max_xp = player_data.get('weaponcrafting_max_xp', None)
        self.gearcrafting_level = player_data.get('gearcrafting_level', None)
        self.gearcrafting_xp = player_data.get('gearcrafting_xp', None)
        self.gearcrafting_max_xp = player_data.get('gearcrafting_max_xp', None)
        self.jewelrycrafting_level = player_data.get('jewelrycrafting_level', None)
        self.jewelrycrafting_xp = player_data.get('jewelrycrafting_xp', None)
        self.jewelrycrafting_max_xp = player_data.get('jewelrycrafting_max_xp', None)
        self.cooking_level = player_data.get('cooking_level', None)
        self.cooking_xp = player_data.get('cooking_xp', None)
        self.cooking_max_xp = player_data.get('cooking_max_xp', None)
        self.alchemy_level = player_data.get('alchemy_level', None)
        self.alchemy_xp = player_data.get('alchemy_xp', None)
        self.alchemy_max_xp = player_data.get('alchemy_max_xp', None)
        self.hp = player_data.get('hp', None)
        self.max_hp = player_data.get('max_hp', None)
        self.haste = player_data.get('haste', None)
        self.critical_strike = player_data.get('critical_strike', None)
        self.wisdom = player_data.get('wisdom', None)
        self.prospecting = player_data.get('prospecting', None)
        self.attack_fire = player_data.get('attack_fire', None)
        self.attack_earth = player_data.get('attack_earth', None)
        self.attack_water = player_data.get('attack_water', None)
        self.attack_air = player_data.get('attack_air', None)
        self.dmg = player_data.get('dmg', None)
        self.dmg_fire = player_data.get('dmg_fire', None)
        self.dmg_earth = player_data.get('dmg_earth', None)
        self.dmg_water = player_data.get('dmg_water', None)
        self.dmg_air = player_data.get('dmg_air', None)
        self.res_fire = player_data.get('res_fire', None)
        self.res_earth = player_data.get('res_earth', None)
        self.res_water = player_data.get('res_water', None)
        self.res_air = player_data.get('res_air', None)
        self.x = player_data.get('x', None)
        self.y = player_data.get('y', None)
        self.cooldown = player_data.get('cooldown', None)
        self.cooldown_expiration = player_data.get('cooldown_expiration', None)
        self.weapon_slot = player_data.get('weapon_slot', None)
        self.rune_slot = player_data.get('rune_slot', None)
        self.shield_slot = player_data.get('shield_slot', None)
        self.helmet_slot = player_data.get('helmet_slot', None)
        self.body_armor_slot = player_data.get('body_armor_slot', None)
        self.leg_armor_slot = player_data.get('leg_armor_slot', None)
        self.boots_slot = player_data.get('boots_slot', None)
        self.ring1_slot = player_data.get('ring1_slot', None)
        self.ring2_slot = player_data.get('ring2_slot', None)
        self.amulet_slot = player_data.get('amulet_slot', None)
        self.artifact1_slot = player_data.get('artifact1_slot', None)
        self.artifact2_slot = player_data.get('artifact2_slot', None)
        self.artifact3_slot = player_data.get('artifact3_slot', None)
        self.utility1_slot = player_data.get('utility1_slot', None)
        self.utility1_slot_quantity = player_data.get('utility1_slot_quantity', None)
        self.utility2_slot = player_data.get('utility2_slot', None)
        self.utility2_slot_quantity = player_data.get('utility2_slot_quantity', None)
        self.bag_slot = player_data.get('bag_slot', None)
        self.task = player_data.get('task', None)
        self.task_type = player_data.get('task_type', None)
        self.task_progress = player_data.get('task_progress', None)
        self.task_total = player_data.get('task_total', None)
        self.inventory_max_items = player_data.get('inventory_max_items', None)
        self.inventory = player_data.get('inventory', None)
