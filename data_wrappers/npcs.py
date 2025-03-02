from data_wrappers.npc import Npc
from data_wrappers.data.npc_data import npc_data


class Npcs:
    npcs = Npc.npcs

    fish_merchant = Npc(npc_data['fish_merchant'])
    gemstone_merchant = Npc(npc_data['gemstone_merchant'])
    herbal_merchant = Npc(npc_data['herbal_merchant'])
    nomadic_merchant = Npc(npc_data['nomadic_merchant'])
    rune_vendor = Npc(npc_data['rune_vendor'])
    timber_merchant = Npc(npc_data['timber_merchant'])
