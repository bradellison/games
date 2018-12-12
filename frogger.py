#! /usr/bin/env python

import os
import random
from random import randint
import pygame


class Player(object):
	def __init__(self,pos):
		self.height = 20
		self.width = 20
		self.score = 0
		self.speed = 30
		self.rect = pygame.Rect(pos[0]+5,pos[1]+5,self.width,self.height)
		self.running = True
		self.lives = 5

	def move(self, dx, dy):
		# Move each axis separately. Note that this checks for collisions both times.
		if dx != 0:
			self.move_single_axis(dx, 0)
		if dy != 0:
			self.move_single_axis(0, dy)

	def move_single_axis(self, dx, dy):		
		# Move the rect
		oldx = self.rect.x
		oldy = self.rect.y

		self.rect.x += dx
		self.rect.y += dy

		# If you collide with a wall, move out based on velocity
		for wall in walls:
			if self.rect.colliderect(wall.rect):
				if dx > 0: # Moving right; Hit the left side of the wall
					self.rect.left = oldx
				if dx < 0: # Moving left; Hit the right side of the wall
					self.rect.left = oldx
				if dy > 0: # Moving down; Hit the top side of the wall
					self.rect.top = oldy
				if dy < 0: # Moving up; Hit the bottom side of the wall
					self.rect.top = oldy

		if self.rect.left > 630 or self.rect.right < 0:
			player.lives -= 1
			player.rect.y = 395
			player.rect.x = 305

		for fly in flies:
			if self.rect.colliderect(fly.rect):
				flies.remove(fly)
				self.rect.y = 395
				self.score += 50

		for water in waters:
			if self.rect.colliderect(water.rect):
				logcollide = 0
				for log in logs:
					if self.rect.colliderect(log.rect):
						logcollide += 1
						self.score += 0.05
				if logcollide == 0:
					player.lives -= 1
					player.rect.y = 395
					player.rect.x = 305			

class Wall(object):
	def __init__(self, pos):
		walls.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 30, 30)

class Ground(object):
	def __init__(self, pos):
		grounds.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 30, 30)


class Water(object):
	def __init__(self, pos):
		waters.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 30, 30)

class Road(object):
	def __init__(self, pos):
		roads.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 30, 30)

class Roadline(object):
	def __init__(self,pos):
		roadlines.append(self)
		self.rect = pygame.Rect(pos[0],pos[1],30,3)

class Car(object):
	def __init__(self,lane):
		cars.append(self)
		carxwidth = 60 + randint(0,2)*30
		caryheight = 20
		self.location = lane
		cary = 215 + 30*self.location
		carx = 200
		self.speed = 4
		if self.location == 1 or self.location == 3 or self.location == 5:
			carx = 0 - carxwidth
			self.direction = 1
		else:
			carx = 630
			self.direction = -1
		self.colour = (randint(150,255),randint(150,255),randint(150,255))
		self.rect = pygame.Rect(carx,cary,carxwidth,caryheight)

	def move(self):
		velocity = self.speed * self.direction
		self.rect.x += velocity
		if self.rect.left > 630:
			cars.remove(self)
		if self.rect.right < 0:
			cars.remove(self)
		if self.rect.colliderect(player):
			player.lives -= 1
			player.rect.y = 395

class Log(object):
	def __init__(self,lane):
		logs.append(self)
		logxwidth = 60 + randint(0,4)*30
		logyheight = 20
		location = lane
		logy = 35 + 30*location
		self.colour = (randint(0,255),0,0)
		self.speed = 2
		if location == 1 or location == 3 or location ==5:
			logx = 0 - logxwidth
			self.direction = 1
		else:
			logx = 630
			self.direction = -1
		self.rect = pygame.Rect(logx,logy,logxwidth,logyheight)

	def move(self):
		velocity = self.speed * self.direction
		self.rect.x += velocity
		if self.rect.left > 630:
			logs.remove(self)
		if self.rect.right < 0:
			logs.remove(self)
		if self.rect.colliderect(player):
			player.rect.x += velocity
			if self.rect.left > 630 or self.rect.right < 0:
				player.lives -= 1
				player.rect.y = 395
				player.rect.x = 305

class Fly(object):
	def __init__(self,pos):
		flies.append(self)
		self.rect = pygame.Rect(pos[0]+12,pos[1]+12,6,6)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

