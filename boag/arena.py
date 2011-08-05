from boag.vector import Vector
from boag.bullet import Bullet

class Arena(object):
    def __init__(self, size, team_a, team_b):
        self.size = Vector(0, 0) + size
        
        self.team_a = team_a
        self.team_b = team_b
        
        self.team_a.color = (0, 255, 0)
        self.team_b.color = (255, 0, 0)
        
        self.team_a.initialize_players(self.size, 0)
        self.team_b.initialize_players(self.size, self.size.x - 1)
        
        self.entities = team_a.players + team_b.players
    
    #Removes entities outside of playing area
    def prune(self):
        pruned = []
        for entity in self.entities:
            if entity.position.x >= 0 and entity.position.y >= 0 and entity.position.x < self.size.x and entity.position.y < self.size.y:
                pruned.append(entity)
        self.entities = pruned
    
    #Copied from the player class, in case they don't check themselves
    def is_valid_plan(self, entity):
        action, direction = entity.tentative
        if action == "fire":
            if direction in [(0, 1), (0, -1), (1, 0), (-1, 0)] and entity.ammo > 0:
                return True
            print action, direction, entity.position
            return False
        elif action == "move":
            if not direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                return False
            t = entity.position + direction
            if t.x >= 0 and t.y >= 0 and t.x < self.size.x and t.y < self.size.y:
                return True
        elif action == "pass":
            #If passing is allowed, have this return True
            return False
        return False
    
    #Returns (Is Game Over, Winner (0 for stalemate))
    def check_gameover(self):
        if not self.team_a.has_living():
            if self.team_b.has_living():
                return True, self.team_b.team_number
            return True, 0
        if not self.team_b.has_living():
            if self.team_a.has_living():
                return True, self.team_a.team_number
            return True, 0
        if self.team_a.count_ammo() + self.team_b.count_ammo() == 0:
            return True, 0
        return False, None
    
    #Play another turn of the game
    def step(self):
        #Iterate through all entities and grab their actions for this turn
        for entity in self.entities:
            entity.tentative = entity.act(self.entities)
            
            #We probably shouldn't use assert for this
            if entity.type == "player":
                assert self.is_valid_plan(entity)
        
        #New entities created in this turn
        births = []
        
        #Actually enact the tentative actions we grabbed last time
        for entity in self.entities:
            action, direction = entity.tentative
            
            if action == 'fire':
                entity.ammo -= 1
                births.append(Bullet(entity.position + direction, direction))
            elif action == 'move':
                entity.position += direction
            elif action == 'pass':
                pass
        
        #Add new entities into the entity list
        self.entities += births
        
        #Remove out-of-play bullets
        self.prune()
        
        #Kill players who have collided with bullets
        bullet_positions = []
        bullets = []
        players = []
        
        for entity in self.entities:
            if entity.type == "bullet":
                bullet_positions.append(Vector(0, 0) + entity.position)
                bullets.append(entity)
            elif entity.type == "player":
                players.append(entity)
        
        living_players = []
        
        for player in players:
            if Vector(0, 0) + player.position in bullet_positions:
                player.alive = False
            else:
                living_players.append(player)
        
        self.entities = bullets + living_players
        
        #Check for game-ending conditions
        gamestate = self.check_gameover()
        if gamestate[0]:
            return False
        return True
