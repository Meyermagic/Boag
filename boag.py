#!/usr/bin/env python
#Might want python2 here instead.
import pygame
from pygame.locals import *
from pygame.time import Clock

#Game imports
from boag.tournament import Tournament
from boag.team import Team
from boag.ai import PlayItSafe, RandomWalker
from boag.vector import Vector

def draw(arena, screen):
    new = pygame.Surface((arena.size.x, arena.size.y))
    for entity in arena.entities:
        new.set_at(entity.position.to_tuple(), entity.color)
    screen.blit(pygame.transform.scale(new, screen.get_size()), (0, 0))
    pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    
    teams = []
    
    teams.append(Team([PlayItSafe] * 4))
    teams.append(Team([PlayItSafe] * 4))
    tournament = Tournament(teams, Vector(40, 40))
    
    clock = Clock()
    
    for game in tournament.games:
        turns = 0
        while game.step():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            turns += 1
            print "Round %d complete." % turns
            print "Team A: %d alive, %d shots remaining." % (game.team_a.count_living(), game.team_a.count_ammo())
            print "Team B: %d alive, %d shots remaining." % (game.team_b.count_living(), game.team_b.count_ammo())
            draw(game, screen)
            clock.tick(20)
        print "Game over in %d rounds." % (turns + 1)
    
    pygame.quit()

