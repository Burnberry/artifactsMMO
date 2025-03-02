import json
from player import Player


class Search:
    _item_data = None
    _resource_data = None
    _npc_data = None
    _npc_item_data = None
    _monster_data = None
    _effect_data = None
    _map_data = None
    _event_data = None  # todo this contains content data
    _task_data = None
    _task_reward_data = None
    _achievement_data = None

    """Helper methods"""
    @staticmethod
    def print_attributes(data, dict_name='data'):
        for key in data:
            print("self.%s = %s.get('%s', None)" % (key, dict_name, key))

    @staticmethod
    def print_data(data, keys):
        if isinstance(keys, str):
            keys = [keys]
        new_data = {}
        for values in data:
            if len(keys) == 1:
                key = values[keys[0]]
            else:
                key = tuple([values[k] for k in keys])
            new_data[key] = values
        if len(keys) == 1:
            print(json.dumps(new_data, indent=4).replace("null", "None").replace("true", "True").replace("false", "False"))
        else:
            print(new_data)

    @staticmethod
    def print_data_code(data, key, name: str):
        class_name = name.capitalize()
        data_name = name + "_data"
        for values in data:
            print("%s = %s(%s['%s'])" % (values[key], class_name, data_name, values[key]))

    """Data request getters"""

    @staticmethod
    def get_item_data():
        if not Search._item_data:
            Search._item_data = Player.get_all_data("/items")

        return Search._item_data

    @staticmethod
    def get_resource_data():
        if not Search._resource_data:
            Search._resource_data = Player.get_all_data("/resources")

        return Search._resource_data

    @staticmethod
    def get_npc_data():
        if not Search._npc_data:
            Search._npc_data = Player.get_all_data("/npcs")

        return Search._npc_data

    @staticmethod
    def get_npc_item_data():
        if not Search._npc_item_data:
            Search._npc_item_data = []
            for npc in Search.get_npc_data():
                Search._npc_item_data += Player.get_all_data("/npcs/%s/items" % npc['code'])

        return Search._npc_item_data

    @staticmethod
    def get_monster_data():
        if not Search._monster_data:
            Search._monster_data = Player.get_all_data("/monsters")

        return Search._monster_data

    @staticmethod
    def get_effect_data():
        if not Search._effect_data:
            Search._effect_data = Player.get_all_data("/effects")

        return Search._effect_data

    @staticmethod
    def get_map_data():
        if not Search._map_data:
            Search._map_data = Player.get_all_data("/maps")

        return Search._map_data

    @staticmethod
    def get_event_data():
        if not Search._event_data:
            Search._event_data = Player.get_all_data("/events")

        return Search._event_data

    @staticmethod
    def get_task_data():
        if not Search._task_data:
            Search._task_data = Player.get_all_data("/tasks/list")

        return Search._task_data

    @staticmethod
    def get_task_reward_data():
        if not Search._task_reward_data:
            Search._task_reward_data = Player.get_all_data("/tasks/rewards")

        return Search._task_reward_data

    @staticmethod
    def get_achievement_data():
        if not Search._achievement_data:
            Search._achievement_data = Player.get_all_data("/achievements")

        return Search._achievement_data
