#! /usr/bin/env python

import os
import random
from random import randint
import pygame

#Class for our ship

class Player(object):
	def __init__(self,pos):
		self.height = 10
		self.width = 24
		self.score = 0
		self.speed = 2
		self.rect = pygame.Rect(pos[0],pos[1]+14,self.width,self.height)
		self.gunrect = pygame.Rect(pos[0]+8,pos[1]+10,8,4)
		self.lastshot = -1
		self.running = True

	def move(self, dx):
		self.rect.x += dx
		self.gunrect.x += dx

		if self.rect.right > 600:
			self.rect.right = 600
			self.gunrect.right = 592
		if self.rect.left < 0:
			self.rect.left = 0
			self.gunrect.left = 8

class PlayerBullet(object):
	def __init__(self,pos):
		self.height = 10
		self.width = 4
		self.speed = 3
		self.rect = pygame.Rect(pos[0],pos[1],self.width,self.height)
		player.lastshot = playtime
		playerbullets.append(self)

	def move(self,dy):
		self.rect.y -= 10

		for wall in walls:
			if self.rect.colliderect(wall):
				wall.rect.y -= 0.5
				wall.green -= 52
				wall.blue -= 51
				if wall.green < 0:
					walls.remove(wall)
				if bullet in playerbullets:
					playerbullets.remove(bullet)

		for alien in aliens:
			if self.rect.colliderect(alien):
				alien.health -= 1
				alien.colour = (255,0,60)
				if alien.health <= 0:
					aliens.remove(alien)
				if bullet in playerbullets:
					playerbullets.remove(bullet)
				player.score += 10

		for saucer in saucers:
			if self.rect.colliderect(saucer):
				saucers.remove(saucer)
				if bullet in playerbullets:
					playerbullets.remove(bullet)
				player.score += 50			

class EnemyBullet(object):
	def __init__(self,pos):
		self.height = 10
		self.width = 4
		self.speed = 3
		self.rect = pygame.Rect(pos[0],pos[1],self.width,self.height)
		enemybullets.append(self)

	def move(self,dy):
		self.rect.y += 10
		for wall in walls:
			if self.rect.colliderect(wall):
				wall.green -= 60
				wall.blue -= 60
				if wall.green < 0:
					walls.remove(wall)
				if bullet in enemybullets:
					enemybullets.remove(bullet)

		for ground in grounds:
			if self.rect.colliderect(ground):
				if bullet in enemybullets:
					enemybullets.remove(bullet)

		if self.rect.colliderect(player):
			print('Game over!')
			player.running = False

class Alien(object):
	def __init__(self, pos, health):
		aliens.append(self)
		self.health = health
		self.rect = pygame.Rect(pos[0]+4, pos[1]+4, 16, 16)
		self.direction = 1
		self.speed = 0.5
		self.colour = (200,200,60)

	def move(self):
		self.rect.x += self.direction * self.speed
		if self.rect.right >= 600 or self.rect.left <= 0:
			for alien in aliens:
				alien.rect.y += 24
				alien.direction *= -1
#			self.rect.y += 24
#			self.direction *= -1

		for wall in walls:
			if self.rect.colliderect(wall):
				walls.remove(wall)

		if self.rect.colliderect(player):
			print('Game over!')
			player.running = False

class Saucer(object):
	def __init__(self):
		saucers.append(self)
		self.direction = 1
		self.speed = 2
		self.posx = -32
		if randint(0,1) == 1:
			self.direction *= -1
			self.posx = 600
		self.rect = pygame.Rect(self.posx, 12, 32, 16)

	def move(self):
		saucer.rect.x += self.direction * self.speed
		if saucer.rect.left > 600:
			saucers.remove(saucer)
		if saucer.rect.right < 0:
			saucers.remove(saucer)

class Wall(object):
	def __init__(self, pos):
		walls.append(self)
		self.red = 255
		self.green = 255
		self.blue = 255
		self.colour = (255,255,255)
		self.rect = pygame.Rect(pos[0], pos[1], 24, 24)

