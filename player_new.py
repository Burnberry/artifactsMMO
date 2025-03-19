import threading, datetime
from time import sleep
from typing import Optional

from data_wrappers.data_manager import *
from goal_new import Goal, GoalManager
from helpers import *
from player_base import _PlayerAPI
from private.config import config


class Player(_PlayerAPI):
    players = {}
    noppe: 'Player' = None
    rubius: 'Player' = None
    pebbleboy: 'Player' = None
    leandra: 'Player' = None
    hekate: 'Player' = None

    player_lock = threading.Lock()

    reserved_stock: dict[Item:int] = {}

    def __init__(self, data):
        super().__init__(data)
        self.add_player(self)
        self.role = config.get('players').get(self.name, {}).get('role', '')
        self.goal: Goal = None
        self.thread = None
        self.has_lock = False

    def __repr__(self):
        return self.name

    def start_thread(self):
        self.thread = threading.Thread(target=self.goal_loop)
        self.thread.start()

    def stop_thread(self):
        pass

    def goal_loop(self):
        while True:
            GoalManager.perform(self)

    @staticmethod
    def add_player(player):
        setattr(Player, player.name.lower(), player)
        Player.players[player.name] = player

    def lock_acquire(self):
        self.player_lock.acquire()
        self.has_lock = True

    def lock_release(self):
        if self.has_lock:
            self.player_lock.release()
            self.has_lock = False

    def _action(self, path, data=None):
        self.__action(path, data)

        if 'application/json' in self.response.headers.get('Content-Type', ''):
            if 'data' in self.response.json():
                data = self.response.json()['data']
                if 'character' in data:
                    self.set_data(data['character'])
                if 'bank' in data:
                    self.bank.set_data(data['bank'])

    def __action(self, path, data=None):
        self.lock_release()
        cooldown = self.get_cooldown_time()
        if cooldown > 0:
            sleep(cooldown)
        super()._action(path, data)
        if not self.handle_response(path, data):
            return False
        if self.response.status_code != 200:
            cdwn = 0.1
            while self.response.status_code == 499:
                sleep(cdwn)
                cdwn += 1
        self.log()
        self.lock_acquire()

    def handle_response(self, path, data):
        cdwn = 0.1
        while self.response.status_code == 499:
            sleep(cdwn)
            super()._action(path, data)
            cdwn += 1
        if self.response.status_code == 200:
            return True
        print(self, self.response.status_code, path, data, self.response.content)
        raise Exception("Woopsie")

    def log(self):
        pass

    def set_goal(self, goal):
        if goal is not self.goal:
            self.goal = goal
            if goal:
                print('%s: %s' % (self.name, self.goal))

    # helper getters
    def stock_on_hand(self, item):
        return self.inventory.get(item, 0)

    @staticmethod
    def stock_in_bank(item):
        return Player.bank.inventory.get(item, 0)

    @staticmethod
    def stock_reserved(item):
        return Player.reserved_stock.get(item, 0)

    def stock_available(self, item):
        return self.stock_on_hand(item) + self.stock_in_bank(item) - self.stock_reserved(item)

    def items_available(self, items):
        for item, qty in items:
            if self.stock_available(item) < qty:
                return False
        return True

    def items_on_hand(self, items):
        for item, qty in items:
            if self.stock_on_hand(item) < qty:
                return False
        return True

    def item_sets_available(self, items):
        return min([self.stock_available(item)//qty for item, qty in items])

    @staticmethod
    def stock_total(item):
        count = sum([player.stock_on_hand(item) for player in Player.players.values()])
        count += Player.stock_in_bank(item)
        return count

    @staticmethod
    def reserve(item, quantity=1):
        Player.reserved_stock[item] = quantity + Player.reserved_stock.get(item, 0)

    @staticmethod
    def reserve_items(items):
        for item, qty in items:
            Player.reserve(item, qty)

    @staticmethod
    def unreserve(item, quantity=1):
        Player.reserve(item, -quantity)

    @staticmethod
    def unreserve_items(items):
        for item, qty in items:
            Player.unreserve(item, qty)

    def get_highest_resource(self, skill):
        level = self.get_level(skill)
        dlvl, best_resource = level+1, None
        for resource in Resource.all():
            if resource.skill == skill and 0 <= level - resource.level < dlvl:
                if not resource.tile_content.is_active(self.get_server_time()):
                    continue
                dlvl = level - resource.level
                best_resource = resource
        return best_resource

    @staticmethod
    def get_total_gold():
        gold = sum([player.gold for player in Player.players.values()])
        gold += Player.bank.gold
        return gold

    def get_available_gold(self):
        return self.gold + self.bank.gold

    def on_bank(self):
        return self.tile_content is TileContent.bank

    @staticmethod
    def get_required_materials(items):
        materials = {}
        for item, n in items:
            for material, qty in item.craft.materials:
                materials[material] = qty*n + materials.get(material, 0)
        return materials

    # helper actions
    def withdraw_items(self, items):
        for item, qty in items:
            self.withdraw(item, qty)

    def deposit_all(self):
        items = [(item, quantity) for item, quantity in self.inventory.items()]
        return self.deposit_items(items)

    def deposit_items(self, items):
        for item, n in items:
            self.deposit(item, n)

    def deposit_any(self, quantity=1, keep_items=None):
        keep_items = keep_items or {}
        items = []
        for item, qty in self.inventory.items():
            if item in keep_items:
                continue
            n = min(qty, quantity)
            quantity -= qty
            items.append((item, n))
            if quantity <= 0:
                break
        return self.deposit_items(items)

    def ensure_inventory_space(self, quantity=1, keep_items=None):
        if self.inventory_space >= quantity:
            return True
        self.deposit_any(quantity, keep_items)
        return True

    def ensure_items(self, items, reserve=True):
        items_to_get, keep_items = [], {}
        qty_total = 0
        for item, qty in items:
            qty -= self.stock_on_hand(item)
            if qty > 0:
                items_to_get.append((item, qty))
                qty_total += qty
                keep_items[item] = self.stock_on_hand(item)
        if not self.items_available(items):
            return False
        if reserve:
            self.reserve_items(items_to_get)
        self.ensure_inventory_space(qty_total, keep_items)
        self.withdraw_items(items_to_get)
        if reserve:
            self.unreserve_items(items_to_get)
        return True

    def fetch_and_equip(self, items):
        items = tuple_convert(items, (1, None))
        items_to_ensure = []
        for item, qty, slot in items:
            qty -= self.equipment.get_item_qty(item, slot)
            if qty >= 0:
                items_to_ensure.append((item, qty))
        self.ensure_items(items_to_ensure)
        for item, qty, slot in items:
            self.equip(item, slot, qty)

    def equip_best_tool(self, skill):
        if not hasattr(Effect, skill):
            return False
        effect = getattr(Effect, skill)
        items = Item.item_effect.get(effect)
        tools = []
        for item in items:
            if item.type == "weapon":
                tools.append(item)
        target_tool = None
        reduction = 0
        if has_weapon := (self.equipment.weapon_slot and self.equipment.weapon_slot.item):
            target_tool = self.equipment.weapon_slot.item
            reduction = target_tool.effects.get(effect, 0)
        for tool in tools:
            r = -tool.effects.get(effect)
            if self.stock_available(tool) and r > reduction and tool.level <= self.level:
                reduction, target_tool = r, tool
        if has_weapon and self.equipment.weapon_slot.item is target_tool:
            return True

        self.ensure_items([(target_tool, 1)])
        if has_weapon:
            self.unequip("weapon")
        self.equip(target_tool)

    def equip_gear_effect(self, effect):
        slot_types = self.equipment.get_slot_types()
        for slot_type in slot_types:
            if slot_type in ["utility", "weapon"]:
                continue
            if slot_type == "artifact":
                self.equip_slot_effect(slot_type, effect, 1)
                self.equip_slot_effect(slot_type, effect, 2)
                self.equip_slot_effect(slot_type, effect, 3)
            elif slot_type == "ring":
                self.equip_slot_effect(slot_type, effect, 1)
                self.equip_slot_effect(slot_type, effect, 2)
            else:
                self.equip_slot_effect(slot_type, effect)

    def equip_slot_effect(self, slot_type, effect, slot=None):
        slot_name = slot_type
        if slot:
            slot_name += str(slot)
        slot_name += "_slot"

        items = Item.item_effect.get(effect)
        gear_items = []
        for item in items:
            if item.type == slot_type:
                gear_items.append(item)
        target_gear, score = None, 0
        for gear in gear_items:
            if self.stock_available(gear) > 0 and gear.level <= self.level and gear.effects.get(effect, 0) > score:
                target_gear = gear
                score = gear.effects.get(effect, 0)

        if self.equipment and getattr(self.equipment, slot_name):
            gear = getattr(self.equipment, slot_name).item
            if gear.effects.get(effect, 0) >= score:
                return

        if target_gear:
            self.fetch_and_equip([(target_gear, 1, slot)])

    def heal(self, allow_overflow=True):
        heal_item = None
        heal_value = 1>>31
        for item in self.inventory:
            heal = item.effects.get(Effect.heal, 0)
            if heal > 0 and item.level <= self.level:
                if heal <= self.hp_missing:
                    heal_item = item
                    break
                elif allow_overflow and heal_value < heal:
                    heal_item = item
                    heal_value = heal

        if heal_item:
            self.use(heal_item)
            return True
        return False

    def ensure_healing(self, n):
        for item in self.inventory:
            if Effect.heal in item.effects:
                return True
        items_to_get = []
        for item in [Item.cooked_gudgeon, Item.cheese, Item.apple_pie, Item.cooked_salmon, Item.cooked_bass, Item.cooked_trout, Item.cooked_shrimp]:
            if item.level > self.level:
                continue
            qty_to_get = min(n, self.stock_available(item))
            items_to_get.append((item, qty_to_get))
            n -= qty_to_get
            if n <= 0:
                break
        self.ensure_items(items_to_get)

    def ensure_utilities(self, item, qty, slot=1):
        if slot == 1:
            equipment_slot = self.equipment.utility1_slot
        else:
            equipment_slot = self.equipment.utility2_slot
        if equipment_slot and equipment_slot.item is item and equipment_slot.quantity >= qty:
            return True
        self.fetch_and_equip([(item, 100, slot)])

    def craft_items(self, items: list[tuple[Item, int]]):
        required_materials = self.get_required_materials(items)
        for item, quantity in items:
            while quantity > 0:
                qty_to_craft = min(quantity, self.inventory_max_items // item.craft.material_count)
                items_to_ensure = [(material, qty*qty_to_craft) for material, qty in item.craft.materials]
                self.ensure_items(items_to_ensure, reserve=False)
                self.move(TileContent.get(item.craft.skill).tiles)
                self.crafting(item, qty_to_craft)
                quantity -= qty_to_craft

    # goal perform logic (partial action)
    def perform_gather(self, resource):
        if not self.equip_best_tool(resource.skill):
            return True
        if self.inventory_space <= 0:
            return self.deposit_all()
        if not self.move(resource.tile_content.tiles):
            return True
        return self.gather(resource)

    def perform_craft(self, item, recycle=False, batch=False):
        n = self.item_sets_available(item.craft.materials)
        n = min(n, self.inventory_max_items // item.craft.material_count)
        if not self.items_on_hand(item.craft.materials):
            items = [(mat, n*qty) for mat, qty in item.craft.materials]
            self.ensure_items(items)
        if not self.move(TileContent.get(item.craft.skill).tiles):
            return True
        if not batch:
            n = 1
        self.craft_items([(item, n)])
        if recycle:
            self.recycling(item, n)

    def perform_fight(self, monster, utility=None):
        if self.inventory_space <= 0:
            return self.deposit_all()

        if utility and not self.ensure_utilities(utility, 15):
            return True

        hp_trigger = 160
        if self.name == "Rubius" and monster.level >= 15:
            hp_trigger = 50
        while self.hp_missing >= hp_trigger:
            self.ensure_healing(70)
            return self.heal(allow_overflow=True)

        if not self.move(monster.tile_content.tiles):
            return True

        return self.fight()

    def perform_monster_task(self, max_level):
        if not self.task:
            self.task_new(TileContent.monsters)
            # temp
            if self.name == "Noppe" and self.task.level <= max_level:
                self.temp_equip_best_armor(self.task.monster)
        if self.name == "Rubius":
            if self.equipment.weapon_slot.item is not Item.multislimes_sword:
                self.fetch_and_equip([Item.multislimes_sword])
        if self.task.level > max_level:
            return self.task_cancel()
        if self.task_total > self.task_progress:
            return self.perform_fight(self.task.monster)
        self.task_complete(TileContent.monsters)

    # temp code
    def temp_equip_best_armor(self, monster):
        res = min([monster.res_water, monster.res_fire, monster.res_earth])
        if monster.res_earth == res:
            return self.temp_equip_earth()
        elif monster.res_fire == res:
            return self.temp_equip_fire()
        else:
            return self.temp_equip_water()

    def temp_equip_water(self):
        self.fetch_and_equip([Item.steel_armor, Item.steel_legs_armor, Item.dreadful_amulet, Item.battlestaff, (Item.water_ring, 1, 1), (Item.water_ring, 1, 2)])

    def temp_equip_earth(self):
        self.fetch_and_equip([Item.steel_armor, Item.steel_legs_armor, Item.dreadful_amulet, Item.wooden_club, (Item.earth_ring, 1, 1), (Item.earth_ring, 1, 2)])

    def temp_equip_fire(self):
        self.fetch_and_equip([(Item.skull_staff, 1), (Item.skeleton_armor, 1), (Item.skeleton_pants, 1), (Item.skull_amulet, 1), (Item.fire_ring, 1, 1), (Item.fire_ring, 1, 2)])

    def temp_equip_rubius(self):
        self.fetch_and_equip([(Item.iron_sword, 1), (Item.forest_ring, 1, 1), (Item.forest_ring, 1, 2), (Item.fire_and_earth_amulet, 1), Item.adventurer_vest])


def create_players():
    for data in Player.get_player_data():
        Player(data)


def setup_players():
    targets = [Player.get_status, Player.get_bank_details, Player.get_bank_item_data, Player.get_active_event_data, create_players]
    threads = [threading.Thread(target=target) for target in targets]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
