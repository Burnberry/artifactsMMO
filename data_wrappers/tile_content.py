import datetime

from data_wrappers.data.tile_content_data import tile_content_data


class _TileContent:
    tile_contents = {}
    
    def __init__(self, data):
        self.data = data
        self.tiles: list[tuple[int, int]] = []
        self.expiration: datetime.datetime = None
        
        self.set_data(data)
        _TileContent.tile_contents[self.code] = self
        
    def __repr__(self):
        return self.code

    def is_active(self, server_time, cooldown=0):
        if not self.is_event:
            return True
        if self.tiles and self.expiration and self.expiration > server_time - datetime.timedelta(seconds=5+cooldown):
            return True
        return False
        
    def set_data(self, data):
        self._set_data(data)
    
    ##### AUTO-GENERATED SECTION #####
    # annotate with # custom if you don't want code to be overwritten
    
    def _set_data(self, data):
        # _set_data start
        self.type = data.get('type', None)
        self.code = data.get('code', None)
        self.is_event = data.get('is_event', None)
        # _set_data end
        

class TileContent(_TileContent):
    @staticmethod
    def get(key) -> _TileContent:
        return _TileContent.tile_contents.get(key)
    
    @staticmethod
    def all() -> list[_TileContent]:
        return list(_TileContent.tile_contents.values())
        
    # auto-attrs start
    salmon_fishing_spot = _TileContent(tile_content_data.get('salmon_fishing_spot', {}))
    goblin_wolfrider = _TileContent(tile_content_data.get('goblin_wolfrider', {}))
    orc = _TileContent(tile_content_data.get('orc', {}))
    ogre = _TileContent(tile_content_data.get('ogre', {}))
    pig = _TileContent(tile_content_data.get('pig', {}))
    woodcutting = _TileContent(tile_content_data.get('woodcutting', {}))
    gold_rocks = _TileContent(tile_content_data.get('gold_rocks', {}))
    cyclops = _TileContent(tile_content_data.get('cyclops', {}))
    blue_slime = _TileContent(tile_content_data.get('blue_slime', {}))
    yellow_slime = _TileContent(tile_content_data.get('yellow_slime', {}))
    red_slime = _TileContent(tile_content_data.get('red_slime', {}))
    green_slime = _TileContent(tile_content_data.get('green_slime', {}))
    goblin = _TileContent(tile_content_data.get('goblin', {}))
    wolf = _TileContent(tile_content_data.get('wolf', {}))
    ash_tree = _TileContent(tile_content_data.get('ash_tree', {}))
    copper_rocks = _TileContent(tile_content_data.get('copper_rocks', {}))
    chicken = _TileContent(tile_content_data.get('chicken', {}))
    cooking = _TileContent(tile_content_data.get('cooking', {}))
    weaponcrafting = _TileContent(tile_content_data.get('weaponcrafting', {}))
    gearcrafting = _TileContent(tile_content_data.get('gearcrafting', {}))
    bank = _TileContent(tile_content_data.get('bank', {}))
    grand_exchange = _TileContent(tile_content_data.get('grand_exchange', {}))
    owlbear = _TileContent(tile_content_data.get('owlbear', {}))
    cow = _TileContent(tile_content_data.get('cow', {}))
    monsters = _TileContent(tile_content_data.get('monsters', {}))
    sunflower_field = _TileContent(tile_content_data.get('sunflower_field', {}))
    nomadic_merchant = _TileContent(tile_content_data.get('nomadic_merchant', {}))
    gudgeon_fishing_spot = _TileContent(tile_content_data.get('gudgeon_fishing_spot', {}))
    shrimp_fishing_spot = _TileContent(tile_content_data.get('shrimp_fishing_spot', {}))
    jewelrycrafting = _TileContent(tile_content_data.get('jewelrycrafting', {}))
    alchemy = _TileContent(tile_content_data.get('alchemy', {}))
    mushmush = _TileContent(tile_content_data.get('mushmush', {}))
    flying_serpent = _TileContent(tile_content_data.get('flying_serpent', {}))
    mining = _TileContent(tile_content_data.get('mining', {}))
    birch_tree = _TileContent(tile_content_data.get('birch_tree', {}))
    coal_rocks = _TileContent(tile_content_data.get('coal_rocks', {}))
    spruce_tree = _TileContent(tile_content_data.get('spruce_tree', {}))
    skeleton = _TileContent(tile_content_data.get('skeleton', {}))
    dead_tree = _TileContent(tile_content_data.get('dead_tree', {}))
    vampire = _TileContent(tile_content_data.get('vampire', {}))
    iron_rocks = _TileContent(tile_content_data.get('iron_rocks', {}))
    death_knight = _TileContent(tile_content_data.get('death_knight', {}))
    lich = _TileContent(tile_content_data.get('lich', {}))
    bat = _TileContent(tile_content_data.get('bat', {}))
    highwayman = _TileContent(tile_content_data.get('highwayman', {}))
    glowstem = _TileContent(tile_content_data.get('glowstem', {}))
    spider = _TileContent(tile_content_data.get('spider', {}))
    imp = _TileContent(tile_content_data.get('imp', {}))
    maple_tree = _TileContent(tile_content_data.get('maple_tree', {}))
    bass_fishing_spot = _TileContent(tile_content_data.get('bass_fishing_spot', {}))
    trout_fishing_spot = _TileContent(tile_content_data.get('trout_fishing_spot', {}))
    mithril_rocks = _TileContent(tile_content_data.get('mithril_rocks', {}))
    hellhound = _TileContent(tile_content_data.get('hellhound', {}))
    cultist_acolyte = _TileContent(tile_content_data.get('cultist_acolyte', {}))
    items = _TileContent(tile_content_data.get('items', {}))
    rune_vendor = _TileContent(tile_content_data.get('rune_vendor', {}))
    nettle = _TileContent(tile_content_data.get('nettle', {}))
    demon = _TileContent(tile_content_data.get('demon', {}))
    bandit_lizard = _TileContent(tile_content_data.get('bandit_lizard', {}))
    cultist_emperor = _TileContent(tile_content_data.get('cultist_emperor', {}))
    strange_rocks = _TileContent(tile_content_data.get('strange_rocks', {}))
    magic_tree = _TileContent(tile_content_data.get('magic_tree', {}))
    rosenblood = _TileContent(tile_content_data.get('rosenblood', {}))
    efreet_sultan = _TileContent(tile_content_data.get('efreet_sultan', {}))
    cursed_tree = _TileContent(tile_content_data.get('cursed_tree', {}))
    fish_merchant = _TileContent(tile_content_data.get('fish_merchant', {}))
    timber_merchant = _TileContent(tile_content_data.get('timber_merchant', {}))
    herbal_merchant = _TileContent(tile_content_data.get('herbal_merchant', {}))
    gemstone_merchant = _TileContent(tile_content_data.get('gemstone_merchant', {}))
    # auto-attrs end
  