from data_wrappers.data.effect_data import effect_data


class _Effect:
    effects = {}
    
    def __init__(self, data):
        self.data = data
        
        self.set_data(data)
        _Effect.effects[self.code] = self
        
    def __repr__(self):
        return "%s - %s" % (self.name, self.description)
        
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
        self.subtype = data.get('subtype', None)
        # _set_data end
        

class Effect(_Effect):
    @staticmethod
    def get(key) -> _Effect:
        return _Effect.effects.get(key)
    
    @staticmethod
    def all() -> list[_Effect]:
        return list(_Effect.effects.values())
        
    # auto-attrs start
    boost_hp = _Effect(effect_data.get('boost_hp', {}))
    boost_dmg_fire = _Effect(effect_data.get('boost_dmg_fire', {}))
    boost_dmg_water = _Effect(effect_data.get('boost_dmg_water', {}))
    boost_dmg_air = _Effect(effect_data.get('boost_dmg_air', {}))
    boost_dmg_earth = _Effect(effect_data.get('boost_dmg_earth', {}))
    restore = _Effect(effect_data.get('restore', {}))
    healing = _Effect(effect_data.get('healing', {}))
    antipoison = _Effect(effect_data.get('antipoison', {}))
    poison = _Effect(effect_data.get('poison', {}))
    lifesteal = _Effect(effect_data.get('lifesteal', {}))
    reconstitution = _Effect(effect_data.get('reconstitution', {}))
    burn = _Effect(effect_data.get('burn', {}))
    boost_res_air = _Effect(effect_data.get('boost_res_air', {}))
    boost_res_water = _Effect(effect_data.get('boost_res_water', {}))
    boost_res_earth = _Effect(effect_data.get('boost_res_earth', {}))
    boost_res_fire = _Effect(effect_data.get('boost_res_fire', {}))
    heal = _Effect(effect_data.get('heal', {}))
    teleport_x = _Effect(effect_data.get('teleport_x', {}))
    gold = _Effect(effect_data.get('gold', {}))
    teleport_y = _Effect(effect_data.get('teleport_y', {}))
    attack_fire = _Effect(effect_data.get('attack_fire', {}))
    attack_water = _Effect(effect_data.get('attack_water', {}))
    attack_air = _Effect(effect_data.get('attack_air', {}))
    attack_earth = _Effect(effect_data.get('attack_earth', {}))
    dmg = _Effect(effect_data.get('dmg', {}))
    dmg_fire = _Effect(effect_data.get('dmg_fire', {}))
    dmg_water = _Effect(effect_data.get('dmg_water', {}))
    dmg_air = _Effect(effect_data.get('dmg_air', {}))
    dmg_earth = _Effect(effect_data.get('dmg_earth', {}))
    res_fire = _Effect(effect_data.get('res_fire', {}))
    res_water = _Effect(effect_data.get('res_water', {}))
    res_air = _Effect(effect_data.get('res_air', {}))
    res_earth = _Effect(effect_data.get('res_earth', {}))
    critical_strike = _Effect(effect_data.get('critical_strike', {}))
    wisdom = _Effect(effect_data.get('wisdom', {}))
    prospecting = _Effect(effect_data.get('prospecting', {}))
    woodcutting = _Effect(effect_data.get('woodcutting', {}))
    fishing = _Effect(effect_data.get('fishing', {}))
    mining = _Effect(effect_data.get('mining', {}))
    alchemy = _Effect(effect_data.get('alchemy', {}))
    hp = _Effect(effect_data.get('hp', {}))
    inventory_space = _Effect(effect_data.get('inventory_space', {}))
    haste = _Effect(effect_data.get('haste', {}))
    # auto-attrs end
  