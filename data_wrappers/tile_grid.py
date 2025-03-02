import json

from data_wrappers.tile import Tile
from data_wrappers.data.tile_data import tile_data
from data_wrappers.tile_content import TileContent
from data_wrappers.data.tile_content_data import tile_content_data


class Grid:
    tiles = {key: Tile(tile_data[key]) for key in tile_data}
    tile_contents: dict[str: TileContent] = TileContent.tile_contents

    @staticmethod
    def inside(x, y):
        return (x, y) in Grid.tiles

    @staticmethod
    def get_tile(x, y):
        return Grid.tiles[(x, y)]

    @staticmethod
    def print_tile_content_data():
        data = {}
        for key, tile in Grid.tiles.items():
            if not tile.content:
                continue
            data[tile.content['code']] = tile.content
        print(json.dumps(data, indent=4))

    @staticmethod
    def print_tile_content_code():
        data, key, name = {}, 'code', 'tile_content'
        for _, tile in Grid.tiles.items():
            if not tile.content:
                continue
            data[tile.content['code']] = tile.content
        class_name = "TileContent"
        data_name = name + "_data"
        for _, values in data.items():
            print("%s = %s(%s['%s'])" % (values[key], class_name, data_name, values[key]))

    salmon_fishing_spot = TileContent(tile_content_data['salmon_fishing_spot'])
    goblin_wolfrider = TileContent(tile_content_data['goblin_wolfrider'])
    orc = TileContent(tile_content_data['orc'])
    ogre = TileContent(tile_content_data['ogre'])
    pig = TileContent(tile_content_data['pig'])
    woodcutting = TileContent(tile_content_data['woodcutting'])
    gold_rocks = TileContent(tile_content_data['gold_rocks'])
    cyclops = TileContent(tile_content_data['cyclops'])
    blue_slime = TileContent(tile_content_data['blue_slime'])
    yellow_slime = TileContent(tile_content_data['yellow_slime'])
    red_slime = TileContent(tile_content_data['red_slime'])
    green_slime = TileContent(tile_content_data['green_slime'])
    goblin = TileContent(tile_content_data['goblin'])
    wolf = TileContent(tile_content_data['wolf'])
    ash_tree = TileContent(tile_content_data['ash_tree'])
    copper_rocks = TileContent(tile_content_data['copper_rocks'])
    bandit_lizard = TileContent(tile_content_data['bandit_lizard'])
    chicken = TileContent(tile_content_data['chicken'])
    cooking = TileContent(tile_content_data['cooking'])
    weaponcrafting = TileContent(tile_content_data['weaponcrafting'])
    gearcrafting = TileContent(tile_content_data['gearcrafting'])
    bank = TileContent(tile_content_data['bank'])
    grand_exchange = TileContent(tile_content_data['grand_exchange'])
    owlbear = TileContent(tile_content_data['owlbear'])
    cow = TileContent(tile_content_data['cow'])
    monsters = TileContent(tile_content_data['monsters'])
    sunflower_field = TileContent(tile_content_data['sunflower_field'])
    gudgeon_fishing_spot = TileContent(tile_content_data['gudgeon_fishing_spot'])
    shrimp_fishing_spot = TileContent(tile_content_data['shrimp_fishing_spot'])
    jewelrycrafting = TileContent(tile_content_data['jewelrycrafting'])
    alchemy = TileContent(tile_content_data['alchemy'])
    mushmush = TileContent(tile_content_data['mushmush'])
    flying_serpent = TileContent(tile_content_data['flying_serpent'])
    mining = TileContent(tile_content_data['mining'])
    birch_tree = TileContent(tile_content_data['birch_tree'])
    efreet_sultan = TileContent(tile_content_data['efreet_sultan'])
    coal_rocks = TileContent(tile_content_data['coal_rocks'])
    spruce_tree = TileContent(tile_content_data['spruce_tree'])
    skeleton = TileContent(tile_content_data['skeleton'])
    dead_tree = TileContent(tile_content_data['dead_tree'])
    vampire = TileContent(tile_content_data['vampire'])
    iron_rocks = TileContent(tile_content_data['iron_rocks'])
    death_knight = TileContent(tile_content_data['death_knight'])
    lich = TileContent(tile_content_data['lich'])
    bat = TileContent(tile_content_data['bat'])
    highwayman = TileContent(tile_content_data['highwayman'])
    glowstem = TileContent(tile_content_data['glowstem'])
    spider = TileContent(tile_content_data['spider'])
    imp = TileContent(tile_content_data['imp'])
    maple_tree = TileContent(tile_content_data['maple_tree'])
    bass_fishing_spot = TileContent(tile_content_data['bass_fishing_spot'])
    trout_fishing_spot = TileContent(tile_content_data['trout_fishing_spot'])
    mithril_rocks = TileContent(tile_content_data['mithril_rocks'])
    hellhound = TileContent(tile_content_data['hellhound'])
    cultist_acolyte = TileContent(tile_content_data['cultist_acolyte'])
    items = TileContent(tile_content_data['items'])
    rune_vendor = TileContent(tile_content_data['rune_vendor'])
    nettle = TileContent(tile_content_data['nettle'])
