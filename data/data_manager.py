from data.Craft import Craft
from data.items import Items, Item
from data.monsters import Monsters, Monster
from data.resources import Resources, Resource
from data.npcs import Npcs, Npc
from data.tile_content import TileContent
from data.tile_grid import Grid
from data.drop import Drop
from data.tasks import Tasks, Task


def manage_data():
    """Map item crafts to items"""
    for code, item in Items.items.items():
        if not item.craft:
            continue
        materials = [(Items.get_item(mat['code']), mat['quantity']) for mat in item.craft['items']]
        item.craft = Craft(item.craft, item, materials)

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


manage_data()
