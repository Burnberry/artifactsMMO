from data.npc_item_data import npc_item_data


class NpcItem:
    npc_items = {}

    def __init__(self, data):
        self._set_data(data)
        self.add_npc_item(self)

    def _set_data(self, data):
        from data.item import Item
        from data.npc import Npc
        self.item: Item = None
        self.npc: Npc = None

        self.__set_data(data)

    @staticmethod
    def add_npc_item(npc_item):
        NpcItem.npc_items[npc_item.code] = npc_item

    @staticmethod
    def get_npc_item(code):
        return NpcItem.npc_items[code]

    def __repr__(self):
        return "%s.%s" % (self.npc, self.code)

    def __set_data(self, data):
        self.code = data.get('code', None)
        self.npc = data.get('npc', None)
        self.buy_price = data.get('buy_price', None)
        self.sell_price = data.get('sell_price', None)


for code, vals in npc_item_data.items():
    NpcItem(vals)
