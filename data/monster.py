class Monster:
    monsters = {}

    def __init__(self, data):
        self._set_data(data)
        self.add_resource(self)

    def _set_data(self, data):
        self.__set_data(data)

    @staticmethod
    def add_resource(resource):
        Monster.monsters[resource.code] = resource

    @staticmethod
    def get_resource(code):
        return Monster.monsters[code]

    def __repr__(self):
        return self.name

    def __set_data(self, data):
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.level = data.get('level', None)
        self.hp = data.get('hp', None)
        self.attack_fire = data.get('attack_fire', None)
        self.attack_earth = data.get('attack_earth', None)
        self.attack_water = data.get('attack_water', None)
        self.attack_air = data.get('attack_air', None)
        self.res_fire = data.get('res_fire', None)
        self.res_earth = data.get('res_earth', None)
        self.res_water = data.get('res_water', None)
        self.res_air = data.get('res_air', None)
        self.critical_strike = data.get('critical_strike', None)
        self.effects = data.get('effects', None)
        self.min_gold = data.get('min_gold', None)
        self.max_gold = data.get('max_gold', None)
        self.drops = data.get('drops', None)
