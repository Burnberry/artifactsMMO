import json
from player import Player
from templates.data_template import data_template


_path = "data_wrappers/"
_tab = "    "


class Search:
    _item_data = None
    _resource_data = None
    _npc_data = None
    _npc_item_data = None
    _monster_data = None
    _effect_data = None
    _map_data = None
    _event_data = None
    _tile_content_data = None
    _task_data = None
    _task_reward_data = None
    _achievement_data = None
    _badge_data = None

    """Helper methods"""
    @staticmethod
    def autogen():
        to_generate = [
            ("item", "code", Search.get_item_data()),
            ("resource", "code", Search.get_resource_data()),
            ("npc", "code", Search.get_npc_data()),
            ("npc_item", "code", Search.get_npc_item_data()),
            ("monster", "code", Search.get_monster_data()),
            ("effect", "code", Search.get_effect_data()),
            ("event", "code", Search.get_event_data()),
            ("tile_content", "code", Search.get_tile_content_data()),
            ("task", "code", Search.get_task_data()),
            ("task_reward", "code", Search.get_task_reward_data()),
            ("achievement", "code", Search.get_achievement_data()),
            ("badge", "code", Search.get_badge_data()),
        ]

        for name, key, data in to_generate:
            print(name, key)
            Search.ensure_data_file(name, key)
            Search.data_autogen(name, data, key)

        tile_data = Search.get_map_data()
        Search.write_raw_data("tile", tile_data, ['x', 'y'])

    @staticmethod
    def file_exists(path):
        try:
            with open(path, 'r') as file:
                file.close()
            return True
        except IOError:
            return False

    @staticmethod
    def data_autogen(name, data, code):
        raw_data = Search.get_raw_data(data, code)
        Search.write_raw_data(name, data, code)
        Search.ensure_data_file(name, code)

        data_path = _path + "%s.py" % name
        content = ""

        with open(data_path, 'r') as file:
            manual_section = []
            auto_section = []
            is_auto = False

            for line in file.readlines():
                if "AUTO-GENERATED SECTION" in line:
                    is_auto = True

                if not is_auto:
                    manual_section.append(line)
                if is_auto:
                    auto_section.append(line)
            file.close()

        auto_section = Search.get_updated_auto_lines(auto_section, name, raw_data, code)
        for line in manual_section + auto_section:
            content += line
        content = content[:-1]

        with open(data_path, 'w+') as file:
            file.write(content)
            file.close()

    @staticmethod
    def get_updated_auto_lines(auto_section, name, raw_data, code):
        new_section = []
        key = False
        data_seen = set()

        for line in auto_section:
            if "auto-attrs end" in line:
                key = False
                Search.add_attrs(new_section, name, raw_data)

            elif "_set_data end" in line:
                key = False
                Search.add_set_data(new_section, name, raw_data, code, data_seen)

            if not key:
                new_section.append(line)
            if key == "attrs":
                if "# custom" in line:
                    new_section.append(line)
            elif key == "data":
                if "# custom" in line:
                    data_seen.add(line.split('=')[0].strip().replace('self.', ''))
                    new_section.append(line)

            if "auto-attrs start" in line:
                key = "attrs"
            elif "_set_data start" in line:
                key = "data"

        return new_section

    @staticmethod
    def add_attrs(new_section, name, raw_data):
        sc_name, cc_name = Search.get_names(name)
        for key in raw_data:
            line = "    %s = _%s(%s_data.get('%s', {}))\n" % (key, cc_name, sc_name, key)
            new_section.append(line)

    @staticmethod
    def add_set_data(new_section, name, raw_data, code, data_seen):
        values = list(raw_data.values())[0]
        for key in values:
            if key in data_seen:
                continue
            line = "        self.%s = data.get('%s', None)\n" % (key, key)
            new_section.append(line)

    @staticmethod
    def ensure_data_file(name, code):
        sc_name, cc_name = Search.get_names(name)
        path = _path + "%s.py" % name
        if not Search.file_exists(path):
            # create file
            with open(path, 'w+') as file:
                template = data_template % (sc_name, sc_name, cc_name, sc_name, cc_name, sc_name, code, code, cc_name, cc_name, cc_name, cc_name, sc_name, cc_name, cc_name, sc_name)
                file.write(template)
                file.close()

    @staticmethod
    def write_raw_data(name, data, keys):
        raw_data = Search.get_raw_data(data, keys, text=True)
        with open(_path + "data/%s_data.py" % name, 'w+') as file:
            file.write("%s_data = " % name)
            file.write(raw_data)
            file.close()

    @staticmethod
    def get_raw_data(data, keys, text=False):
        if isinstance(keys, str):
            keys = [keys]
        new_data = {}
        for values in data:
            if len(keys) == 1:
                key = values[keys[0]]
            else:
                key = tuple([values[k] for k in keys])
            new_data[key] = values
        if len(keys) == 1 and text:
            return json.dumps(new_data, indent=4).replace("null", "None").replace("true", "True").replace("false",
                                                                                                         "False")
        elif text:
            return str(new_data)
        else:
            return new_data

    @staticmethod
    def get_names(name):
        sc_name = name
        cc_name = ""
        for n in name.split('_'):
            cc_name += n.capitalize()
        return sc_name, cc_name

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
            Search._item_data = Player.get_all_data("items")

        return Search._item_data

    @staticmethod
    def get_resource_data():
        if not Search._resource_data:
            Search._resource_data = Player.get_all_data("resources")

        return Search._resource_data

    @staticmethod
    def get_npc_data():
        if not Search._npc_data:
            Search._npc_data = Player.get_all_data("npcs")

        return Search._npc_data

    @staticmethod
    def get_npc_item_data():
        if not Search._npc_item_data:
            Search._npc_item_data = []
            for npc in Search.get_npc_data():
                Search._npc_item_data += Player.get_all_data("npcs/%s/items" % npc['code'])

        return Search._npc_item_data

    @staticmethod
    def get_monster_data():
        if not Search._monster_data:
            Search._monster_data = Player.get_all_data("monsters")

        return Search._monster_data

    @staticmethod
    def get_effect_data():
        if not Search._effect_data:
            Search._effect_data = Player.get_all_data("effects")

        return Search._effect_data

    @staticmethod
    def get_map_data():
        if not Search._map_data:
            Search._map_data = Player.get_all_data("maps")

        return Search._map_data

    @staticmethod
    def get_event_data():
        if not Search._event_data:
            Search._event_data = Player.get_all_data("events")

        return Search._event_data

    @staticmethod
    def get_tile_content_data():
        if not Search._tile_content_data:
            map_data = Search.get_map_data()
            event_data = Search.get_event_data()
            content_data = {}
            for map_vals in map_data:
                if content := map_vals.get('content', None):
                    content_data[content['code']] = content
                    content_data[content['code']]['is_event'] = False
            for event_vals in event_data:
                if content := event_vals.get('content', None):
                    content_data[content['code']] = content
                    content_data[content['code']]['is_event'] = True

            Search._tile_content_data = list(content_data.values())

        return Search._tile_content_data

    @staticmethod
    def get_task_data():
        if not Search._task_data:
            Search._task_data = Player.get_all_data("tasks/list")

        return Search._task_data

    @staticmethod
    def get_task_reward_data():
        if not Search._task_reward_data:
            Search._task_reward_data = Player.get_all_data("tasks/rewards")

        return Search._task_reward_data

    @staticmethod
    def get_achievement_data():
        if not Search._achievement_data:
            Search._achievement_data = Player.get_all_data("achievements")

        return Search._achievement_data

    @staticmethod
    def get_badge_data():
        if not Search._badge_data:
            Search._badge_data = Player.get_all_data("badges")

        return Search._badge_data
