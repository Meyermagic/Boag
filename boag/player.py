from boag.entity import Entity

class Player(Entity):
    player_number = 0
    def __init__(self, position, board_size, initial_ammo=1024):
        super(Player, self).__init__(position)
        Player.player_number += 1
        
        #Constant
        self.type = "player"
        
        #Per-game
        self.player_number = Player.player_number
        self.color = (0, 0, 255)
        self.team = None
        
        #Dynamic
        self.ammo = initial_ammo
        self.alive = True
        self.states = dict()
        self.board_size = board_size
    
    def set_team(self, team):
        self.team = team
        self.color = team.color
    
    def is_legal(self, move):
        action, direction = move
        if action == "fire":
            if direction in [(0, 1), (0, -1), (1, 0), (-1, 0)] and self.ammo > 0:
                return True
            return False
        elif action == "move":
            if not direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                return False
            t = self.position + direction
            if t.x >= 0 and t.y >= 0 and t.x < self.board_size.x and t.y < self.board_size.y:
                return True
        return False
    
    def entity_sort(self, entities):
        players = []
        bullets = []
        for entity in entities:
            if entity.type == "bullet":
                bullets.append(entity)
            elif entity.type == "player" and not entity is self:
                players.append(entity)
        return players, bullets
    
    def player_sort(self, players):
        teammates = []
        enemies = []
        for player in players:
            if player.team is self.team:
                if not player is self:
                    teammates.append(player)
            else:
                enemies.append(player)
        return teammates, enemies

