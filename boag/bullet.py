from boag.entity import Entity

class Bullet(Entity):
    def __init__(self, position, direction):
        super(Bullet, self).__init__(position)
        self.type = "bullet"
        self.direction = direction
        self.color = (255, 255, 255)
    def act(self, entities):
        return ("move", self.direction)
