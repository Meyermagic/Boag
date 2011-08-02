#!/usr/bin/env python2
import pygame
from pygame.locals import *
from time import sleep
from vector import Vector


class Entity(object):
    def __init__(self, position):
        self.position = position
        self.tentative = None
    def act(self, entities):
        return ("move", Vector(0, 0))

class Bullet(Entity):
    def __init__(self, position, direction):
        self.direction = direction
        self.type = "bullet"
        super(Bullet, self).__init__(position)
    def act(self, entities):
        return ("move", self.direction)

class Player(Entity):
    player_number = 0
    def __init__(self, position, world, ammo=256):
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
            if t.x >= 0 and t.y >= 0 and t.x < size.x and t.y < size.y:
                return True
        return False

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
    #Return False if game over
    def step(self):
        #Grab each entity's planned action
        for entity in self.entities:
            entity.tentative = entity.act(self.entities)
            if entity.type == "player":
                print "Player", entity.player_number, entity.tentative, "at", entity.position
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
        if not self.check_valid():
            return False
        return not self.check_win()

class PlayerA(Player):
    def act(self, entities):
        players, bullets = self.sort(entities)
        enemy = players[0]
        if self.position.x != enemy.position.x:
            return ("move", ((enemy.position - self.position).direction().x, 0))
        return ("fire", (enemy.position - self.position).direction())

class PlayerB(Player):
    def act(self, entities):
        players, bullets = self.sort(entities)
        return ("fire", (-1, 0))
        

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
    game = Arena(Vector(20, 20), PlayerA, PlayerB)
    turns = 0
    while game.step():
        turns += 1
        print "Round", turns, "complete."
        draw(game, screen)
        sleep(1)
    print "Game over in", turns + 1, "rounds."




