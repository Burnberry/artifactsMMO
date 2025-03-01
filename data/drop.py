class Drop:
    drops = set()

    def __init__(self, vals):
        self.item: 'Item' = None
        self.code = vals.get('code', None)
        self.rate = vals.get('rate', None)
        self.min_quantity = vals.get('min_quantity', None)
        self.max_quantity = vals.get('max_quantity', None)

        Drop.drops.add(self)
        
    def __repr__(self):
        return self.code
