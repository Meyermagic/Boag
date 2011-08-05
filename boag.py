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
    
    team_1 = Team([PlayItSafe] * 3)
    team_2 = Team([PlayItSafe] * 3)
    team_3 = Team([PlayItSafe] * 3)
    tournament = Tournament([team_1, team_2, team_3], Vector(30, 30))
    
    clock = Clock()
    
    for game in tournament.games:
        turns = 0
        while game.step():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            turns += 1
            print "Round", turns, "complete."
            draw(game, screen)
            clock.tick(200)
        print "Game over in", turns + 1, "rounds."
    
    pygame.quit()

