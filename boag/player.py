from boag.entity import Entity

class Player(Entity):
    player_number = 0
    def __init__(self, position, world, ammo=1024):
        Player.player_number += 1
        self.player_number = Player.player_number
        self.type = "player"
        self.ammo = ammo
        self.states = dict()
        self.world = world
        super(Player, self).__init__(position)
    def sort(self, entities):
        other_players = []
        bullets = []
        for entity in entities:
            if entity.type == "bullet":
                bullets.append(entity)
            elif entity.type == "player" and not entity is self:
                other_players.append(entity)
        return other_players, bullets
    #Returns True if move is legal (checks bullet count and boundaries)
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
            if t.x >= 0 and t.y >= 0 and t.x < self.world.x and t.y < self.world.y:
                return True
        return False
