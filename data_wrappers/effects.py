from data_wrappers.effect import Effect
from data_wrappers.effect_data import effect_data


class Effects:
    effects = Effect.effects

    @staticmethod
    def get_effect(code):
        return Effect.effects.get(code, None)

    boost_hp = Effect(effect_data['boost_hp'])
    boost_dmg_fire = Effect(effect_data['boost_dmg_fire'])
    boost_dmg_water = Effect(effect_data['boost_dmg_water'])
    boost_dmg_air = Effect(effect_data['boost_dmg_air'])
    boost_dmg_earth = Effect(effect_data['boost_dmg_earth'])
    restore = Effect(effect_data['restore'])
    healing = Effect(effect_data['healing'])
    antipoison = Effect(effect_data['antipoison'])
    poison = Effect(effect_data['poison'])
    lifesteal = Effect(effect_data['lifesteal'])
    reconstitution = Effect(effect_data['reconstitution'])
    burn = Effect(effect_data['burn'])
    boost_res_air = Effect(effect_data['boost_res_air'])
    boost_res_water = Effect(effect_data['boost_res_water'])
    boost_res_earth = Effect(effect_data['boost_res_earth'])
    boost_res_fire = Effect(effect_data['boost_res_fire'])
    heal = Effect(effect_data['heal'])
    teleport_x = Effect(effect_data['teleport_x'])
    gold = Effect(effect_data['gold'])
    teleport_y = Effect(effect_data['teleport_y'])
    attack_fire = Effect(effect_data['attack_fire'])
    attack_water = Effect(effect_data['attack_water'])
    attack_air = Effect(effect_data['attack_air'])
    attack_earth = Effect(effect_data['attack_earth'])
    dmg = Effect(effect_data['dmg'])
    dmg_fire = Effect(effect_data['dmg_fire'])
    dmg_water = Effect(effect_data['dmg_water'])
    dmg_air = Effect(effect_data['dmg_air'])
    dmg_earth = Effect(effect_data['dmg_earth'])
    res_fire = Effect(effect_data['res_fire'])
    res_water = Effect(effect_data['res_water'])
    res_air = Effect(effect_data['res_air'])
    res_earth = Effect(effect_data['res_earth'])
    critical_strike = Effect(effect_data['critical_strike'])
    wisdom = Effect(effect_data['wisdom'])
    prospecting = Effect(effect_data['prospecting'])
    woodcutting = Effect(effect_data['woodcutting'])
    fishing = Effect(effect_data['fishing'])
    mining = Effect(effect_data['mining'])
    alchemy = Effect(effect_data['alchemy'])
    hp = Effect(effect_data['hp'])
    inventory_space = Effect(effect_data['inventory_space'])
    haste = Effect(effect_data['haste'])