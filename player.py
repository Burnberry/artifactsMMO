import requests, threading, datetime
from time import sleep

from data_wrappers.data_manager import *
from goal_base import Goal
from helpers import *


class Player:
    players = set()
    player_lock = threading.Lock()
    bank_inventory = None
    server_drift = None

    def __init__(self, name, role):
        Player.add_player(self)
        self.name = name
        self.role = role
        self.base_path = url + "my/%s/" % self.name
        self.response = None
        self.get_character_data()
        self.auto = False
        self.thread = None
        self.has_lock = False
        self.last_server_sync = None
        self.action_time = datetime.datetime.now()
        self.goal: Goal = None
        self.sync_server()

    def __repr__(self):
        return self.name

    def set_goal(self, goal):
        if goal is not self.goal:
            self.goal = goal
            print('%s:' % self.name, self.goal)

    # Scripting
    def script_main(self):
        print("No main script made for", self.name)

    def equip_lvl1(self):
        if not self.weapon_slot:
            self.withdraw(Item.wooden_staff)
            self.equip(Item.wooden_staff)

    def equip_lvl5(self):
        if self.level >= 5 and self.weapon_slot == Item.wooden_staff.code:
            self.withdraw(Item.water_bow)
            self.equip(Item.water_bow)
            self.withdraw(Item.feather_coat)
            self.equip(Item.feather_coat)
            self.withdraw(Item.copper_legs_armor)
            self.equip(Item.copper_legs_armor)

    def equip_lvl10(self):
        if self.level >= 10 and self.weapon_slot == Item.water_bow.code and self.bank_inventory.get(Item.iron_sword, 0) > 0:
            self.withdraw(Item.iron_sword)
            self.equip(Item.iron_sword)

    def equip_lvl15(self):
        if self.level >= 15 and self.weapon_slot != Item.multislimes_sword and self.bank_inventory.get(Item.multislimes_sword, 0) > 0:
            self.ensure_equipment(Item.multislimes_sword)

    def fight_loop(self, monster, n):
        while n > 0:
            self.equip_lvl5()
            self.equip_lvl10()
            self.equip_lvl15()
            if self.inventory_max_items-4 <= self.inventory_count:
                self.deposit_all()
            if self.max_hp - self.hp >= 75:
                if self.inventory.get(Item.cooked_shrimp, 0) <= 0:
                    if not self.ensure_items([(Item.cooked_shrimp, 100)]):
                        return False
                else:
                    self.use(Item.cooked_shrimp, 1)
            else:
                self.move(monster.tile_content.tiles)
                self.fight()
                n -= 1
        return True

    def monster_task_loop(self):
        while True:
            if self.inventory_max_items - 4 <= self.inventory_count:
                self.deposit_all()
            if not self.task:
                self.get_task('monsters')
            max_level = 6
            if self.level >= 10:
                max_level = 7
            if self.level >= 15:
                max_level = 8

            while self.task.level > max_level:
                if not self.inventory.get(Item.tasks_coin, 0) > 0:
                    return False
                self.action("action/task/cancel")
                self.get_task('monsters')
            if not self.fight_loop(self.task.monster, self.task_total-self.task_progress):
                return
            self.complete_task()

    def starter_achievement_loop(self):
        achievements = [
            (Achievement.amateur_miner, Resource.copper_rocks),
            (Achievement.amateur_lumberjack, Resource.ash_tree),
            (Achievement.amateur_fisherman, Resource.gudgeon_fishing_spot),
            (Achievement.amateur_alchmist, Resource.sunflower_field),
        ]
        for achievement, resource in achievements:
            if achievement.current < achievement.total:
                n = (achievement.total - achievement.current)//4 + 1
                print(n)
                for _ in range(n):
                    self.gather_resource(resource)

    def main_skills_loop(self):
        resources = [Resource.copper_rocks, Resource.ash_tree, Resource.sunflower_field, Resource.gudgeon_fishing_spot]
        for resource in resources:
            while self.get_level(resource.skill) < 10:
                self.gather_resource(resource)

        while self.get_level(Item.cooked_gudgeon.craft.skill) < 10:
            self.craft_items([(Item.cooked_gudgeon, 100)])

    def craft_skill_batch(self, item, level):
        n = self.inventory_max_items//item.craft.material_count
        n = min(n, self.item_sets_available(item.craft.materials))
        self.ensure_items(item.craft.materials, n)

        print(self.name, "level crafting", n, item)
        while self.get_level(item.craft.skill) < level and n > 0:
            self.craft_items([(item, 1)])
            n -= 1

    def item_sets_available(self, items):
        n = 2**31
        for item, qty in items:
            n = min(n, self.get_available_qty(item)//qty)
        return n

    def on_hand(self, items):
        for item, qty in items:
            if self.inventory.get(item, 0) < qty:
                return False
        return True

    def get_available_qty(self, item):
        return self.bank_inventory.get(item, 0) + self.inventory.get(item, 0)

    def craft_skill_loop(self, item, level):
        skill = item.craft.skill

        while self.get_level(skill) < level:
            if self.ensure_items(item.craft.materials, self.inventory_max_items//item.craft.material_count):
                self.craft_items([(item, 1)])
                self.recycle(item, 1)
            else:
                return
                # material, _ = item.craft.materials[0]
                # n = self.inventory_max_items//material.craft.material_count
                # self.craft_items([(material, n)])

    def ensure_equipment(self, item, slot=None, quantity=None):
        slot = slot or item.type
        if getattr(self, "%s_slot" % slot) != item.code and self.bank_inventory.get(item, 0) > 0:
            self.withdraw(item)
            self.equip(item)

    def ensure_items(self, items, factor=None):
        items_to_get = []
        size = 0
        for item, n in items:
            x = n - self.inventory.get(item, 0)
            if x > 0:
                items_to_get.append((item, x))
                size += x
        for item, n in items_to_get:
            if self.bank_inventory.get(item, 0) < n:
                return False
        if size > self.inventory_max_items - self.inventory_count:
            self.deposit_all()  # can be optimized to keep required items
        if items_to_get and factor:
            for i in range(factor-1):
                res = self.ensure_items([(item, n * (factor-i)) for item, n in items])
                if res:
                    return res
            return self.ensure_items([(item, n * factor) for item, n in items])
        for item, n in items_to_get:
            self.withdraw(item, n)
        return True

    # helpers
    def craft_items(self, items: list[tuple[Item, int]]):
        required_materials = self.get_required_crafting_materials(items)
        gather_materials = not self.is_carrying_items(required_materials)

        for item, quantity in items:
            while quantity > 0:
                qty_to_craft = quantity
                if gather_materials:
                    self.deposit_all()
                    qty_to_craft = min(quantity, self.inventory_max_items//item.craft.material_count)
                    for material, qty in item.craft.materials:
                        self.withdraw(material, qty*qty_to_craft)
                tiles = Grid.tile_contents.get(item.craft.skill).tiles
                self.move(tiles=tiles)
                self.craft(item, qty_to_craft)
                quantity -= qty_to_craft

    @staticmethod
    def get_required_crafting_materials(items: list[tuple[Item, int]]):
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

    def get_available_items(self):
        return self.bank_inventory

    def equip(self, item, quantity=1, slot=None):
        slot = slot or item.type
        if hasattr(self, "%s_slot" % slot) and getattr(self, "%s_slot" % slot) and item is not Item.small_health_potion:
            self.unequip(slot)
        self.action("action/equip", {'code': item.code, 'slot': slot, 'quantity': quantity})

    def unequip(self, slot, quantity=1):
        self.action("action/unequip", {'slot': slot, 'quantity': quantity})

    def use(self, item, quantity=1):
        self.action("action/use", {'code': item.code, 'quantity': quantity})

    def fight(self):
        self.action("action/fight")

    def sell_npc_item(self, npc_item: NpcItem, quantity=1):
        self.move(npc_item.npc.tile_content.tiles)
        self.action("action/npc/sell", {'code': npc_item.item.code, 'quantity': quantity})

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

    def cancel_task(self):
        self.move(TileContent.monsters.tiles)
        self.action("action/task/cancel")

    def reroll_task(self):
        self.ensure_items([(Item.tasks_coin, 1)])
        self.cancel_task()
        self.get_task("monsters")

    def gather_resource(self, resource):
        if self.inventory_count >= self.inventory_max_items:
            self.deposit_all()
        self.gather(resource)

    def gather_loop(self, skill=None, resource_forced=None):
        resource = None
        while self.auto:
            if self.inventory_count >= self.inventory_max_items:
                self.deposit_all()
            else:
                if not resource_forced:
                    resource = self.get_highest_resource(skill)
                self.gather(resource or resource_forced)

    def gather_batch(self, arg):
        skill, resource = None, None
        if isinstance(arg, Resource):
            resource = arg
        elif hasattr(arg, 'resource'):
            resource = arg.resource
        else:
            skill = arg
        if self.inventory_count >= self.inventory_max_items:
            self.deposit_all()
        while self.inventory_count < self.inventory_max_items:
            if not self.gather(resource or self.get_highest_resource(skill)):
                return

    def get_highest_resource(self, skill):
        level = self.get_level(skill)
        dx, best_resource = level+100, None
        for _, resource in Resource.resources.items():
            # if self.name == 'Pebbleboy':
            #     if resource.skill == skill:
            #         print(resource, resource.tile_content.tiles, resource.tile_content.is_active(self.get_server_time()))
            if resource.skill == skill and 0 <= level - resource.level < dx:
                if not resource.tile_content.is_active(self.get_server_time()):
                    continue
                dx = level - resource.level
                best_resource = resource
        return best_resource

    def get_level(self, skill):
        return getattr(self, skill+"_level")

    def gather(self, resource):
        if resource.tile_content.is_active(self.get_server_time()):
            self.move(resource=resource)
        else:
            return False
        if resource.tile_content.is_active(self.get_server_time()):
            self.action("action/gathering")
            return True
        else:
            return False

    def deposit_all(self):
        for item, quantity in self.inventory.items():
            self.deposit(item, quantity)

    def deposit(self, item, quantity):
        self.move(tiles=Grid.bank.tiles)
        self.action("action/bank/deposit", {'code': item.code, 'quantity': quantity})

    def move(self, tiles=None, x=None, y=None, resource=None):
        if x is None or y is None:
            x, y = self.x, self.y
        if resource and resource.tile_content.tiles:
            tiles = resource.tile_content.tiles
        if tiles:
            x, y = self.get_closest_tile(tiles)

        self._move(x, y)

    def _move(self, x, y):
        if self.x != x or self.y != y:
            self.action("action/move", {'x': x, 'y': y})

    def get_closest_tile(self, tiles):
        x, y = self.x, self.y
        closest_tile = None
        distance = 2**31
        for tx, ty in tiles:
            d = abs(tx - x) + abs(ty - y)
            if d < distance:
                closest_tile, distance = (tx, ty), d
        return closest_tile

    def action(self, path, data=None):
        self.sync_server()

        self._action(path, data)

        if 'application/json' in self.response.headers.get('Content-Type', ''):
            if 'data' in self.response.json():
                data = self.response.json()['data']
                if 'character' in data:
                    self.set_player_data(data['character'])
                if 'bank' in data:
                    self.set_bank_data(data['bank'])

    def _action(self, path, data=None):
        self.lock_release()

        cooldown = self.get_cooldown_time()
        if cooldown > 0:
            sleep(cooldown)
        for i in range(5):
            self.response = requests.post(self.base_path + path, json=data, headers=headers)
            if self.response.status_code not in [200, 499]:
                print(self.name, path, data, self.response.json())
                sleep(0.01 + 0.1*i**2)
            else:
                break
            if i == 3:
                self._check_status_loop()
                print("status OK")
        # if self.name == "Noppe":
        #     self.log_time(path)
        if self.response.status_code != 200:
            if self.goal and hasattr(self.goal, "resource") and self.goal.resource.tile_content.is_event:
                self.goal.resource.tile_content.tiles = []
            else:
                return

        self.lock_acquire()

    def _check_status_loop(self):
        print("Checking status loop")
        while True:
            sleep(60)
            try:
                response = self.get_request("")
                if response.status_code == 200:
                    return
            except Exception as e:
                print(e)

    def log_time(self, msg):
        time = datetime.datetime.now()
        print(msg, time - self.action_time)
        self.action_time = time

    def sync_server(self):
        if not self.last_server_sync:
            response = requests.get(url, headers=headers)
            time = datetime.datetime.now()
            server_time = to_datetime(response.json()['data']['server_time'])
            Player.server_drift = server_time - time
            self.last_server_sync = time

    @staticmethod
    def get_request(path, data=None):
        if not data:
            data = {}
        return requests.get(url + path, headers=headers, params=data)

    @staticmethod
    def get_all_data(path):
        if path and path[0] == '/':
            path = path[1:]
        data = []
        page, pages = 0, 1
        while page < pages:
            page += 1
            response = Player.get_request(path, {'page': page})
            content = response.json()
            pages = content.get('pages', 1)
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

    def lock_acquire(self):
        self.player_lock.acquire()
        self.has_lock = True

    def lock_release(self):
        if self.has_lock:
            self.player_lock.release()
            self.has_lock = False

    @staticmethod
    def update_bank_data():
        data = Player.get_all_data("/my/bank/items")
        Player.set_bank_data(data)

    @staticmethod
    def update_event_data():
        event_data = Player.get_all_data("/events/active")
        for tile_content in TileContent.all():
            if tile_content.is_event:
                tile_content.tiles = []
        for event in event_data:
            tile = TileContent.get(event['map']['content']['code'])
            tile.tiles.append((event['map']['x'], event['map']['y']))
            tile.expiration = to_datetime(event['expiration'])

    @staticmethod
    def set_bank_data(data):
        bank_inventory = {}
        for vals in data:
            item = Item.get(vals['code'])
            bank_inventory[item] = vals["quantity"]
        Player.bank_inventory = bank_inventory

    @staticmethod
    def update_achievement_data():
        data = Player.get_all_data("/accounts/Burnberry/achievements")
        for vals in data:
            achievement = Achievement.get(vals['code'])
            achievement.current = vals['current']
            achievement.is_complete = vals['completed_at']

    @staticmethod
    def get_bank_stock(item):
        return Player.bank_inventory.get(item, 0)

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
            sleep(0.05)
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
            cooldown_time = to_datetime(self.cooldown_expiration) - self.get_server_time()
            cooldown = cooldown_time.days*24*60*60 + cooldown_time.seconds + cooldown_time.microseconds/10**6
            cooldown -= 0.30  # request transfer delay
        return cooldown

    @staticmethod
    def get_server_time():
        if Player.server_drift:
            return datetime.datetime.now() + Player.server_drift
        return datetime.datetime.now()

    def set_player_data(self, player_data):
        self._set_player_data(player_data)
        self.inventory_count = 0
        inventory = {}
        for slot in self.inventory:
            if not slot['code']:
                continue
            inventory[Item.get(slot['code'])] = slot['quantity']
            self.inventory_count += slot['quantity']
        self.inventory = inventory
        if self.task:
            self.task = Task.get(self.task)

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


Player.update_bank_data()
Player.update_achievement_data()
