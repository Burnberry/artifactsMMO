from data_wrappers.Craft import Craft
from data_wrappers.Drops import Drops
from data_wrappers.items import Items
from data_wrappers.monsters import Monsters
from data_wrappers.resources import Resources
from data_wrappers.npcs import Npcs
from data_wrappers.tile_content import TileContent
from data_wrappers.tile_grid import Grid
from data_wrappers.drop import Drop
from data_wrappers.tasks import Tasks
from data_wrappers.npc_item import NpcItem
from data_wrappers.data.task_reward_data import task_reward_data


def manage_data():
    """Map item crafts to items"""
    for code, item in Items.items.items():
        if not item.craft:
            continue
        materials = [(Items.get_item(mat['code']), mat['quantity']) for mat in item.craft['items']]
        item.craft = Craft(item.craft, item, materials)
        item.craft.update_material_count()

    """Add task reward data as drop to task coin"""
    Items.tasks_coin.drops = Drops([vals for vals in task_reward_data.values()], Items.tasks_coin)

    """Map drops to items"""
    for drop in Drop.drops:
        drop.item = Items.get_item(drop.code)

    """Set main item on resources"""
    for _, resource in Resources.resources.items():
        resource.set_main_item()

    """Create tile contents and map tiles lists"""
    for key, content in Grid.tile_contents.items():
        if content.type == 'monster':
            content.monster = Monsters.monsters.get(content.code, None)
            content.monster.tile_content = content
        elif content.type == 'resource':
            content.resource = Resources.resources.get(content.code, None)
            content.resource.tile_content = content
        elif content.type == 'npc':
            content.npc = Npcs.npcs.get(content.code, None)
            content.npc.tile_content = content

    """Set tiles in tile_content & resource"""
    for _, tile in Grid.tiles.items():
        if not tile.content:
            continue
        code = tile.content['code']
        content = TileContent.get_tile_content(code)
        content.tiles.append(tile)
        if content.resource:
            content.resource.tiles.append(tile)

    """Map items and monsters on Task"""
    for code, task in Tasks.tasks.items():
        if task.type == 'items':
            task.item = Items.get_item(code)
        elif task.type == 'monsters':
            task.monster = Monsters.get_monster(code)

    """Map npc items to npc and items"""
    for npc_item in NpcItem.npc_items.values():
        npc_item: NpcItem
        npc_item.item = Items.get_item(npc_item.code)
        npc_item.item.npc_item = npc_item
        npc_item.npc = Npcs.npcs.get(npc_item.npc)
        npc_item.npc.items.append(npc_item)


manage_data()
