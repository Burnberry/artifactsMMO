from data_wrappers.data.achievement_data import achievement_data


class _Achievement:
    achievements = {}
    
    def __init__(self, data):
        self.data = data
        
        self.set_data(data)
        _Achievement.achievements[self.code] = self

    def __repr__(self):
        return "%s - %s: %s" % (self.name, self.type, self.description)
        
    def set_data(self, data):
        self._set_data(data)
    
    ##### AUTO-GENERATED SECTION #####
    # annotate with # custom if you don't want code to be overwritten
    
    def _set_data(self, data):
        # _set_data start
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.description = data.get('description', None)
        self.points = data.get('points', None)
        self.type = data.get('type', None)
        self.target = data.get('target', None)
        self.total = data.get('total', None)
        self.rewards = data.get('rewards', None)
        # _set_data end
        

class Achievement(_Achievement):
    @staticmethod
    def get(key) -> _Achievement:
        return _Achievement.achievements.get(key)
    
    @staticmethod
    def all() -> list[_Achievement]:
        return list(_Achievement.achievements.values())
        
    # auto-attrs start
    loktar_ogar = _Achievement(achievement_data.get('loktar_ogar', {}))
    feather_me_impressed = _Achievement(achievement_data.get('feather_me_impressed', {}))
    novice = _Achievement(achievement_data.get('novice', {}))
    tasks_farmer = _Achievement(achievement_data.get('tasks_farmer', {}))
    ecologist = _Achievement(achievement_data.get('ecologist', {}))
    cabinet_maker = _Achievement(achievement_data.get('cabinet_maker', {}))
    worker = _Achievement(achievement_data.get('worker', {}))
    mithril_mastery = _Achievement(achievement_data.get('mithril_mastery', {}))
    amateur_miner = _Achievement(achievement_data.get('amateur_miner', {}))
    miner = _Achievement(achievement_data.get('miner', {}))
    intermediate_miner = _Achievement(achievement_data.get('intermediate_miner', {}))
    expert_miner = _Achievement(achievement_data.get('expert_miner', {}))
    professional_miner = _Achievement(achievement_data.get('professional_miner', {}))
    amateur_lumberjack = _Achievement(achievement_data.get('amateur_lumberjack', {}))
    lumberjack = _Achievement(achievement_data.get('lumberjack', {}))
    intermediate_lumberjack = _Achievement(achievement_data.get('intermediate_lumberjack', {}))
    expert_lumberjack = _Achievement(achievement_data.get('expert_lumberjack', {}))
    professional_lumberjack = _Achievement(achievement_data.get('professional_lumberjack', {}))
    amateur_fisherman = _Achievement(achievement_data.get('amateur_fisherman', {}))
    fisherman = _Achievement(achievement_data.get('fisherman', {}))
    intermediate_fisherman = _Achievement(achievement_data.get('intermediate_fisherman', {}))
    expert_fisherman = _Achievement(achievement_data.get('expert_fisherman', {}))
    professional_fisherman = _Achievement(achievement_data.get('professional_fisherman', {}))
    amateur_alchmist = _Achievement(achievement_data.get('amateur_alchmist', {}))
    intermediate_alchemist = _Achievement(achievement_data.get('intermediate_alchemist', {}))
    expert_alchemist = _Achievement(achievement_data.get('expert_alchemist', {}))
    restoring_the_peace = _Achievement(achievement_data.get('restoring_the_peace', {}))
    king_of_the_Forest = _Achievement(achievement_data.get('king_of_the_Forest', {}))
    closing_the_gate = _Achievement(achievement_data.get('closing_the_gate', {}))
    i_want_bacon = _Achievement(achievement_data.get('i_want_bacon', {}))
    adventurer = _Achievement(achievement_data.get('adventurer', {}))
    arachnophobia_conquered = _Achievement(achievement_data.get('arachnophobia_conquered', {}))
    maple_maestro = _Achievement(achievement_data.get('maple_maestro', {}))
    catch_and_cook = _Achievement(achievement_data.get('catch_and_cook', {}))
    sweet_as_pie = _Achievement(achievement_data.get('sweet_as_pie', {}))
    strange_miner = _Achievement(achievement_data.get('strange_miner', {}))
    magic_lumberjack = _Achievement(achievement_data.get('magic_lumberjack', {}))
    alchemist = _Achievement(achievement_data.get('alchemist', {}))
    cursed_wood_blessed_victory = _Achievement(achievement_data.get('cursed_wood_blessed_victory', {}))
    recall_forever = _Achievement(achievement_data.get('recall_forever', {}))
    the_french_cheese = _Achievement(achievement_data.get('the_french_cheese', {}))
    money_time = _Achievement(achievement_data.get('money_time', {}))
    lich_please = _Achievement(achievement_data.get('lich_please', {}))
    grand_master = _Achievement(achievement_data.get('grand_master', {}))
    the_new_king = _Achievement(achievement_data.get('the_new_king', {}))
    the_new_bandit = _Achievement(achievement_data.get('the_new_bandit', {}))
    swordbreaker = _Achievement(achievement_data.get('swordbreaker', {}))
    magic_power = _Achievement(achievement_data.get('magic_power', {}))
    crown_of_mithril = _Achievement(achievement_data.get('crown_of_mithril', {}))
    crafted_with_honor = _Achievement(achievement_data.get('crafted_with_honor', {}))
    bite_oh_algae = _Achievement(achievement_data.get('bite_oh_algae', {}))
    diamond_in_the_sky = _Achievement(achievement_data.get('diamond_in_the_sky', {}))
    enchanted_alchemist = _Achievement(achievement_data.get('enchanted_alchemist', {}))
    real_canadian = _Achievement(achievement_data.get('real_canadian', {}))
    sultan_slayer = _Achievement(achievement_data.get('sultan_slayer', {}))
    rosenblod = _Achievement(achievement_data.get('rosenblod', {}))
    cult_destroyer = _Achievement(achievement_data.get('cult_destroyer', {}))
    life_lover = _Achievement(achievement_data.get('life_lover', {}))
    its_malefic = _Achievement(achievement_data.get('its_malefic', {}))
    tasks_coins_fan = _Achievement(achievement_data.get('tasks_coins_fan', {}))
    the_planet_thanks_you = _Achievement(achievement_data.get('the_planet_thanks_you', {}))
    elixir_collector = _Achievement(achievement_data.get('elixir_collector', {}))
    carnivore = _Achievement(achievement_data.get('carnivore', {}))
    release_the_wolves = _Achievement(achievement_data.get('release_the_wolves', {}))
    # auto-attrs end
  