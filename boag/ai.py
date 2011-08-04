from boag.player import Player
from boag.vector import Vector
from random import choice, randint, shuffle
from itertools import product

class PlayerA(Player):
    def act(self, entities):
        players, bullets = self.sort(entities)
        enemy = players[0]
        if self.position.x != enemy.position.x:
            return ("move", ((enemy.position - self.position).direction().x, 0))
        return ("fire", (enemy.position - self.position).direction())

class PlayerB(Player):
    def act(self, entities):
        players, bullets = self.sort(entities)
        return ("fire", (-1, 0))

class PlayItSafe(Player):
    #Returns True if move might not lead to death on next turn (checks bullets)
    def is_viable(self, move):
        #Assumes move is legal.
        enemy, bullets = self.sort(self.states["current"])
        enemy = enemy[0]
        action, direction = move
        #Firing doesn't move us
        if action == "fire":
            direction = Vector(0, 0)
        test_pos = self.position + direction
        #Make sure we don't hit a bullet
        for bullet in bullets:
            if bullet.position + bullet.direction == test_pos:
                return False
        return True
    #Returns True if move can't lead to death on next turn (is viable + enemy adjacency)
    def is_safe(self, move):
        #Assumes move is viable
        enemy, bullets = self.sort(self.states["current"])
        enemy = enemy[0]
        action, direction = move
        if action == "fire":
            direction = Vector(0, 0)
        test_pos = self.position + direction
        for adj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if enemy.position + adj == test_pos:
                return False
        return True
    def act(self, entities):
        possible = product(["fire", "move"], [(0, 1), (0, -1), (-1, 0), (1, 0)])
        self.states["current"] = entities
        legal = filter(self.is_legal, possible)
        viable = filter(self.is_viable, legal)
        safe = filter(self.is_safe, viable)
        choices = []
        if len(safe) != 0:
            choices = safe
        elif len(viable) != 0:
            choices = viable
        else:
            #If there are no viable moves, then we should surrender.
            #return ("surrender", None)
            choices = legal
        #Pick best move out of choices
        return choice(choices)

class SafeAndAttack(PlayItSafe):
    def act(self, entities):
        possible = product(["fire", "move"], [(0, 1), (0, -1), (-1, 0), (1, 0)])
        self.states["current"] = entities
        legal = filter(self.is_legal, possible)
        viable = filter(self.is_viable, legal)
        safe = filter(self.is_safe, viable)
        choices = []
        if len(safe) != 0:
            choices = safe
#            if randint(1, 100) == 1:
#                return choice(choices)
        elif len(viable) != 0:
            choices = viable
        else:
            #If there are no viable moves, then we should surrender.
            #return ("surrender", None)
            choices = legal
        enemy, bullets = self.sort(entities)
        enemy = enemy[0]
        if enemy.position.x == self.position.x or enemy.position.y == self.position.y:
            tent = ("fire", (enemy.position - self.position).direction())
            if tent in choices:
                return tent
        else:
            diffx = abs(enemy.position.x - self.position.x)
            diffy = abs(enemy.position.y - self.position.y)
            if diffx <= diffy and diffx != 0:
                tent = ("move", ((enemy.position - self.position).direction().x, 0))
                if tent in choices:
                    return tent
            else:
                tent = ("move", (0, (enemy.position - self.position).direction().y))
                if tent in choices:
                    return tent
        return choice(choices)

class CloseInAttack(PlayItSafe):
    def act(self, entities):
        possible = [('fire', (0, 1)), ('fire', (0, -1)), ('fire', (-1, 0)), ('fire', (1, 0)), ('move', (0, 1)), ('move', (0, -1)), ('move', (-1, 0)), ('move', (1, 0))]
        self.states["current"] = entities
        legal = filter(self.is_legal, possible)
        viable = filter(self.is_viable, legal)
        safe = filter(self.is_safe, viable)
        choices = []
        if len(safe) != 0:
            choices = safe
        elif len(viable) != 0:
            choices = viable
        else:
            #If there are no viable moves, then we should surrender.
            #return ("surrender", None)
            choices = legal
        enemy, bullets = self.sort(entities)
        enemy = enemy[0]
        if enemy.position.x == self.position.x or enemy.position.y == self.position.y:
            tent = ("fire", (enemy.position - self.position).direction())
            if tent in choices:
                return tent
        else:
            diffx = abs(enemy.position.x - self.position.x)
            diffy = abs(enemy.position.y - self.position.y)
            if diffx >= diffy:
                tent = ("move", ((enemy.position - self.position).direction().x, 0))
                if tent in choices:
                    return tent
            else:
                tent = ("move", (0, (enemy.position - self.position).direction().y))
                if tent in choices:
                    return tent
        return choice(choices)

class CornerAttacker(PlayItSafe):
    def act(self, entities):
        possible = [('fire', (0, 1)), ('fire', (0, -1)), ('fire', (-1, 0)), ('fire', (1, 0)), ('move', (0, 1)), ('move', (0, -1)), ('move', (-1, 0)), ('move', (1, 0))]
        self.states["current"] = entities
        legal = filter(self.is_legal, possible)
        viable = filter(self.is_viable, legal)
        safe = filter(self.is_safe, viable)
        choices = []
        if len(safe) != 0:
            choices = safe
        elif len(viable) != 0:
            choices = viable
        else:
            #If there are no viable moves, then we should surrender.
            #return ("surrender", None)
            choices = legal
        enemy, bullets = self.sort(entities)
        enemy = enemy[0]
        epos = enemy.position
        corners = [epos + (1, 1), epos + (-1, -1), epos + (-1, 1), epos + (1, -1)]
        if self.position in corners:
            tcs = [("fire", ((enemy.position - self.position).direction().x, 0)), ("fire", (0, (enemy.position - self.position).direction().y))]
            shuffle(tcs)
            for tent in tcs:
                if tent in choices:
                    return tent
        else:
            corners.sort(key=lambda p: abs(p - self.position))
            target = corners[0]
            diffx = abs(target.x - self.position.x)
            diffy = abs(target.y - self.position.y)
            if diffx >= diffy:
                tent = ("move", ((target - self.position).direction().x, 0))
                if tent in choices:
                    return tent
            else:
                tent = ("move", (0, (target - self.position).direction().y))
                if tent in choices:
                    return tent
        return choice(choices)
