class Tile:
    tiles = {}

    def __init__(self, data):
        self._set_data(data)
        self.add_tile(self)

    def _set_data(self, data):
        self.__set_data(data)

    @staticmethod
    def add_tile(tile):
        Tile.tiles[(tile.x, tile.y)] = tile

    @staticmethod
    def get_tile(x, y):
        return Tile.tiles[(x, y)]

    @staticmethod
    def inside(x, y):
        return (x, y) in Tile.tiles

    def __repr__(self):
        return "%s, %s - %s - %s" % (self.x, self.y, self.name, self.content)

    def __set_data(self, data):
        self.name = data.get('name', None)
        self.skin = data.get('skin', None)
        self.x = data.get('x', None)
        self.y = data.get('y', None)
        self.content = data.get('content', None)
