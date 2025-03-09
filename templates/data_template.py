data_template = """from data_wrappers_test.data import %s_data


class _%s:
    %ss = {}
    
    def __init__(self, data):
        self.data = data
        
        self.set_data(data)
        _%s.%ss[self.%s] = self
        
    def __repr__(self):
        return self.%s
        
    def set_data(self, data):
        self._set_data(data)
    
    ##### AUTO-GENERATED SECTION #####
    # annotate with # custom if you don't want code to be overwritten
    
    def _set_data(self, data):
        # _set_data start
        pass
        # _set_data end
        

class %s:
    @staticmethod
    def get(key):
        return _%s.%ss.get(key)
    
    @staticmethod
    def all():
        return list(_%s.%ss.values())
        
    # auto-attrs start
    
    # auto-attrs end
    """
