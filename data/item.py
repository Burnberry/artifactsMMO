class Item:
    items = {}

    def __init__(self, data):
        self.resource: 'Resource' = None
        self.set_data(data)
        self.add_item(self)

    def set_data(self, data):
        self._set_data(data)

    def _set_data(self, data):
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.level = data.get('level', None)
        self.type = data.get('type', None)
        self.subtype = data.get('subtype', None)
        self.description = data.get('description', None)
        self.effects = data.get('effects', None)
        self.craft = data.get('craft', None)
        self.tradeable = data.get('tradeable', None)

    @staticmethod
    def add_item(item):
        Item.items[item.code] = item

    @staticmethod
    def get_item(code):
        return Item.items[code]

    def __repr__(self):
        return self.name
