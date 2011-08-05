class Entity(object):
    def __init__(self, position):
        self.position = position
        self.color = (0, 0, 0)
        self.tentative = None
    def act(self, entities):
        return ("pass", None)
