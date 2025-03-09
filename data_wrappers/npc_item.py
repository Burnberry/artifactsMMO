from data_wrappers.data.npc_item_data import npc_item_data
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from item import _Item
    from npc import _Npc


class _NpcItem:
    npc_items = {}
    
    def __init__(self, data):
        self.data = data
        self.item: _Item = None
        self.npc: _Npc = None
        
        self.set_data(data)
        _NpcItem.npc_items[self.code] = self
        
    def __repr__(self):
        return "%s - %s - buy: %s - sell: %s" % (self.code, self.npc, self.buy_price, self.sell_price)
        
    def set_data(self, data):
        self._set_data(data)
    
    ##### AUTO-GENERATED SECTION #####
    # annotate with # custom if you don't want code to be overwritten
    
    def _set_data(self, data):
        # _set_data start
        self.code = data.get('code', None)
        self.npc = data.get('npc', None)
        self.buy_price = data.get('buy_price', None)
        self.sell_price = data.get('sell_price', None)
        # _set_data end
        

class NpcItem(_NpcItem):
    @staticmethod
    def get(key) -> _NpcItem:
        return _NpcItem.npc_items.get(key)
    
    @staticmethod
    def all() -> list[_NpcItem]:
        return list(_NpcItem.npc_items.values())
        
    # auto-attrs start
    algae = _NpcItem(npc_item_data.get('algae', {}))
    bass = _NpcItem(npc_item_data.get('bass', {}))
    frozen_fishing_rod = _NpcItem(npc_item_data.get('frozen_fishing_rod', {}))
    golden_chalice = _NpcItem(npc_item_data.get('golden_chalice', {}))
    golden_shrimp = _NpcItem(npc_item_data.get('golden_shrimp', {}))
    gudgeon = _NpcItem(npc_item_data.get('gudgeon', {}))
    salmon = _NpcItem(npc_item_data.get('salmon', {}))
    shrimp = _NpcItem(npc_item_data.get('shrimp', {}))
    silver_chalice = _NpcItem(npc_item_data.get('silver_chalice', {}))
    trout = _NpcItem(npc_item_data.get('trout', {}))
    coal = _NpcItem(npc_item_data.get('coal', {}))
    copper_ore = _NpcItem(npc_item_data.get('copper_ore', {}))
    diamond = _NpcItem(npc_item_data.get('diamond', {}))
    emerald = _NpcItem(npc_item_data.get('emerald', {}))
    frozen_pickaxe = _NpcItem(npc_item_data.get('frozen_pickaxe', {}))
    gold_ore = _NpcItem(npc_item_data.get('gold_ore', {}))
    iron_ore = _NpcItem(npc_item_data.get('iron_ore', {}))
    mithril_ore = _NpcItem(npc_item_data.get('mithril_ore', {}))
    piece_of_obsidian = _NpcItem(npc_item_data.get('piece_of_obsidian', {}))
    ruby = _NpcItem(npc_item_data.get('ruby', {}))
    sapphire = _NpcItem(npc_item_data.get('sapphire', {}))
    strange_ore = _NpcItem(npc_item_data.get('strange_ore', {}))
    topaz = _NpcItem(npc_item_data.get('topaz', {}))
    frozen_gloves = _NpcItem(npc_item_data.get('frozen_gloves', {}))
    glowstem_leaf = _NpcItem(npc_item_data.get('glowstem_leaf', {}))
    nettle_leaf = _NpcItem(npc_item_data.get('nettle_leaf', {}))
    recall_potion = _NpcItem(npc_item_data.get('recall_potion', {}))
    south_bank_potion = _NpcItem(npc_item_data.get('south_bank_potion', {}))
    sunflower = _NpcItem(npc_item_data.get('sunflower', {}))
    backpack = _NpcItem(npc_item_data.get('backpack', {}))
    death_knight_sword = _NpcItem(npc_item_data.get('death_knight_sword', {}))
    forest_ring = _NpcItem(npc_item_data.get('forest_ring', {}))
    golden_egg = _NpcItem(npc_item_data.get('golden_egg', {}))
    highwayman_dagger = _NpcItem(npc_item_data.get('highwayman_dagger', {}))
    lich_crown = _NpcItem(npc_item_data.get('lich_crown', {}))
    minor_health_potion = _NpcItem(npc_item_data.get('minor_health_potion', {}))
    old_boots = _NpcItem(npc_item_data.get('old_boots', {}))
    small_antidote = _NpcItem(npc_item_data.get('small_antidote', {}))
    wolf_ears = _NpcItem(npc_item_data.get('wolf_ears', {}))
    wooden_club = _NpcItem(npc_item_data.get('wooden_club', {}))
    burn_rune = _NpcItem(npc_item_data.get('burn_rune', {}))
    healing_rune = _NpcItem(npc_item_data.get('healing_rune', {}))
    lifesteal_rune = _NpcItem(npc_item_data.get('lifesteal_rune', {}))
    ash_wood = _NpcItem(npc_item_data.get('ash_wood', {}))
    birch_wood = _NpcItem(npc_item_data.get('birch_wood', {}))
    cursed_wood = _NpcItem(npc_item_data.get('cursed_wood', {}))
    dead_wood = _NpcItem(npc_item_data.get('dead_wood', {}))
    frozen_axe = _NpcItem(npc_item_data.get('frozen_axe', {}))
    magic_sap = _NpcItem(npc_item_data.get('magic_sap', {}))
    magic_wood = _NpcItem(npc_item_data.get('magic_wood', {}))
    maple_sap = _NpcItem(npc_item_data.get('maple_sap', {}))
    maple_wood = _NpcItem(npc_item_data.get('maple_wood', {}))
    sap = _NpcItem(npc_item_data.get('sap', {}))
    spruce_wood = _NpcItem(npc_item_data.get('spruce_wood', {}))
    # auto-attrs end
  