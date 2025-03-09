from data_wrappers.data.event_data import event_data


class _Event:
    events = {}
    
    def __init__(self, data):
        self.data = data
        
        self.set_data(data)
        _Event.events[self.code] = self
        
    def __repr__(self):
        return self.name
        
    def set_data(self, data):
        self._set_data(data)
    
    ##### AUTO-GENERATED SECTION #####
    # annotate with # custom if you don't want code to be overwritten
    
    def _set_data(self, data):
        # _set_data start
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.maps = data.get('maps', None)
        self.skin = data.get('skin', None)
        self.duration = data.get('duration', None)
        self.rate = data.get('rate', None)
        self.content = data.get('content', None)
        # _set_data end
        

class Event(_Event):
    @staticmethod
    def get(key) -> _Event:
        return _Event.events.get(key)
    
    @staticmethod
    def all() -> list[_Event]:
        return list(_Event.events.values())
        
    # auto-attrs start
    portal_demon = _Event(event_data.get('portal_demon', {}))
    bandit_camp = _Event(event_data.get('bandit_camp', {}))
    cult_of_darkness = _Event(event_data.get('cult_of_darkness', {}))
    strange_apparition = _Event(event_data.get('strange_apparition', {}))
    magic_apparition = _Event(event_data.get('magic_apparition', {}))
    rosenblood = _Event(event_data.get('rosenblood', {}))
    portal_efreet_sultan = _Event(event_data.get('portal_efreet_sultan', {}))
    cursed_tree = _Event(event_data.get('cursed_tree', {}))
    fish_merchant = _Event(event_data.get('fish_merchant', {}))
    timber_merchant = _Event(event_data.get('timber_merchant', {}))
    herbal_merchant = _Event(event_data.get('herbal_merchant', {}))
    nomadic_merchant = _Event(event_data.get('nomadic_merchant', {}))
    gemstone_merchant = _Event(event_data.get('gemstone_merchant', {}))
    # auto-attrs end
  