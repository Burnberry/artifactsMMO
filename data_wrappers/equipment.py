from data_wrappers.item import _Item, Item
from typing import Optional


class EquipmentSlot:
    def __init__(self, item: _Item, quantity=1):
        self.item = item
        self.slot = item.type
        self.quantity = quantity

    def __repr__(self):
        return "%s %sx" % (self.item, self.quantity)


class Equipment:
    def __init__(self, data):
        self.weapon_slot: EquipmentSlot = None
        self.rune_slot: EquipmentSlot = None
        self.shield_slot: EquipmentSlot = None
        self.helmet_slot: EquipmentSlot = None
        self.body_armor_slot: EquipmentSlot = None
        self.leg_armor_slot: EquipmentSlot = None
        self.boots_slot: EquipmentSlot = None
        self.ring1_slot: EquipmentSlot = None
        self.ring2_slot: EquipmentSlot = None
        self.amulet_slot: EquipmentSlot = None
        self.artifact1_slot: EquipmentSlot = None
        self.artifact2_slot: EquipmentSlot = None
        self.artifact3_slot: EquipmentSlot = None
        self.utility1_slot: EquipmentSlot = None
        self.utility2_slot: EquipmentSlot = None
        self.bag_slot: EquipmentSlot = None

        if data.get('weapon_slot', False):
            self.weapon_slot = EquipmentSlot(Item.get(data['weapon_slot']))
        if data.get('rune_slot', False):
            self.rune_slot = EquipmentSlot(Item.get(data['rune_slot']))
        if data.get('shield_slot', False):
            self.shield_slot = EquipmentSlot(Item.get(data['shield_slot']))
        if data.get('helmet_slot', False):
            self.helmet_slot = EquipmentSlot(Item.get(data['helmet_slot']))
        if data.get('body_armor_slot', False):
            self.body_armor_slot = EquipmentSlot(Item.get(data['body_armor_slot']))
        if data.get('leg_armor_slot', False):
            self.leg_armor_slot = EquipmentSlot(Item.get(data['leg_armor_slot']))
        if data.get('boots_slot', False):
            self.boots_slot = EquipmentSlot(Item.get(data['boots_slot']))
        if data.get('ring1_slot', False):
            self.ring1_slot = EquipmentSlot(Item.get(data['ring1_slot']))
        if data.get('ring2_slot', False):
            self.ring2_slot = EquipmentSlot(Item.get(data['ring2_slot']))
        if data.get('amulet_slot', False):
            self.amulet_slot = EquipmentSlot(Item.get(data['amulet_slot']))
        if data.get('artifact1_slot', False):
            self.artifact1_slot = EquipmentSlot(Item.get(data['artifact1_slot']))
        if data.get('artifact2_slot', False):
            self.artifact2_slot = EquipmentSlot(Item.get(data['artifact2_slot']))
        if data.get('artifact3_slot', False):
            self.artifact3_slot = EquipmentSlot(Item.get(data['artifact3_slot']))
        if data.get('utility1_slot', False):
            self.utility1_slot = EquipmentSlot(Item.get(data['utility1_slot']), data['utility1_slot_quantity'])
        if data.get('utility2_slot', False):
            self.utility2_slot = EquipmentSlot(Item.get(data['utility2_slot']), data['utility2_slot_quantity'])
        if data.get('bag_slot', False):

            self.bag_slot = EquipmentSlot(Item.get(data['bag_slot']))

    def __repr__(self):
        return "Equipment"
