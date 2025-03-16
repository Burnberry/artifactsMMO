import datetime
import threading

import requests

from data_wrappers.data_manager import *
from data_wrappers.item import _Item
from helpers import *
from typing import Optional, TYPE_CHECKING


class _Player:
    bank: Bank = None
    server_drift: datetime.timedelta = None
    player_lock = threading.Lock()

    def __init__(self, data):
        self.data = data
        self.inventory_item_count = 0
        self.inventory_space = 0
        self.inventory: dict[_Item: int] = {}
        self.task: Task = None
        self.tile_content: TileContent = None

        self.set_data(data)

    def set_data(self, data):
        self.data = data
        self._set_data(data)

        # player inventory
        self.inventory_item_count = 0
        self.inventory = {}
        for slot in self.data.get('inventory', []):
            if slot.get('code', None):
                self.inventory[Item.get(slot['code'])] = slot['quantity']
                self.inventory_item_count += slot['quantity']
        self.inventory_space = self.inventory_max_items - self.inventory_item_count
        self.equipment: Equipment = Equipment(data)

        # other
        if self.task:
            self.task = Task.get(self.task)
        self.hp_missing = self.max_hp - self.hp
        if 'cooldown_expiration' in data:
            self.cooldown_expiration = to_datetime(self.cooldown_expiration)

    def get_level(self, skill):
        return getattr(self, skill+"_level")

    @staticmethod
    def _set_bank_data(data):
        if not _Player.bank:
            _Player.bank = Bank(data)
        else:
            _Player.bank.set_data(data)

    def get_cooldown_time(self):
        cooldown_time = self.cooldown_expiration - self.get_server_time()
        cooldown = cooldown_time.days * 24 * 60 * 60 + cooldown_time.seconds + cooldown_time.microseconds / 10 ** 6
        cooldown -= config.get("request_delay", 0)
        return cooldown

    @staticmethod
    def get_server_time():
        if _Player.server_drift:
            return datetime.datetime.now() + _Player.server_drift
        return datetime.datetime.now()

    @staticmethod
    def get_server_drift():
        return _Player.server_drift

    def _set_data(self, data):
        self.name = data.get('name', None)
        self.account = data.get('account', None)
        self.skin = data.get('skin', None)
        self.level = data.get('level', None)
        self.xp = data.get('xp', None)
        self.max_xp = data.get('max_xp', None)
        self.gold = data.get('gold', None)
        self.speed = data.get('speed', None)
        self.mining_level = data.get('mining_level', None)
        self.mining_xp = data.get('mining_xp', None)
        self.mining_max_xp = data.get('mining_max_xp', None)
        self.woodcutting_level = data.get('woodcutting_level', None)
        self.woodcutting_xp = data.get('woodcutting_xp', None)
        self.woodcutting_max_xp = data.get('woodcutting_max_xp', None)
        self.fishing_level = data.get('fishing_level', None)
        self.fishing_xp = data.get('fishing_xp', None)
        self.fishing_max_xp = data.get('fishing_max_xp', None)
        self.weaponcrafting_level = data.get('weaponcrafting_level', None)
        self.weaponcrafting_xp = data.get('weaponcrafting_xp', None)
        self.weaponcrafting_max_xp = data.get('weaponcrafting_max_xp', None)
        self.gearcrafting_level = data.get('gearcrafting_level', None)
        self.gearcrafting_xp = data.get('gearcrafting_xp', None)
        self.gearcrafting_max_xp = data.get('gearcrafting_max_xp', None)
        self.jewelrycrafting_level = data.get('jewelrycrafting_level', None)
        self.jewelrycrafting_xp = data.get('jewelrycrafting_xp', None)
        self.jewelrycrafting_max_xp = data.get('jewelrycrafting_max_xp', None)
        self.cooking_level = data.get('cooking_level', None)
        self.cooking_xp = data.get('cooking_xp', None)
        self.cooking_max_xp = data.get('cooking_max_xp', None)
        self.alchemy_level = data.get('alchemy_level', None)
        self.alchemy_xp = data.get('alchemy_xp', None)
        self.alchemy_max_xp = data.get('alchemy_max_xp', None)
        self.hp = data.get('hp', None)
        self.max_hp = data.get('max_hp', None)
        self.haste = data.get('haste', None)
        self.critical_strike = data.get('critical_strike', None)
        self.wisdom = data.get('wisdom', None)
        self.prospecting = data.get('prospecting', None)
        self.attack_fire = data.get('attack_fire', None)
        self.attack_earth = data.get('attack_earth', None)
        self.attack_water = data.get('attack_water', None)
        self.attack_air = data.get('attack_air', None)
        self.dmg = data.get('dmg', None)
        self.dmg_fire = data.get('dmg_fire', None)
        self.dmg_earth = data.get('dmg_earth', None)
        self.dmg_water = data.get('dmg_water', None)
        self.dmg_air = data.get('dmg_air', None)
        self.res_fire = data.get('res_fire', None)
        self.res_earth = data.get('res_earth', None)
        self.res_water = data.get('res_water', None)
        self.res_air = data.get('res_air', None)
        self.x = data.get('x', None)
        self.y = data.get('y', None)
        self.cooldown = data.get('cooldown', None)
        self.cooldown_expiration = data.get('cooldown_expiration', None)
        self.weapon_slot = data.get('weapon_slot', None)
        self.rune_slot = data.get('rune_slot', None)
        self.shield_slot = data.get('shield_slot', None)
        self.helmet_slot = data.get('helmet_slot', None)
        self.body_armor_slot = data.get('body_armor_slot', None)
        self.leg_armor_slot = data.get('leg_armor_slot', None)
        self.boots_slot = data.get('boots_slot', None)
        self.ring1_slot = data.get('ring1_slot', None)
        self.ring2_slot = data.get('ring2_slot', None)
        self.amulet_slot = data.get('amulet_slot', None)
        self.artifact1_slot = data.get('artifact1_slot', None)
        self.artifact2_slot = data.get('artifact2_slot', None)
        self.artifact3_slot = data.get('artifact3_slot', None)
        self.utility1_slot = data.get('utility1_slot', None)
        self.utility1_slot_quantity = data.get('utility1_slot_quantity', None)
        self.utility2_slot = data.get('utility2_slot', None)
        self.utility2_slot_quantity = data.get('utility2_slot_quantity', None)
        self.bag_slot = data.get('bag_slot', None)
        self.task = data.get('task', None)
        self.task_type = data.get('task_type', None)
        self.task_progress = data.get('task_progress', None)
        self.task_total = data.get('task_total', None)
        self.inventory_max_items = data.get('inventory_max_items', None)
        self.inventory = data.get('inventory', None)


