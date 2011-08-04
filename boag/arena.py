from boag.vector import Vector
from boag.bullet import Bullet

class Arena(object):
    def __init__(self, size, player1, player2):
        self.size = size
        self.entities = [player1(Vector(0, 0), size), player2(size - (1, 1), size)]
    def sort(self, entities):
        players = []
        bullets = []
        for entity in entities:
            if entity.type == "bullet":
                bullets.append(entity)
            elif entity.type == "player":
                players.append(entity)
        return players, bullets
    def check_valid(self):
        return True
    def check_win(self):
        players, bullets = self.sort(self.entities)
        gameover = False
        for player in players:
            for bullet in bullets:
                if player.position == bullet.position:
                    print "Player", player.player_number, "lost at", bullet.position
                    gameover = True
        return gameover
    def valid_act(self, action, param):
        if not action in ["move", "fire"]:
            return False
        #No standing still, I guess
        if not param in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            return False
        return True
    def prune(self):
        pruned = []
        for entity in self.entities:
            if entity.position.x >= 0 and entity.position.y >= 0 and entity.position.x < self.size.x and entity.position.y < self.size.y:
                pruned.append(entity)
        self.entities = pruned
    #Return False if game over
    def step(self):
        #Grab each entity's planned action
        for entity in self.entities:
            entity.tentative = entity.act(self.entities)
            if entity.type == "player":
                print "Player", entity.player_number, entity.tentative, "at", entity.position, "with", entity.ammo, "shots remaining."
        births = []
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
                births.append(Bullet(entity.position + param, param))
            elif action == "move":
                entity.position += param
        self.entities += births
        self.prune()
        if not self.check_valid():
            return False
        return not self.check_win()
