class Event:
    events = {}

    def __init__(self, data):
        self._set_data(data)
        self.add_event(self)

    def _set_data(self, data):
        self.__set_data(data)

    @staticmethod
    def add_event(event):
        Event.events[event.code] = event

    @staticmethod
    def get_event(code):
        return Event.events[code]

    def __repr__(self):
        return self.name

    def __set_data(self, data):
        self.name = data.get('name', None)
        self.code = data.get('code', None)
        self.maps = data.get('maps', None)
        self.skin = data.get('skin', None)
        self.duration = data.get('duration', None)
        self.rate = data.get('rate', None)
        self.content = data.get('content', None)
