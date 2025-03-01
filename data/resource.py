class Resource:
    resources = {}

    def __init__(self, data):
        self._set_data(data)
        self.add_resource(self)

    def _set_data(self, data):
        self.__set_data(data)

    @staticmethod
    def add_resource(resource):
        Resource.resources[resource.code] = resource

    @staticmethod
    def get_resource(code):
        return Resource.resources[code]

    def __repr__(self):
        return self.name

    def __set_data(self, data):
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.skill = data.get('skill', None)
        self.level = data.get('level', None)
        self.drops = data.get('drops', None)