screen = pygame.display.set_mode((630, 420))


walls = []
cars = []
grounds = []
logs = []
waters = []
roads = []
roadlines = []
flies = []


nextcar = [0,0,0,0,0]
nextlog = [0,0,0,0,0]


clock = pygame.time.Clock()
playtime = 0
FPS = 60
score = 0


level = [
"BBBBBBBBBBBBBBBBBBBBBBB",
"BBBBBBBBBBBBBBBBBBBBBBB",
"BBBFBBBFBBBFBBBFBBBFBBB",
"WWWWWWWWWWWWWWWWWWWWWWW",
"WWWWWWWWWWWWWWWWWWWWWWW",
"WWWWWWWWWWWWWWWWWWWWWWW",
"WWWWWWWWWWWWWWWWWWWWWWW",
"WWWWWWWWWWWWWWWWWWWWWWW",
"BGGGGGGGGGGGGGGGGGGGGGB",
"BPPOPPPOPPPOPPPOPPPOPPB",
"BRRLRRRLRRRLRRRLRRRLRRB",
"BRRLRRRLRRRLRRRLRRRLRRB",
"BRRLRRRLRRRLRRRLRRRLRRB",
"BKKJKKKJKKKJKKKJKKKJKKB",
"BGGGGGGGGGGTGGGGGGGGGGB",
"BBBBBBBBBBBBBBBBBBBBBBB",
]

x = y = -30
for row in level:
	for col in row:
		if col == "B":
			Wall((x, y))
		if col == "G":
			Ground((x, y))
		if col == "F":
			Ground((x, y))
			Fly((x, y))
		if col == "W":
			Water((x,y))
		if col == "R":
			Road((x,y))
		if col == "T":
			player = Player((x, y))
			Ground((x, y))
		if col == "P":
			Road((x,y))
			Roadline((x,y))
		if col == "O":
			Road((x,y))
			Roadline((x,y))
			Roadline((x,y+27))
		if col == "L":
			Road((x,y))
			Roadline((x,y+27))
			Roadline((x,y))
		if col == "J":
			Road((x,y))
			Roadline((x,y))
			Roadline((x,y+27))
		if col == "K":
			Road((x,y))
			Roadline((x,y+27))

		x += 30
	y += 30
	x = -30

while player.running:
	milliseconds = clock.tick(FPS)
	playtime += milliseconds / 1000.0

	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			player.running = False
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				player.running = False
			elif e.key == pygame.K_LEFT:
				player.move(-player.speed, 0)
			elif e.key == pygame.K_RIGHT:
				player.move(player.speed, 0)
			elif e.key == pygame.K_UP:
				player.move(0, -player.speed)
			elif e.key == pygame.K_DOWN:
				player.move(0, player.speed)

	for i in range(0,5):
		if nextcar[i] < playtime:
			Car(i+1)
			nextcar[i] += randint(8,15)/10

	for i in range(0,5):
		if nextlog[i] < playtime:
			Log(i+1)
			nextlog[i] += randint(20,40)/10

	for car in cars:
		car.move()

	for log in logs:
		log.move()

	screen.fill((0, 0, 0))
	for wall in walls:
		pygame.draw.rect(screen, (255,0,255), wall.rect)
	for ground in grounds:
		pygame.draw.rect(screen, (0, 255, 0), ground.rect)
	for water in waters:
		pygame.draw.rect(screen, (0,0,255), water.rect)
	for road in roads:
		pygame.draw.rect(screen, (25,25,25), road.rect)
	for roadline in roadlines:
		pygame.draw.rect(screen, (255,255,255), roadline.rect)
	for car in cars:
		pygame.draw.rect(screen, car.colour, car.rect)
	for log in logs:
		pygame.draw.rect(screen, log.colour, log.rect)
	for fly in flies:
		pygame.draw.rect(screen, (0, 0, 0), fly.rect)
	pygame.draw.rect(screen, (255, 120, 150), player.rect)

	pygame.display.set_caption('Frogger -- Score: {0:.0f}		Lives: {1:.2f}		Time: {2:.2f}'.format(player.score,player.lives,playtime))
	pygame.display.flip()

pygame.quit()
print('Final Score: {0:.1f}		Time: {1:.2f}'.format(player.score,playtime))