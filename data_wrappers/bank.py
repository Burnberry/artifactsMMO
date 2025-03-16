from data_wrappers.item import Item


class Bank:
    def __init__(self, data):
        self.data = data
        self.slots = None
        self.expansions = None
        self.next_expansion_cost = None
        self.gold = None
        self.inventory: dict[Item, int] = {}
        self.slots_used = 0
        self.slots_free = 0

    def __repr__(self):
        return "Bank %s/%s" % (self.slots_used, self.slots_used)

    def set_data(self, data):
        self._set_data(data)
        if self.slots:
            self.slots_used = self.slots - len(self.inventory)
            self.slots_free = self.slots - self.slots_used

    def _set_data(self, data):
        if isinstance(data, list):
            self.inventory = {Item.get(vals['code']): vals['quantity'] for vals in data}
        else:
            self.slots = data.get('slots', None)
            self.expansions = data.get('expansions', None)
            self.next_expansion_cost = data.get('next_expansion_cost', None)
            self.gold = data.get('gold', None)
