from data_wrappers.data.monster_data import monster_data
from typing import Optional, TYPE_CHECKING
from .drop import Drop, Drops
if TYPE_CHECKING:
    from tile_content import _TileContent


class _Monster:
    monsters = {}
    
    def __init__(self, data):
        self.data = data
        self.tile_content: _TileContent = None
        self.drops: Drops = None
        
        self.set_data(data)
        _Monster.monsters[self.code] = self
        
    def __repr__(self):
        return self.name
        
    def set_data(self, data):
        self._set_data(data)
        if "drops" in self.data:
            self.drops = Drops(self.data, self)
    
    ##### AUTO-GENERATED SECTION #####
    # annotate with # custom if you don't want code to be overwritten
    
    def _set_data(self, data):
        # _set_data start
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.level = data.get('level', None)
        self.hp = data.get('hp', None)
        self.attack_fire = data.get('attack_fire', None)
        self.attack_earth = data.get('attack_earth', None)
        self.attack_water = data.get('attack_water', None)
        self.attack_air = data.get('attack_air', None)
        self.res_fire = data.get('res_fire', None)
        self.res_earth = data.get('res_earth', None)
        self.res_water = data.get('res_water', None)
        self.res_air = data.get('res_air', None)
        self.critical_strike = data.get('critical_strike', None)
        self.effects = data.get('effects', None)
        self.min_gold = data.get('min_gold', None)
        self.max_gold = data.get('max_gold', None)
        self.drops = data.get('drops', None)
        # _set_data end
        

class Monster(_Monster):
    @staticmethod
    def get(key) -> _Monster:
        return _Monster.monsters.get(key)
    
    @staticmethod
    def all() -> list[_Monster]:
        return list(_Monster.monsters.values())
        
    # auto-attrs start
    chicken = _Monster(monster_data.get('chicken', {}))
    yellow_slime = _Monster(monster_data.get('yellow_slime', {}))
    green_slime = _Monster(monster_data.get('green_slime', {}))
    blue_slime = _Monster(monster_data.get('blue_slime', {}))
    red_slime = _Monster(monster_data.get('red_slime', {}))
    cow = _Monster(monster_data.get('cow', {}))
    mushmush = _Monster(monster_data.get('mushmush', {}))
    flying_serpent = _Monster(monster_data.get('flying_serpent', {}))
    wolf = _Monster(monster_data.get('wolf', {}))
    highwayman = _Monster(monster_data.get('highwayman', {}))
    skeleton = _Monster(monster_data.get('skeleton', {}))
    pig = _Monster(monster_data.get('pig', {}))
    ogre = _Monster(monster_data.get('ogre', {}))
    spider = _Monster(monster_data.get('spider', {}))
    vampire = _Monster(monster_data.get('vampire', {}))
    bandit_lizard = _Monster(monster_data.get('bandit_lizard', {}))
    cyclops = _Monster(monster_data.get('cyclops', {}))
    death_knight = _Monster(monster_data.get('death_knight', {}))
    imp = _Monster(monster_data.get('imp', {}))
    owlbear = _Monster(monster_data.get('owlbear', {}))
    demon = _Monster(monster_data.get('demon', {}))
    lich = _Monster(monster_data.get('lich', {}))
    cultist_acolyte = _Monster(monster_data.get('cultist_acolyte', {}))
    cursed_tree = _Monster(monster_data.get('cursed_tree', {}))
    cultist_emperor = _Monster(monster_data.get('cultist_emperor', {}))
    goblin = _Monster(monster_data.get('goblin', {}))
    bat = _Monster(monster_data.get('bat', {}))
    orc = _Monster(monster_data.get('orc', {}))
    rosenblood = _Monster(monster_data.get('rosenblood', {}))
    goblin_wolfrider = _Monster(monster_data.get('goblin_wolfrider', {}))
    hellhound = _Monster(monster_data.get('hellhound', {}))
    efreet_sultan = _Monster(monster_data.get('efreet_sultan', {}))
    # auto-attrs end
  