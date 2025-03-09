from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from item import _Item


class Drop:
    drops = set()

    def __init__(self, vals):
        self.item: _Item = None
        self.code = vals.get('code', None)
        self.rate = vals.get('rate', None)
        self.min_quantity = vals.get('min_quantity', None)
        self.max_quantity = vals.get('max_quantity', None)

        Drop.drops.add(self)

    def __repr__(self):
        return self.code


class Drops:
    drops = set()

    def __init__(self, vals, source):
        self.source = source
        self.min_coins = vals.get('min_coins', 0)
        self.max_coins = vals.get('max_coins', 0)
        self.drops: list[Drop] = [Drop(drop_vals) for drop_vals in vals.get('drops', [])]
