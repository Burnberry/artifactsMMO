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
        return "%s - %s: %s" % (self.name, self.type, self.description)

    def __set_data(self, data):
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.description = data.get('description', None)
        self.points = data.get('points', None)
        self.type = data.get('type', None)
        self.target = data.get('target', None)
        self.total = data.get('total', None)
        self.rewards = data.get('rewards', None)
        self.current = data.get('current', None)
        self.completed_on = data.get('completed_on', None)
