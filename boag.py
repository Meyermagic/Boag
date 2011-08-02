#!/usr/bin/env python2

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        if isinstance(other, tuple):
            return Vector(self.x + other[0], self.y + other[1])
        return Vector(self.x + other.x, self.y + other.y)
    def __iadd__(self, other):
        if isinstance(other, tuple):
            return Vector(self.x + other[0], self.y + other[1])
        return Vector(self.x + other.x, self.y + other.y)
    def __str__(self):
        return str((self.x, self.y))
    def __repr__(self):
        return repr((self.x, self.y))
    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

class Entity(object):
    def __init__(self, position):
        self.position = position
        self.tentative = None
    def act(self, entities):
        return ("move", Vector(0, 0))

class Bullet(Entity):
    def __init__(self, position, direction):
        self.direction = direction
        self.type = "bullet"
        super(Bullet, self).__init__(self, position)
    def act(self, entities):
        return ("move", self.direction)

class Player(Entity):
    def __init__(self, position, ammo=128):
        self.type = "player"
        self.ammo = ammo
        super(Player, self).__init__(self, position)

class Arena(object):
    def __init__(self, size, player1, player2):
        self.size = size
        self.entities = [player1(Vector(0, 0)), player2(size + (-1, -1))]
    def check_valid(self):
        pass
    def check_win(self):
        pass
    def valid_act(self, action, param):
        if not action in ["move", "fire"]:
            return False
        #No standing still, I guess
        if not param in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            return False
        return True
    #Return False if game over
    def step(self):
        #Grab each entity's planned action
        for entity in self.entities:
            entity.tentative = entity.act(self.entities)
        
        #Actually implement the actions
        for entity in self.entities:
            action, param = entity.tentative
            if not self.valid_act(action, param):
                print "Invalid Action:", action, param
                return False
            if action == "fire":
                if entity.ammo <= 0:
                    print "Player tried to fire with no ammo"
                    return False
                #Drop by 1 ammo
                entity.ammo -= 1
                #Spawn a new bullet
                self.entities.append(Bullet(entity.position + param, param))
            elif action == "move":
                entity.position += param











