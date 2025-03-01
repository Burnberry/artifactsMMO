from data.items import Items
from data.monsters import Monsters
from data.resources import Resources
from data.npcs import Npcs
from data.tile_content import TileContent
from data.tile_grid import Grid
from data.drop import Drop

"""Map item crafts to items"""
# todo should be craft class
for code, item in Items.items.items():
    if not item.craft:
        continue
    materials = [(Items.get_item(mat['code']), mat['quantity']) for mat in item.craft['items']]
    item.craft = (item.craft['level'], item.craft['skill'], materials)

"""Map drops to items"""
for drop in Drop.drops:
    drop.item = Items.get_item(drop.code)

"""Set main item on resources"""
for _, resource in Resources.resources.items():
    resource.set_main_item()

"""Create tile contents"""
for key, content in Grid.tile_contents.items():
    if content.type == 'monster':
        content.monster = Monsters.monsters.get(content.code, None)
    elif content.type == 'resource':
        content.resource = Resources.resources.get(content.code, None)
    elif content.type == 'npc':
        content.npc = Npcs.npcs.get(content.code, None)

"""Set tiles in tile_content & resource"""
for _, tile in Grid.tiles.items():
    if not tile.content:
        continue
    code = tile.content['code']
    content = TileContent.get_tile_content(code)
    content.tiles.append(tile)
    if content.resource:
        content.resource.tiles.append(tile)
