from data_wrappers.data.npc_data import npc_data
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from tile_content import _TileContent
    from npc_item import _NpcItem


class _Npc:
    npcs = {}
    
    def __init__(self, data):
        self.data = data
        self.tile_content: _TileContent = None
        self.items: list[_NpcItem] = []
        
        self.set_data(data)
        _Npc.npcs[self.code] = self
        
    def __repr__(self):
        return self.name
        
    def set_data(self, data):
        self._set_data(data)
    
    ##### AUTO-GENERATED SECTION #####
    # annotate with # custom if you don't want code to be overwritten
    
    def _set_data(self, data):
        # _set_data start
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.description = data.get('description', None)
        self.type = data.get('type', None)
        # _set_data end
        

class Npc(_Npc):
    @staticmethod
    def get(key) -> _Npc:
        return _Npc.npcs.get(key)
    
    @staticmethod
    def all() -> list[_Npc]:
        return list(_Npc.npcs.values())
        
    # auto-attrs start
    fish_merchant = _Npc(npc_data.get('fish_merchant', {}))
    gemstone_merchant = _Npc(npc_data.get('gemstone_merchant', {}))
    herbal_merchant = _Npc(npc_data.get('herbal_merchant', {}))
    nomadic_merchant = _Npc(npc_data.get('nomadic_merchant', {}))
    rune_vendor = _Npc(npc_data.get('rune_vendor', {}))
    timber_merchant = _Npc(npc_data.get('timber_merchant', {}))
    # auto-attrs end
  