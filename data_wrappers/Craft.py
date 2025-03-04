from typing import Optional


class Craft:
    crafts = {}

    def __init__(self, data, item, materials):
        from data_wrappers.item import Item
        self.item: Item = item
        self.materials: list[(Item, int)] = materials
        self.material_count = None

        self.skill = data.get('skill', None)
        self.level = data.get('level', None)
        self.quantity = data.get('quantity', None)

        self.add_craft(self)

    def update_material_count(self):
        self.material_count = sum([qty for item, qty in self.materials])

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
