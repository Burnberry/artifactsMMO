from data_wrappers.data.resource_data import resource_data
from typing import Optional, TYPE_CHECKING
from .drop import Drop, Drops
if TYPE_CHECKING:
    from tile_content import _TileContent
    from item import _Item


class _Resource:
    resources = {}
    
    def __init__(self, data):
        self.data = data
        self.main_item: _Item = None
        self.tile_content: _TileContent = None
        self.tiles: list[tuple[int, int]] = []
        self.drops: Drops = None
        
        self.set_data(data)
        _Resource.resources[self.code] = self
        
    def __repr__(self):
        return self.code
        
    def set_data(self, data):
        self._set_data(data)
        if "drops" in self.data:
            self.drops = Drops(self.data, self)

    def set_main_item(self):
        for drop in self.drops.drops:
            if drop.rate == 1:
                self.main_item = drop.item
                drop.item.resource = self
                return
    
    ##### AUTO-GENERATED SECTION #####
    # annotate with # custom if you don't want code to be overwritten
    
    def _set_data(self, data):
        # _set_data start
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.skill = data.get('skill', None)
        self.level = data.get('level', None)
        self.drops = data.get('drops', None)
        # _set_data end
        

class Resource(_Resource):
    @staticmethod
    def get(key) -> _Resource:
        return _Resource.resources.get(key)
    
    @staticmethod
    def all() -> list[_Resource]:
        return list(_Resource.resources.values())
        
    # auto-attrs start
    ash_tree = _Resource(resource_data.get('ash_tree', {}))
    gudgeon_fishing_spot = _Resource(resource_data.get('gudgeon_fishing_spot', {}))
    copper_rocks = _Resource(resource_data.get('copper_rocks', {}))
    sunflower_field = _Resource(resource_data.get('sunflower_field', {}))
    shrimp_fishing_spot = _Resource(resource_data.get('shrimp_fishing_spot', {}))
    iron_rocks = _Resource(resource_data.get('iron_rocks', {}))
    spruce_tree = _Resource(resource_data.get('spruce_tree', {}))
    coal_rocks = _Resource(resource_data.get('coal_rocks', {}))
    trout_fishing_spot = _Resource(resource_data.get('trout_fishing_spot', {}))
    birch_tree = _Resource(resource_data.get('birch_tree', {}))
    nettle = _Resource(resource_data.get('nettle', {}))
    bass_fishing_spot = _Resource(resource_data.get('bass_fishing_spot', {}))
    gold_rocks = _Resource(resource_data.get('gold_rocks', {}))
    dead_tree = _Resource(resource_data.get('dead_tree', {}))
    strange_rocks = _Resource(resource_data.get('strange_rocks', {}))
    magic_tree = _Resource(resource_data.get('magic_tree', {}))
    salmon_fishing_spot = _Resource(resource_data.get('salmon_fishing_spot', {}))
    glowstem = _Resource(resource_data.get('glowstem', {}))
    mithril_rocks = _Resource(resource_data.get('mithril_rocks', {}))
    maple_tree = _Resource(resource_data.get('maple_tree', {}))
    # auto-attrs end
  