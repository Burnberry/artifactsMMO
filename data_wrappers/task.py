class Task:
    tasks = {}

    def __init__(self, data):
        from data_wrappers.item import Item
        from data_wrappers.monster import Monster
        self.item: Item = None
        self.monster: Monster = None

        self._set_data(data)
        self.add_task(self)

    def _set_data(self, data):
        self.__set_data(data)

    @staticmethod
    def add_task(task):
        Task.tasks[task.code] = task

    @staticmethod
    def get_task(code):
        return Task.tasks[code]

    def __repr__(self):
        return "Task: %s.%s %s/%s - %s lv.%s - x%s coins" % (self.type, self.code, self.min_quantity, self.max_quantity, self.skill, self.level, self.rewards['items'][0]['quantity'])

    def __set_data(self, data):
        self.code = data.get('code', None)
        self.level = data.get('level', None)
        self.type = data.get('type', None)
        self.min_quantity = data.get('min_quantity', None)
        self.max_quantity = data.get('max_quantity', None)
        self.skill = data.get('skill', None)
        self.rewards = data.get('rewards', None)
