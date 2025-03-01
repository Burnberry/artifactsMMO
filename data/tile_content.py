class TileContent:
    tile_contents: dict[str: 'TileContent'] = {}

    def __init__(self, data):
        self._set_data(data)
        self.add_tile_content(self)
        self.tiles: list['Tile'] = []

    def _set_data(self, data):
        self.__set_data(data)
        self.monster: 'Monster' = None
        self.npc: 'Npc' = None
        self.resource: 'Resource' = None

    @staticmethod
    def add_tile_content(monster):
        TileContent.tile_contents[monster.code] = monster

    @staticmethod
    def get_tile_content(code):
        return TileContent.tile_contents[code]

    def __repr__(self):
        return '%s.%s' % (self.type, self.code)

    def __set_data(self, data):
        self.code = data.get('code', None)
        self.type = data.get('type', None)
