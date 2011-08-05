from boag.player import Player
from boag.vector import Vector
from random import choice, randint, shuffle
from itertools import product

class RandomWalker(Player):
    def act(self, entities):
        possible = product(["fire", "move"], [(0, 1), (0, -1), (-1, 0), (1, 0)])
        legal = filter(self.is_legal, possible)
        return choice(legal)

class PlayItSafe(Player):
    #Might not lead to death (assumes is_legal)
    def is_viable(self, move):
        players, bullets = self.entity_sort(self.states['current'])
        action, direction = move
        if action == 'fire':
            direction = Vector(0, 0)
        test_pos = self.position + direction
        for bullet in bullets:
            if bullet.position + bullet.direction == test_pos:
                return False
        return True
    #Will not lead to death of self (except for friendly fire) (assumes is_viable)
    def is_safe(self, move):
        players, bullets = self.entity_sort(self.states['current'])
        allies, enemies = self.player_sort(players)
        
        action, direction = move
        if action == 'fire':
            direction = Vector(0, 0)
            
        test_pos = self.position + direction
        
        for enemy in enemies:
            for adj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if test_pos == enemy.position + adj:
                    return False
        return True
    #Will not lead to teammate death (assumes is_safe)
    def is_safe_team(self, move):
        players, bullets = self.entity_sort(self.states['current'])
        allies, enemies = self.player_sort(players)
        
        action, direction = move
        if action == 'move':
            return True
            
        test_pos = self.position + direction
        
        for ally in allies:
            for adj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if test_pos == ally.position + adj:
                    return False
        return True
    def act(self, entities):
        self.states["current"] = entities
        possible = product(["fire", "move"], [(0, 1), (0, -1), (-1, 0), (1, 0)])
        legal = filter(self.is_legal, possible)
        viable = filter(self.is_viable, legal)
        safe = filter(self.is_safe, viable)
        team_safe = filter(self.is_safe_team, safe)
        choices = []
        if len(team_safe) != 0:
            choices = team_safe
        elif len(safe) != 0:
            choices = safe
        elif len(viable) != 0:
            choices = viable
        else:
            #If there are no viable moves, then we should surrender.
            #return ("surrender", None)
            choices = legal
        #Pick best move out of choices
        return choice(choices)
