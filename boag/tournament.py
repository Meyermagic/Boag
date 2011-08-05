from boag.arena import Arena
from boag.vector import Vector
from itertools import combinations, imap

class Tournament(object):
    def __init__(self, teams, size):
        self.teams = teams
        self.board_size = Vector(0, 0) + size
        self.complete = False
        self.in_game = False
        self.games = self.make_games(teams)
    def make_game(self, team_pair):
        return Arena(self.board_size, team_pair[0], team_pair[1])
    def make_games(self, teams):
        return imap(self.make_game, combinations(teams, 2))
