from typing import Optional

from data_wrappers.achievement import Achievement, _Achievement
from data_wrappers.badge import Badge, _Badge
from data_wrappers.craft import Craft
from data_wrappers.drop import Drops, Drop
from data_wrappers.effect import Effect, _Effect
from data_wrappers.event import Event, _Event
from data_wrappers.item import Item, _Item
from data_wrappers.monster import Monster, _Monster
from data_wrappers.npc import Npc, _Npc
from data_wrappers.npc_item import NpcItem, _NpcItem
from data_wrappers.resource import Resource, _Resource
from data_wrappers.task import Task, _Task
from data_wrappers.data.task_reward_data import task_reward_data
from data_wrappers.tile_content import TileContent, _TileContent
from data_wrappers.tile_grid import Grid
from data_wrappers.equipment import Equipment, EquipmentSlot
from data_wrappers.bank import Bank
from data_wrappers.skill import Skill


def manage_data():
    """Map item crafts to items and whether item is material"""
    for item in Item.all():
        if not item.craft:
            continue
        materials = [(Item.get(mat['code']), mat['quantity']) for mat in item.data['craft']['items']]
        item.craft = Craft(item.craft, item, materials)
        item.craft.update_material_count()
        for material, _ in materials:
            material.is_material = True

    """Add task reward data as drop to task coin"""
    Item.tasks_coin.drops = Drops(task_reward_data, Item.tasks_coin)

    """Map drops to items"""
    for drop in Drop.drops:
        drop.item = Item.get(drop.code)

    """Set main item on resources"""
    for resource in Resource.all():
        resource.set_main_item()

    """Create tile contents and map tiles lists"""
    for content in Grid.all():
        if content.type == 'monster':
            content.monster = Monster.get(content.code)
            content.monster.tile_content = content
        elif content.type == 'resource':
            content.resource = Resource.get(content.code)
            content.resource.tile_content = content
        elif content.type == 'npc':
            content.npc = Npc.get(content.code)
            content.npc.tile_content = content

    """Set tiles in tile_content & resource"""
    Grid.set_main_tiles()

    """Map items and monsters on Task"""
    for task in Task.all():
        if task.type == 'items':
            task.item = Item.get(task.code)
        elif task.type == 'monsters':
            task.monster = Monster.get(task.code)

    """Map npc items to npc and items"""
    for npc_item in NpcItem.all():
        npc_item.item = Item.get(npc_item.code)
        npc_item.item.npc_item = npc_item
        npc_item.npc = Npc.get(npc_item.npc)
        npc_item.npc.items.append(npc_item)

    """Set effects on items"""
    Item.item_effect = {effect: [] for effect in Effect.all()}
    for item in Item.all():
        for effect in item.data.get('effects', []):
            item.effects[Effect.get(effect['code'])] = effect['value']
            Item.item_effect[Effect.get(effect['code'])].append(item)


manage_data()
