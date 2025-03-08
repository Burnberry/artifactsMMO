data_template = """class %s:
    %s = {}
    
    def __init__(self, data):
        self.data = data
        
        self.set_data(data)
        %s.%s[self.%s] = self
        
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
        
    # auto-attrs start
    
    # auto-attrs end
    """