class Ground(object):
	def __init__(self, pos):
		grounds.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 24, 24)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

screen = pygame.display.set_mode((600, 384))


walls = []
aliens = []
grounds = []
playerbullets = []
enemybullets = []
saucers = []

clock = pygame.time.Clock()
playtime = 0
FPS = 60
score = 0
loopcount = 0
framenumber = 5

level = [
"AAAAAAAAAAAAAAAAAAAAAAAAA",
"AAAAEAEAEAEAEAEAEAEAEAAAA",
"AAAEAEAEAEAEAEAEAEAEAEAAA",
"AAAASASASASASASASASASAAAA",
"AAASASASASASASASASASASAAA",
"AAAASASASASASASASASASAAAA",
"AAAAAAAAAAAAAAAAAAAAAAAAA",
"AAAAAAAAAAAAAAAAAAAAAAAAA",
"AAAAAAAAAAAAAAAAAAAAAAAAA",
"AAAAAAAAAAAAAAAAAAAAAAAAA",
"AAAAAAAAAAAAAAAAAAAAAAAAA",
"AAAAAAAAAAAAAAAAAAAAAAAAA",
"AAAAAAAAAAAAAAAAAAAAAAAAA",
"AWWWWAAAAAAWWWAAAAAAWWWWA",
"AAAAAAAAAAAAPAAAAAAAAAAAA",
"GGGGGGGGGGGGGGGGGGGGGGGGG",
]

x = y = 0
for row in level:
	for col in row:
		if col == "W":
			Wall((x, y))
#		if col == "A":
		if col == "G":
			Ground((x, y))
		if col == "E":
			Alien((x,y),2)
		if col == "S":
			Alien((x,y),1)
		if col == "P":
			player = Player((x, y))
		x += 24
	y += 24
	x = 0

while player.running:
	milliseconds = clock.tick(FPS)
	playtime += milliseconds / 1000.0

	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			player.running = False
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			player.running = False

	# Move the player if an arrow key is pressed
	key = pygame.key.get_pressed()
	if key[pygame.K_LEFT]:
		player.move(-player.speed)
	if key[pygame.K_RIGHT]:
		player.move(player.speed)
	if key[pygame.K_UP]:
		if player.lastshot < playtime-1:
			PlayerBullet((player.rect.x+10,player.rect.y-5))

	for bullet in playerbullets:
		bullet.move(10)

	for alien in aliens:

		alien.move()
		if randint(1,10000) > 9990:
			EnemyBullet((alien.rect.x+8,alien.rect.y+16))

	if randint(1,1000) > 997:
		Saucer()

	for saucer in saucers:
		saucer.move()

	for bullet in enemybullets:
		bullet.move(6)

	screen.fill((0, 0, 0))
	for wall in walls:
		wall.colour = (wall.red, wall.green, wall.blue)
		pygame.draw.rect(screen, wall.colour, wall.rect)
	for ground in grounds:
		pygame.draw.rect(screen, (255, 255, 0), ground.rect)
	pygame.draw.rect(screen, (255, 200, 0), player.rect)
	pygame.draw.rect(screen, (255, 200, 0), player.gunrect)
	for saucer in saucers:
		pygame.draw.rect(screen, (255,255,255), saucer.rect)
	for alien in aliens:
		pygame.draw.rect(screen, alien.colour, alien.rect)
	for bullet in playerbullets:
		pygame.draw.rect(screen, (0,0,255), bullet.rect)
	for bullet in enemybullets:
		pygame.draw.rect(screen, (255,0,0), bullet.rect)

	pygame.display.set_caption('Space Invaders -- Score: {0:.0f}		Time: {1:.2f}'.format(player.score,playtime))
	pygame.display.flip()

pygame.quit()
print('Final Score: {0:.1f}		Time: {1:.2f}'.format(player.score,playtime))