from data.tile import Tile
from data.tile_data import tile_data


class Grid:
    tiles = {key: Tile(tile_data[key]) for key in tile_data}

    @staticmethod
    def inside(x, y):
        return (x, y) in Grid.tiles

    @staticmethod
    def get_tile(x, y):
        return Grid.tiles[(x, y)]
