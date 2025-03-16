import datetime
from private.config import config


def get_api_key():
    if not (key := config.get('key', None)):
        print("Make sure to fill in the data correctly in private/config.py")
    return key


url = "https://api.artifactsmmo.com/"
headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer %s" % get_api_key()}


def dict_to_attributes(data, dict_name="data"):
    for key in data:
        print("self.%s = %s.get('%s', None)" % (key, dict_name, key))


def to_datetime(time):
    return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')


def get_nearest_tiles(tiles, x, y):
    tx, ty = tiles[0]
    tile = (tx, ty)
    d = abs(x - tx) + abs(y - ty)
    for tx, ty in tiles:
        if (td := abs(x - tx) + abs(y - ty)) < d:
            d, tile = td, (tx, ty)
    return tile


def tuple_convert(lst, values):
    """Convenience list converter, e.g. will transform:
    [item, (item, qty), item] -> [(item, qty), (item, qty), (item, qty)]
    for given default vals"""
    new_lst = []
    for obj in lst:
        if not isinstance(obj, tuple):
            obj = (obj,)
        new_lst.append(obj + values[len(obj)-1:])
    return new_lst

