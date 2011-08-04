

class Team(object):
    team_number = 0
    def __init__(self, players):
        self.players = players
        self.player_count = len(players)
        Team.team_number += 1
        self.team_number = Team.team_number
