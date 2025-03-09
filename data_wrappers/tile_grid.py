from data_wrappers.tile_content import TileContent
from data_wrappers.data.tile_data import tile_data


class Grid(TileContent):
    @staticmethod
    def set_main_tiles():
        for key, vals in tile_data.items():
            if content := vals.get('content', False):
                tile_content = TileContent.get(content['code'])
                tile_content.tiles.append((vals['x'], vals['y']))
