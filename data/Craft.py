class Craft:
    crafts = {}

    def __init__(self, data, item, materials):
        from data.item import Item
        self.item: Item = item
        self.materials = materials

        self.skill = data.get('skill', None)
        self.level = data.get('level', None)
        self.quantity = data.get('quantity', None)

    @staticmethod
    def add_craft(craft):
        Craft.crafts[craft.item.code] = craft

    @staticmethod
    def get_craft(code):
        Craft.crafts.get(code)

    def __repr__(self):
        materials = ""
        for mat, qty in self.materials:
            materials += "%sx %s, " % (qty, mat)
        return "Craft: %sx %s - %s lv.%s - (%s)" % (self.quantity, self.item, self.skill, self.level, materials[:-2])
