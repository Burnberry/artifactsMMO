from data_wrappers.data.badge_data import badge_data


class _Badge:
    badges = {}
    
    def __init__(self, data):
        self.data = data
        
        self.set_data(data)
        _Badge.badges[self.code] = self
        
    def __repr__(self):
        return self.code
        
    def set_data(self, data):
        self._set_data(data)
    
    ##### AUTO-GENERATED SECTION #####
    # annotate with # custom if you don't want code to be overwritten
    
    def _set_data(self, data):
        # _set_data start
        self.code = data.get('code', None)
        self.season = data.get('season', None)
        self.description = data.get('description', None)
        self.conditions = data.get('conditions', None)
        # _set_data end
        

class Badge(_Badge):
    @staticmethod
    def get(key) -> _Badge:
        return _Badge.badges.get(key)
    
    @staticmethod
    def all() -> list[_Badge]:
        return list(_Badge.badges.values())
        
    # auto-attrs start
    season2_bronze = _Badge(badge_data.get('season2_bronze', {}))
    season2_silver = _Badge(badge_data.get('season2_silver', {}))
    season2_gold = _Badge(badge_data.get('season2_gold', {}))
    season2_color = _Badge(badge_data.get('season2_color', {}))
    season3_bronze = _Badge(badge_data.get('season3_bronze', {}))
    season3_silver = _Badge(badge_data.get('season3_silver', {}))
    season3_gold = _Badge(badge_data.get('season3_gold', {}))
    season3_color = _Badge(badge_data.get('season3_color', {}))
    founder = _Badge(badge_data.get('founder', {}))
    gold_founder = _Badge(badge_data.get('gold_founder', {}))
    vip_founder = _Badge(badge_data.get('vip_founder', {}))
    season4_bronze = _Badge(badge_data.get('season4_bronze', {}))
    season4_silver = _Badge(badge_data.get('season4_silver', {}))
    season4_gold = _Badge(badge_data.get('season4_gold', {}))
    season4_color = _Badge(badge_data.get('season4_color', {}))
    # auto-attrs end
  