class Entity(object):
    def __init__(self, position):
        self.position = position
        self.tentative = None
    def act(self, entities):
        return ("move", Vector(0, 0))
