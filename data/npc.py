class Npc:
    npcs = {}

    def __init__(self, data):
        self._set_data(data)
        self.add_resource(self)

    def _set_data(self, data):
        self.__set_data(data)

    @staticmethod
    def add_resource(resource):
        Npc.npcs[resource.code] = resource

    @staticmethod
    def get_resource(code):
        return Npc.npcs[code]

    def __repr__(self):
        return self.name

    def __set_data(self, data):
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.description = data.get('description', None)
        self.type = data.get('type', None)
