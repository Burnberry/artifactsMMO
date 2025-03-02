import requests, threading, datetime
from time import sleep

from data.data_manager import *
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
        self.server_drift = None
        self.last_server_sync = None
        self.sync_server()

    def script_main(self):
        print("No main script made for", self.name)

    def recycle_loop(self, item, location, quantity=1):
        # todo improve
        self.deposit_all()
        self.withdraw(item, quantity)
        self.move(*location)
        self.recycle(item, quantity)

    def craft_items(self, items: list[Item, int]):
        required_materials = self.get_required_crafting_materials(items)
        gather_materials = not self.is_carrying_items(required_materials)

        for item, quantity in items:
            while quantity > 0:
                qty_to_craft = quantity
                if gather_materials:
                    self.deposit_all()
                    qty_to_craft = self.inventory_max_items//item.craft.material_count
                    for material, qty in item.craft.materials:
                        self.withdraw(material, qty*qty_to_craft)
                tiles = Grid.tile_contents.get(item.craft.skill).tiles
                self.move(tiles=tiles)
                self.craft(item, qty_to_craft)
                quantity -= qty_to_craft

    def get_required_crafting_materials(self, items: list[Item, int]):
        required_materials = {}
        for item, qty in items:
            for material, quantity in item.craft.materials:
                required_materials[material] = quantity*qty + required_materials.get(material, 0)
        return required_materials

    def is_carrying_items(self, items: dict):
        for item, qty in items.items():
            if self.inventory.get(item, 0) < qty:
                return False
        return True

    def craft_loop(self, item, location, quantity=2**32):
        # todo improve to handle more recipes + level/location checks
        bank_data = self.get_bank_data()
        level, skill, materials = item.craft
        mat_qty = sum([qty for mat, qty in materials])
        mats = {mat: (bank_data.get(mat, 0), qty) for (mat, qty) in materials}
        for mat, (stock, qty) in mats.items():
            quantity = min(quantity, stock//qty)

        while quantity > 0:
            self.deposit_all()
            qty_to_craft = min(quantity, self.inventory_max_items//mat_qty)
            print("crafting: %s, batch: %s, quantity: %s" % (item.name, qty_to_craft, quantity))
            for mat, (stock, qty) in mats.items():
                self.withdraw(mat, qty*qty_to_craft)
            self.move(*location)
            self.craft(item, qty_to_craft)
            quantity -= qty_to_craft

    def craft_one(self, item, location, equip=False):
        level, skill, materials = item.craft
        for mat, qty in materials:
            self.withdraw(mat, qty)
        self.move(*location)
        self.craft(item)
        if equip:
            self.equip(item)

    def equip(self, item, quantity=1, slot=None):
        slot = slot or item.type
        if getattr(self, "%s_slot" % slot):
            self.unequip(slot)
        self.action("action/equip", {'code': item.code, 'slot': slot, 'quantity': quantity})

    def unequip(self, slot, quantity=1):
        self.action("action/unequip", {'slot': slot, 'quantity': quantity})

    def use(self, item, quantity=1):
        self.action("action/use", {'code': item.code, 'quantity': quantity})

    def fight(self):
        self.action("action/fight")

    def withdraw(self, item, quantity=1):
        self.move(Grid.bank.tiles)
        self.action("action/bank/withdraw", {'code': item.code, 'quantity': quantity})

    def recycle(self, item, quantity=1):
        self.action("action/recycling", {'code': item.code, 'quantity': quantity})

    def craft(self, item, quantity=1):
        self.action("action/crafting", {'code': item.code, 'quantity': quantity})

    def get_task(self, code):
        if code == "items":
            self.move(tiles=Grid.items.tiles)
        elif code == "monsters":
            self.move(tiles=Grid.monsters.tiles)
        else:
            print("Invalid task code:", code)
            return
        if not self.task:
            self.action("action/task/new")

    def turn_in_items(self, item, quantity):
        self.move(Grid.items.tiles)
        self.action("action/task/trade", {"code": item.code, "quantity": quantity})

    def complete_task(self):
        if self.task:
            self.get_task(self.task.type)
            self.action("action/task/complete")

    def gather_loop(self, skill):
        while self.auto:
            if self.inventory_count >= self.inventory_max_items:
                self.deposit_all()
            else:
                self.gather(self.get_highest_resource(skill))

    def get_highest_resource(self, skill):
        level = self.get_level(skill)
        dx, best_resource = level+100, None
        for _, resource in Resources.resources.items():
            if resource.skill == skill and 0 <= level - resource.level < dx:
                dx = level - resource.level
                best_resource = resource
        return best_resource

    def get_level(self, skill):
        return getattr(self, skill+"_level")

    def gather(self, resource):
        self.move(resource=resource)
        self.action("action/gathering")

    def deposit_all(self):
        for item, quantity in self.inventory.items():
            self.deposit(item, quantity)

    def deposit(self, item, quantity):
        self.move(tiles=Grid.bank.tiles)
        self.action("action/bank/deposit", {'code': item.code, 'quantity': quantity})

    def move(self, tiles=None, x=None, y=None, resource=None):
        if x is None or y is None:
            x, y = self.x, self.y
        if resource and resource.tiles:
            tiles = resource.tiles
        if tiles:
            tile = self.get_closest_tile(tiles)
            x, y = tile.x, tile.y

        self._move(x, y)

    def _move(self, x, y):
        if self.x != x or self.y != y:
            self.action("action/move", {'x': x, 'y': y})

    def get_closest_tile(self, tiles):
        x, y = self.x, self.y
        closest_tile = None
        distance = 2**31
        for tile in tiles:
            d = abs(tile.x - x) + abs(tile.y - y)
            if d < distance:
                closest_tile, distance = tile, d
        return closest_tile

    def action(self, path, data=None):
        self.sync_server()
        cooldown = self.get_cooldown_time()
        if cooldown > 0:
            sleep(cooldown)
        self.response = requests.post(self.base_path+path, json=data, headers=headers)
        if self.response.status_code != 200:
            print(self.name, path, data, self.response.json())
        data = self.response.json()['data']
        if 'character' in data:
            self.set_player_data(data['character'])

    def sync_server(self):
        if not self.last_server_sync:
            response = requests.get(url, headers=headers)
            time = datetime.datetime.now()
            server_time = to_datetime(response.json()['data']['server_time'])
            self.server_drift = server_time - time
            self.last_server_sync = time

    @staticmethod
    def get_request(path, data=None):
        if not data:
            data = {}
        return requests.get(url + path, headers=headers, params=data)

    @staticmethod
    def get_all_data(path):
        data = []
        page, pages = 0, 1
        while page < pages:
            page += 1
            sleep(0.2)
            response = Player.get_request(path, {'page': page})
            content = response.json()
            pages = content['pages']
            data += content['data']
        return data

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
    def get_bank_data():
        data = Player.get_all_data("/my/bank/items")
        return {Items.get_item(item['code']): item['quantity'] for item in data}


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

    def get_cooldown_time(self):
        simple = False
        if simple:
            cooldown = self.cooldown
        else:
            cooldown_time = to_datetime(self.cooldown_expiration) - (datetime.datetime.now() + self.server_drift)
            cooldown = cooldown_time.days*24*60*60 + cooldown_time.seconds + cooldown_time.microseconds/10**6
        return cooldown

    def set_player_data(self, player_data):
        self._set_player_data(player_data)
        self.inventory_count = 0
        inventory = {}
        for slot in self.inventory:
            if not slot['code']:
                continue
            inventory[Items.get_item(slot['code'])] = slot['quantity']
            self.inventory_count += slot['quantity']
        self.inventory = inventory
        if self.task:
            self.task = Task.get_task(self.task)

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
