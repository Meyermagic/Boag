from boag.entity import Entity

class Bullet(Entity):
    def __init__(self, position, direction):
        self.direction = direction
        self.type = "bullet"
        super(Bullet, self).__init__(position)
    def act(self, entities):
        return ("move", self.direction)
