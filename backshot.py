import os
import random
from random import randint
import pygame


class Player(object):
	def __init__(self):
		players.append(self)
		number = len(players)
		self.height = 10
		self.width = 10
		self.score = 0
		self.speed = 2	
		self.rect = pygame.Rect(200,200,self.width,self.height)
		self.direction = 'NONE'
		self.dx = 0
		self.dy = 0


	def move(self):
		self.rect.x += self.dx
		self.rect.y += self.dy

		if self.rect.left > 400:
			self.rect.right = 0
		if self.rect.right < 0:
			self.rect.left = 400
		if self.rect.bottom < 0:
			self.rect.top = 400
		if self.rect.top > 400:
			self.rect.bottom = 0

		for apple in apples:
			if self.rect.colliderect(apple.rect):
				apples.remove(apple)
				self.score += 10
				Apple()
				Tail()

		for tail in tails:
			if self.rect.colliderect(tail.rect):
				game.running = False

class Tail(object):
	def __init__(self):

		tails.append(self)
		self.height = 10
		self.width = 10
		self.speed = 2
		self.dx = -2*player.dx
		self.dy = -2*player.dy
		x = player.rect.x - 5*player.dx
		y = player.rect.y - 5*player.dy
		self.rect = pygame.Rect(x,y,self.width,self.height)

	def move(self):
		self.rect.x += self.dx
		self.rect.y += self.dy

		if self.rect.left > 400:
			self.rect.right = 0
		if self.rect.right < 0:
			self.rect.left = 400
		if self.rect.bottom < 0:
			self.rect.top = 400
		if self.rect.top > 400:
			self.rect.bottom = 0

		for apple in apples:
			if self.rect.colliderect(apple.rect):
				apples.remove(apple)
				Apple()
				Tail()

class Apple(object):
	def __init__(self):
		height = 10
		width = 10
		apples.append(self)
		x = randint(2,38)*10
		y = randint(2,38)*10
		self.rect = pygame.Rect(x,y,width,height)

class Game(object):
	def __init__(self):
		self.running = True

# Initialise pygame
pygame.init()

screen = pygame.display.set_mode((400, 400))


apples = []
tails = []
players = []

clock = pygame.time.Clock()
playtime = 0
FPS = 60
score = 0


player = Player()
Apple()
game = Game()

while game.running:
	milliseconds = clock.tick(FPS)
	playtime += milliseconds / 1000.0

	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			game.running = False
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				game.running = False
			elif e.key == pygame.K_LEFT:
				player.dy = 0
				player.dx = -player.speed
			elif e.key == pygame.K_RIGHT:
				player.dy = 0
				player.dx = player.speed
			elif e.key == pygame.K_UP:
				player.dx = 0
				player.dy = -player.speed
			elif e.key == pygame.K_DOWN:
				player.dx = 0
				player.dy = player.speed

	for player in players:
		player.move()

	for tail in tails:
		tail.move()

	screen.fill((0, 0, 0))
	for tail in tails:
		pygame.draw.rect(screen, (255,0,0), tail.rect)
	for apple in apples:
		pygame.draw.rect(screen, (0, 0, 255), apple.rect)
	pygame.draw.rect(screen, (255, 255, 0), player.rect)

	pygame.display.set_caption('Snake -- Score: {0:.0f}		Time: {1:.2f}'.format(player.score,playtime))
	pygame.display.flip()

pygame.quit()
print('Final Score: {0:.1f}		Time: {1:.2f}'.format(player.score,playtime))