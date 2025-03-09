from data_wrappers.data.task_reward_data import task_reward_data


class _TaskReward:
    task_rewards = {}
    
    def __init__(self, data):
        self.data = data
        
        self.set_data(data)
        _TaskReward.task_rewards[self.code] = self
        
    def __repr__(self):
        return self.code
        
    def set_data(self, data):
        self._set_data(data)
    
    ##### AUTO-GENERATED SECTION #####
    # annotate with # custom if you don't want code to be overwritten
    
    def _set_data(self, data):
        # _set_data start
        self.code = data.get('code', None)
        self.rate = data.get('rate', None)
        self.min_quantity = data.get('min_quantity', None)
        self.max_quantity = data.get('max_quantity', None)
        # _set_data end
        

class TaskReward(_TaskReward):
    @staticmethod
    def get(key) -> _TaskReward:
        return _TaskReward.task_rewards.get(key)
    
    @staticmethod
    def all() -> list[_TaskReward]:
        return list(_TaskReward.task_rewards.values())
        
    # auto-attrs start
    magical_cure = _TaskReward(task_reward_data.get('magical_cure', {}))
    jasper_crystal = _TaskReward(task_reward_data.get('jasper_crystal', {}))
    astralyte_crystal = _TaskReward(task_reward_data.get('astralyte_crystal', {}))
    enchanted_fabric = _TaskReward(task_reward_data.get('enchanted_fabric', {}))
    small_bag_of_gold = _TaskReward(task_reward_data.get('small_bag_of_gold', {}))
    bag_of_gold = _TaskReward(task_reward_data.get('bag_of_gold', {}))
    ruby = _TaskReward(task_reward_data.get('ruby', {}))
    sapphire = _TaskReward(task_reward_data.get('sapphire', {}))
    emerald = _TaskReward(task_reward_data.get('emerald', {}))
    topaz = _TaskReward(task_reward_data.get('topaz', {}))
    diamond = _TaskReward(task_reward_data.get('diamond', {}))
    # auto-attrs end
  