class Achievement:
    achievements = {}

    def __init__(self, data):
        self._set_data(data)
        self.add_achievement(self)

    def _set_data(self, data):
        self.__set_data(data)

    @staticmethod
    def add_achievement(achievement):
        Achievement.achievements[achievement.code] = achievement

    @staticmethod
    def get_achievement(code):
        return Achievement.achievements[code]

    def __repr__(self):
        return "%s - %s.%s: %s" % (self.name, self.type, self.subtype, self.description)

    def __set_data(self, data):
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.description = data.get('description', None)
        self.type = data.get('type', None)
        self.subtype = data.get('subtype', None)
        self.current = data.get('current', None)
