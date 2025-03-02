from data_wrappers.achievement import Achievement
from data_wrappers.data.achievement_data import achievement_data


class Achievements:
    achievements = Achievement.achievements

    @staticmethod
    def get_effect(code):
        return Achievements.achievements.get(code, None)

    loktar_ogar = Achievement(achievement_data['loktar_ogar'])
    feather_me_impressed = Achievement(achievement_data['feather_me_impressed'])
    novice = Achievement(achievement_data['novice'])
    tasks_farmer = Achievement(achievement_data['tasks_farmer'])
    ecologist = Achievement(achievement_data['ecologist'])
    cabinet_maker = Achievement(achievement_data['cabinet_maker'])
    worker = Achievement(achievement_data['worker'])
    mithril_mastery = Achievement(achievement_data['mithril_mastery'])
    amateur_miner = Achievement(achievement_data['amateur_miner'])
    miner = Achievement(achievement_data['miner'])
    intermediate_miner = Achievement(achievement_data['intermediate_miner'])
    expert_miner = Achievement(achievement_data['expert_miner'])
    professional_miner = Achievement(achievement_data['professional_miner'])
    amateur_lumberjack = Achievement(achievement_data['amateur_lumberjack'])
    lumberjack = Achievement(achievement_data['lumberjack'])
    intermediate_lumberjack = Achievement(achievement_data['intermediate_lumberjack'])
    expert_lumberjack = Achievement(achievement_data['expert_lumberjack'])
    professional_lumberjack = Achievement(achievement_data['professional_lumberjack'])
    amateur_fisherman = Achievement(achievement_data['amateur_fisherman'])
    fisherman = Achievement(achievement_data['fisherman'])
    intermediate_fisherman = Achievement(achievement_data['intermediate_fisherman'])
    expert_fisherman = Achievement(achievement_data['expert_fisherman'])
    professional_fisherman = Achievement(achievement_data['professional_fisherman'])
    amateur_alchmist = Achievement(achievement_data['amateur_alchmist'])
    intermediate_alchemist = Achievement(achievement_data['intermediate_alchemist'])
    expert_alchemist = Achievement(achievement_data['expert_alchemist'])
    restoring_the_peace = Achievement(achievement_data['restoring_the_peace'])
    king_of_the_Forest = Achievement(achievement_data['king_of_the_Forest'])
    closing_the_gate = Achievement(achievement_data['closing_the_gate'])
    i_want_bacon = Achievement(achievement_data['i_want_bacon'])
    adventurer = Achievement(achievement_data['adventurer'])
    arachnophobia_conquered = Achievement(achievement_data['arachnophobia_conquered'])
    maple_maestro = Achievement(achievement_data['maple_maestro'])
    catch_and_cook = Achievement(achievement_data['catch_and_cook'])
    sweet_as_pie = Achievement(achievement_data['sweet_as_pie'])
    strange_miner = Achievement(achievement_data['strange_miner'])
    magic_lumberjack = Achievement(achievement_data['magic_lumberjack'])
    alchemist = Achievement(achievement_data['alchemist'])
    cursed_wood_blessed_victory = Achievement(achievement_data['cursed_wood_blessed_victory'])
    recall_forever = Achievement(achievement_data['recall_forever'])
    the_french_cheese = Achievement(achievement_data['the_french_cheese'])
    money_time = Achievement(achievement_data['money_time'])
    lich_please = Achievement(achievement_data['lich_please'])
    grand_master = Achievement(achievement_data['grand_master'])
    the_new_king = Achievement(achievement_data['the_new_king'])
    the_new_bandit = Achievement(achievement_data['the_new_bandit'])
    swordbreaker = Achievement(achievement_data['swordbreaker'])
    magic_power = Achievement(achievement_data['magic_power'])
    crown_of_mithril = Achievement(achievement_data['crown_of_mithril'])
    crafted_with_honor = Achievement(achievement_data['crafted_with_honor'])
    bite_oh_algae = Achievement(achievement_data['bite_oh_algae'])
    diamond_in_the_sky = Achievement(achievement_data['diamond_in_the_sky'])
    enchanted_alchemist = Achievement(achievement_data['enchanted_alchemist'])
    real_canadian = Achievement(achievement_data['real_canadian'])
    sultan_slayer = Achievement(achievement_data['sultan_slayer'])
    rosenblod = Achievement(achievement_data['rosenblod'])
    cult_destroyer = Achievement(achievement_data['cult_destroyer'])
    life_lover = Achievement(achievement_data['life_lover'])
    its_malefic = Achievement(achievement_data['its_malefic'])
    tasks_coins_fan = Achievement(achievement_data['tasks_coins_fan'])
    the_planet_thanks_you = Achievement(achievement_data['the_planet_thanks_you'])
    elixir_collector = Achievement(achievement_data['elixir_collector'])
    carnivore = Achievement(achievement_data['carnivore'])
    release_the_wolves = Achievement(achievement_data['release_the_wolves'])
