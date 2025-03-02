from data_wrappers.drop import Drop


class Drops:
    drops = {}

    def __init__(self, data, source):
        if isinstance(data, list):
            vals_list = data
        else:
            vals_list = data['items']
        self.drops = [Drop(vals) for vals in vals_list]
        self.source = source
        self.add_drops(self, source)

    @staticmethod
    def add_drops(drops, source):
        Drops.drops[source] = drops

    @staticmethod
    def get_drops(source):
        Drops.drops.get(source)
