import os
import random
from random import randint
import pygame

class Player(object):
	def __init__(self):
		self.score = 0
		self.dy = 20
		self.rect = pygame.Rect(200,200,20,20)

	def move(self):
		self.rect.y -= round(self.dy)

		for pipe in pipes:
			if self.rect.colliderect(pipe.rect):
				if pipe.type == 1:
					game.running = False
				if pipe.type == 1:
					player.score + 1
					pipes.remove(pipe)

class Pipe(object):
	def __init__(self, limit, direction):
		pipes.append(self)
		if direction == 1:
			self.rect = pygame.Rect(800,-2000,20,limit+2000)
			self.colour = (255,255,255)
			self.type = 1
		if direction == 2:
			self.rect = pygame.Rect(800,limit,20,800)
			self.colour = (255,255,255)
			self.type = 1
		if direction == 3:
			self.rect = pygame.Rect(800,limit,20,120)
			self.colour = (20,0,0)
			self.type = 2

	def move(self):
		self.rect.x -= 4

		if self.rect.right < -200:
			pipes.remove(self)


class Game(object):
	def __init__(self):
		self.running = True

pygame.init()

screen = pygame.display.set_mode((800,400))

game = Game()
player = Player()
pipes = []

clock = pygame.time.Clock()
playtime = 0
FPS = 60
score = 0
lastpipe = 0

while game.running == True:
	milliseconds = clock.tick(FPS)
	playtime += milliseconds / 1000.0

	for key in pygame.event.get():
		if key.type == pygame.QUIT:
			game.running = False
		if key.type == pygame.KEYDOWN:
			if key.key == pygame.K_ESCAPE:
				game.running = False
			if key.key == pygame.K_UP:
				player.dy = 12

	if lastpipe < playtime:
		centre = randint(80,320)
		toppipe = centre - 60
		bottompipe = centre + 60
		Pipe(toppipe,1)
		Pipe(bottompipe,2)
		Pipe(toppipe,3)
		lastpipe = playtime + 1.

	player.dy -= 1

	player.move()

	print(len(pipes))

	for pipe in pipes:
		pipe.move()

	screen.fill((0,0,0))
	for pipe in pipes:
		pygame.draw.rect(screen, pipe.colour, pipe.rect)
	pygame.draw.rect(screen, (255,255,0), player.rect)

	pygame.display.set_caption('Flappy Bird -- Score: {}'.format(round(player.score)))
	pygame.display.flip()
