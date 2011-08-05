from operator import methodcaller
from boag.vector import Vector

class Team(object):
    team_number = 0
    def __init__(self, players, color=(0, 0, 255)):
        Team.team_number += 1
        
        #Per-game
        self.player_classes = players
        self.players = None
        self.player_count = len(players)
        self.team_number = Team.team_number
        self.color = color
        
        #Dynamic
        self.states = dict()
    
    def initialize_players(self, board_size, x_pos):
        #Initialize players to (0, 0)
        initializer = methodcaller('__call__', Vector(0, 0), board_size)
        self.players = map(initializer, self.player_classes)
        
        #Calculate space between players
        spacing = float(board_size.y - 1) / (self.player_count - 1)
        offset = 0
        
        #Set player teams and positions
        for player in self.players:
            player.set_team(self)
            player.position = Vector(x_pos, int(offset))
            offset += spacing
    
    def has_living(self):
        for player in self.players:
            if player.alive:
                return True
        return False
    
    def count_ammo(self):
        total = 0
        for player in self.players:
            if player.alive:
                total += player.ammo
        return total
