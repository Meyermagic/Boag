#!/usr/bin/env python
#Might want python2 here instead.
import pygame
from pygame.locals import *
from pygame.time import Clock
from boag.arena import Arena
from boag.ai import CornerAttacker, PlayItSafe
from boag.vector import Vector

def draw(arena, screen):
	new = pygame.Surface((arena.size.x, arena.size.y))
	for entity in arena.entities:
		if entity.type == "player":
			new.set_at(entity.position.to_tuple(), (255, 0, 0))
		else:
			new.set_at(entity.position.to_tuple(), (255, 255, 255))
	screen.blit(pygame.transform.scale(new, screen.get_size()), (0, 0))
	pygame.display.update()

if __name__ == "__main__":
	pygame.init()
	size = (800, 800)
	screen = pygame.display.set_mode(size)
	game = Arena(Vector(20, 20), CornerAttacker, PlayItSafe)
	clock = Clock()
	turns = 0
	running = True
	while game.step() and running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		turns += 1
		print "Round", turns, "complete."
		draw(game, screen)
		clock.tick(20)
	pygame.quit()
	print "Game over in", turns + 1, "rounds."



