from data_wrappers.data.task_data import task_data
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from monster import _Monster
    from item import _Item


class _Task:
    tasks = {}
    
    def __init__(self, data):
        self.data = data
        self.item: _Item = None
        self.monster: _Monster = None
        
        self.set_data(data)
        _Task.tasks[self.code] = self
        
    def __repr__(self):
        return "Task: %s.%s %s/%s - %s lv.%s - x%s coins" % (self.type, self.code, self.min_quantity, self.max_quantity, self.skill, self.level, self.rewards['items'][0]['quantity'])
        
    def set_data(self, data):
        self._set_data(data)
    
    ##### AUTO-GENERATED SECTION #####
    # annotate with # custom if you don't want code to be overwritten
    
    def _set_data(self, data):
        # _set_data start
        self.code = data.get('code', None)
        self.level = data.get('level', None)
        self.type = data.get('type', None)
        self.min_quantity = data.get('min_quantity', None)
        self.max_quantity = data.get('max_quantity', None)
        self.skill = data.get('skill', None)
        self.rewards = data.get('rewards', None)
        # _set_data end
        

class Task(_Task):
    @staticmethod
    def get(key) -> _Task:
        return _Task.tasks.get(key)
    
    @staticmethod
    def all() -> list[_Task]:
        return list(_Task.tasks.values())
        
    # auto-attrs start
    chicken = _Task(task_data.get('chicken', {}))
    copper_ore = _Task(task_data.get('copper_ore', {}))
    ash_wood = _Task(task_data.get('ash_wood', {}))
    sunflower = _Task(task_data.get('sunflower', {}))
    copper = _Task(task_data.get('copper', {}))
    small_health_potion = _Task(task_data.get('small_health_potion', {}))
    ash_plank = _Task(task_data.get('ash_plank', {}))
    gudgeon = _Task(task_data.get('gudgeon', {}))
    cooked_gudgeon = _Task(task_data.get('cooked_gudgeon', {}))
    yellow_slime = _Task(task_data.get('yellow_slime', {}))
    green_slime = _Task(task_data.get('green_slime', {}))
    blue_slime = _Task(task_data.get('blue_slime', {}))
    red_slime = _Task(task_data.get('red_slime', {}))
    cow = _Task(task_data.get('cow', {}))
    mushmush = _Task(task_data.get('mushmush', {}))
    iron_ore = _Task(task_data.get('iron_ore', {}))
    spruce_wood = _Task(task_data.get('spruce_wood', {}))
    iron = _Task(task_data.get('iron', {}))
    spruce_plank = _Task(task_data.get('spruce_plank', {}))
    shrimp = _Task(task_data.get('shrimp', {}))
    cooked_shrimp = _Task(task_data.get('cooked_shrimp', {}))
    flying_serpent = _Task(task_data.get('flying_serpent', {}))
    wolf = _Task(task_data.get('wolf', {}))
    highwayman = _Task(task_data.get('highwayman', {}))
    skeleton = _Task(task_data.get('skeleton', {}))
    pig = _Task(task_data.get('pig', {}))
    ogre = _Task(task_data.get('ogre', {}))
    coal = _Task(task_data.get('coal', {}))
    birch_wood = _Task(task_data.get('birch_wood', {}))
    nettle_leaf = _Task(task_data.get('nettle_leaf', {}))
    steel = _Task(task_data.get('steel', {}))
    hardwood_plank = _Task(task_data.get('hardwood_plank', {}))
    trout = _Task(task_data.get('trout', {}))
    cooked_trout = _Task(task_data.get('cooked_trout', {}))
    spider = _Task(task_data.get('spider', {}))
    vampire = _Task(task_data.get('vampire', {}))
    cyclops = _Task(task_data.get('cyclops', {}))
    death_knight = _Task(task_data.get('death_knight', {}))
    imp = _Task(task_data.get('imp', {}))
    owlbear = _Task(task_data.get('owlbear', {}))
    gold_ore = _Task(task_data.get('gold_ore', {}))
    dead_wood = _Task(task_data.get('dead_wood', {}))
    gold = _Task(task_data.get('gold', {}))
    dead_wood_plank = _Task(task_data.get('dead_wood_plank', {}))
    bass = _Task(task_data.get('bass', {}))
    cooked_bass = _Task(task_data.get('cooked_bass', {}))
    cultist_acolyte = _Task(task_data.get('cultist_acolyte', {}))
    goblin = _Task(task_data.get('goblin', {}))
    strange_ore = _Task(task_data.get('strange_ore', {}))
    magic_wood = _Task(task_data.get('magic_wood', {}))
    strangold = _Task(task_data.get('strangold', {}))
    magical_plank = _Task(task_data.get('magical_plank', {}))
    bat = _Task(task_data.get('bat', {}))
    lich = _Task(task_data.get('lich', {}))
    goblin_wolfrider = _Task(task_data.get('goblin_wolfrider', {}))
    hellhound = _Task(task_data.get('hellhound', {}))
    mithril_ore = _Task(task_data.get('mithril_ore', {}))
    maple_wood = _Task(task_data.get('maple_wood', {}))
    glowstem_leaf = _Task(task_data.get('glowstem_leaf', {}))
    mithril = _Task(task_data.get('mithril', {}))
    maple_plank = _Task(task_data.get('maple_plank', {}))
    salmon = _Task(task_data.get('salmon', {}))
    cooked_salmon = _Task(task_data.get('cooked_salmon', {}))
    # auto-attrs end
  