class _PlayerAPI(_Player):
    def __init__(self, data):
        super().__init__(data)
        self._action_url = url + "my/%s/action/" % self.name

    @staticmethod
    def get_request(path, data=None):
        if not data:
            data = {}
        return requests.get(url + path, headers=headers, params=data)

    @staticmethod
    def post_request(path, data=None):
        if not data:
            data = {}
        return requests.post(path, headers=headers, json=data)

    @staticmethod
    def get_all_data(path, parameters=None):
        parameters, data = parameters or {}, []
        page, pages = 0, 1
        while page < pages:
            page += 1
            parameters['page'] = page
            response = _PlayerAPI.get_request(path, parameters)
            content = response.json()
            pages = content.get('pages', 1)
            data += content['data']
        return data

    def _action(self, path, data=None):
        if path and path[0] == '/':
            path = path[1:]
        self.response = self.post_request(self._action_url + path, data=data)
        return self.response

    # Custom action logic
    def move(self, tiles, **kwargs):
        x, y = get_nearest_tiles(tiles, self.x, self.y)
        if x == self.x and y == self.y:
            return True
        return self._move(x, y)

    def rest(self):
        if self.max_hp <= self.hp:
            return False
        return self._rest()

    def use(self, item, quantity=1):
        return self._use(item.code, quantity)

    def gather(self, resource):
        self.move(resource.tile_content.tiles)
        return self._gathering()

    def crafting(self, item, quantity=1):
        return self._crafting(item.code, quantity)

    def equip(self, item, slot=None, quantity=1, add_quantity=None):
        slot_code = item.type
        if slot:
            slot_code += str(slot)
        slot: EquipmentSlot = getattr(self.equipment, "%s_slot" % slot_code)
        if slot and slot.item is item and not add_quantity:
            if slot.quantity == quantity:
                return True
            elif slot.quantity < quantity:
                return self._equip(item.code, slot_code, quantity-slot.quantity)
            elif slot.quantity > quantity:
                return self.unequip(slot_code, quantity - slot.quantity)
        if slot:
            self.unequip(slot_code, slot.quantity)
        if add_quantity:
            quantity = add_quantity
        return self._equip(item.code, slot_code, quantity)

    def deposit_gold(self, quantity=None):
        self.move(TileContent.bank.tiles)
        if not quantity:
            quantity = self.gold
        if quantity == 0:
            return True
        return self._deposit_gold(quantity)

    def deposit(self, item: Item, quantity=1):
        self.move(TileContent.bank.tiles)
        return self._deposit(item.code, quantity)

    def withdraw(self, item: Item, quantity=1):
        self.move(TileContent.bank.tiles)
        return self._withdraw(item.code, quantity)

    def withdraw_gold(self, quantity):
        self.move(TileContent.bank.tiles)
        return self._withdraw_gold(quantity)

    def buy_expansion(self):
        if self.gold < self.bank.next_expansion_cost:
            return False
        self.move(TileContent.bank.tiles)
        self._buy_expansion()

    def npc_buy(self, item: Item, quantity=1):
        return self._npc_buy(item.code, quantity)

    def npc_sell(self, item: Item, quantity=1):
        return self._npc_sell(item.code, quantity)

    def recycling(self, item: Item, quantity=1):
        return self._recycling(item.code, quantity)

    def task_complete(self, tile_content=None):
        if tile_content:
            tiles = tile_content.tiles
        else:
            tiles = TileContent.monsters.tiles + TileContent.items.tiles
        self.move(tiles)
        return self._task_complete()

    def task_exchange(self):
        tiles = TileContent.monsters.tiles + TileContent.items.tiles
        self.move(tiles)
        return self._task_exchange()

    def task_new(self, tile_content: TileContent):
        self.move(tile_content.tiles)
        return self._task_new()

    def task_cancel(self):
        tiles = TileContent.monsters.tiles + TileContent.items.tiles
        self.move(tiles)
        return self._task_cancel()

    def task_trade(self, item: Item, quantity=1):
        tiles = TileContent.monsters.tiles + TileContent.items.tiles
        self.move(tiles)
        return self._task_trade(item.code, quantity)

    def delete_item(self, item: Item, quantity=1):
        return self._delete_item(item.code, quantity)

    # Base Action requests, no extra logic added
    def _move(self, x, y):
        data = {'x': x, 'y': y}
        return self._action("move", data=data)

    def _rest(self):
        data = {}
        return self._action("rest", data=data)

    def _equip(self, code, slot, quantity):
        data = {'code': code, 'slot': slot, 'quantity': quantity}
        return self._action("equip", data=data)

    def unequip(self, slot, quantity=1):
        data = {'slot': slot, 'quantity': quantity}
        return self._action("unequip", data=data)

    def _use(self, code, quantity=1):
        data = {'code': code, 'quantity': quantity}
        return self._action("use", data=data)

    def fight(self):
        data = {}
        return self._action("fight", data=data)

    def _gathering(self):
        data = {}
        return self._action("gathering", data=data)

    def _crafting(self, code, quantity=1):
        data = {'code': code, 'quantity': quantity}
        return self._action("crafting", data=data)

    def _deposit_gold(self, quantity):
        data = {'quantity': quantity}
        return self._action("bank/deposit/gold", data=data)

    def _deposit(self, code, quantity=1):
        data = {'code': code, 'quantity': quantity}
        return self._action("bank/deposit", data=data)

    def _withdraw(self, code, quantity=1):
        data = {'code': code, 'quantity': quantity}
        return self._action("bank/withdraw", data=data)

    def _withdraw_gold(self, quantity):
        data = {'quantity': quantity}
        return self._action("bank/withdraw/gold", data=data)

    def _buy_expansion(self):
        data = {}
        return self._action("bank/buy_expansion", data=data)

    def _npc_buy(self, code, quantity=1):
        data = {'code': code, 'quantity': quantity}
        return self._action("npc/buy", data=data)

    def _npc_sell(self, code, quantity=1):
        data = {'code': code, 'quantity': quantity}
        return self._action("npc/sell", data=data)

    def _recycling(self, code, quantity=1):
        data = {'code': code, 'quantity': quantity}
        return self._action("recycling", data=data)

    def ge_buy(self, gid, quantity=1):
        data = {'id': gid, 'quantity': quantity}
        return self._action("grandexchange/buy", data=data)

    def ge_sell(self, code, price, quantity=1):
        data = {'code': code, 'price': price, 'quantity': quantity}
        return self._action("grandexchange/sell", data=data)

    def ge_cancel_sell(self, gid):
        data = {'gid': gid}
        return self._action("grandexchange/cancel", data=data)

    def _task_complete(self):
        data = {}
        return self._action("task/complete", data=data)

    def _task_exchange(self):
        data = {}
        return self._action("task/exchange", data=data)

    def _task_new(self):
        data = {}
        return self._action("task/new", data=data)

    def _task_trade(self, code, quantity=1):
        data = {'code': code, 'quantity': quantity}
        return self._action("task/trade", data=data)

    def _task_cancel(self):
        data = {}
        return self._action("task/cancel", data=data)

    def _delete_item(self, code, quantity=1):
        data = {'code': code, 'quantity': quantity}
        return self._action("delete", data=data)

    # Get requests, incomplete

    @staticmethod
    def get_status():
        response = _PlayerAPI.get_request("/")
        if response.status_code == 200:
            time = datetime.datetime.now()
            server_time = to_datetime(response.json()['data']['server_time'])
            _Player.server_drift = server_time - time
        return response

    @staticmethod
    def get_bank_details():
        response = _PlayerAPI.get_request("/my/bank")
        _Player._set_bank_data(response.json().get('data'))
        return response

    @staticmethod
    def get_bank_item_data():
        data = _PlayerAPI.get_all_data("/my/bank/items")
        _Player._set_bank_data(data)
        return data

    @staticmethod
    def get_player_data():
        response = _PlayerAPI.get_request("/my/characters")
        return response.json().get('data', [])

    @staticmethod
    def get_achievement_data(account=None):
        if not account:
            account = config.get('account')
        return _PlayerAPI.get_all_data("/accounts/%s/achievements" % account)

    @staticmethod
    def get_active_event_data():
        data = _PlayerAPI.get_all_data("/events/active")
        TileContent.update_event_data(data)
        return data
