#! /usr/bin/env python

import os
import random
from random import randint
import pygame


# Class for the orange dude
class Player(object):	
	def __init__(self):
		self.size = 24
		self.rect = pygame.Rect(240, 384, self.size, self.size)
		self.score = 0
		self.speed = 2
		self.powerup = False
		self.powerupend = 0

	def move(self, dx, dy):		
		# Move each axis separately. Note that this checks for collisions both times.
		if dx != 0:
			self.move_single_axis(dx, 0)
		if dy != 0:
			self.move_single_axis(0, dy)
	
	def move_single_axis(self, dx, dy):		
		# Move the rect
		self.rect.x += dx
		self.rect.y += dy

		# If you collide with a wall, move out based on velocity
		for wall in walls:
			if self.rect.colliderect(wall.rect):
				if dx > 0: # Moving right; Hit the left side of the wall
					self.rect.right = wall.rect.left
				if dx < 0: # Moving left; Hit the right side of the wall
					self.rect.left = wall.rect.right
				if dy > 0: # Moving down; Hit the top side of the wall
					self.rect.bottom = wall.rect.top
				if dy < 0: # Moving up; Hit the bottom side of the wall
					self.rect.top = wall.rect.bottom

		for coin in coins:
			 if self.rect.colliderect(coin.rect):
			 	coins.remove(coin)
			 	self.score += 5

		for powerup in powerups:
			 if self.rect.colliderect(powerup.rect):
			 	powerups.remove(powerup)
			 	self.score += 15
			 	self.powerup = True
			 	self.powerupend = playtime + 5
			 	self.speed = 3

	def get_powerup_end(self, powerupend, playtime):
		if powerupend > playtime:
			self.speed = 4
			self.size = 12
		else:
			self.speed = 2
			self.powerup = False


class Turn(object):
	def __init__(self, pos):
		turningPoints.append(self)
		self.rect=pygame.Rect(pos[0],pos[1],23,23)

class Ghost(object):
	def __init__(self, pos, colour):
		ghosts.append(self)
		self.originalsize = 24
		self.size = self.originalsize
		self.rect = pygame.Rect(pos[0],pos[1],self.size,self.size)
		self.originalcolour = colour
		self.colour = colour
		self.direction = 1
		self.hit = False

	def move(self,direction):
		if direction == 0:
			dxdy = (0,0)
		elif direction == 1:
			dxdy = (0,-2)
		elif direction == 2:
			dxdy = (2,0)
		elif direction == 3:
			dxdy = (0,2)
		elif direction == 4:
			dxdy = (-2,0)
		dx = dxdy[0]
		dy = dxdy[1]
		if dx != 0:
			self.move_single_axis(dx, 0)
		if dy != 0:
			self.move_single_axis(0, dy)

	def move_single_axis(self, dx, dy):		
		# Move the rect
		self.rect.x += dx
		self.rect.y += dy

		# If you collide with a wall, move out based on velocity
		for wall in walls:
			if self.rect.colliderect(wall.rect):
				if dx > 0: # Moving right; Hit the left side of the wall
					self.rect.right = wall.rect.left
				if dx < 0: # Moving left; Hit the right side of the wall
					self.rect.left = wall.rect.right
				if dy > 0: # Moving down; Hit the top side of the wall
					self.rect.bottom = wall.rect.top
				if dy < 0: # Moving up; Hit the bottom side of the wall
					self.rect.top = wall.rect.bottom

		for point in turningPoints:
			if self.rect.contains(point.rect):
				self.direction = randint(1,4)

		if self.rect.colliderect(player.rect):
			if player.powerup == False:
				print('Game over!')
				game.running = False
			if player.powerup == True:
				if self.hit == False:
					player.score += 50
				self.hit = True

		if player.powerup == True:
			if self.hit == True:
				self.colour = (240,240,240)
			else:
				self.colour = (randint(0,255),randint(0,255),randint(0,255))
		else:
			self.colour = self.originalcolour
			self.hit = False


# Nice class to hold a wall rect
class Wall(object):
	def __init__(self, pos):
		walls.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 24, 24)

class Coin(object):
	def __init__(self,pos):
		coins.append(self)
		self.rect = pygame.Rect(pos[0]+7, pos[1]+7, 10, 10)

class Powerup(object):
	def __init__(self,pos):
		powerups.append(self)
		self.rect = pygame.Rect(pos[0]+5, pos[1]+5, 15, 15)

class Game(object):
	def __init__(self):
		self.running = True


# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()


# Set up the display


clock = pygame.time.Clock()
walls = [] # List to hold the walls
coins = []
ghosts = []
powerups = []
turningPoints = []
player = Player() # Create the player
game = Game()
FPS = 60
playtime = 0

ghost1colour = (255,0,0)
ghost2colour = (255,0,255)
ghost3colour = (0,255,255)
ghost4colour = (0,0,255) 

screen = pygame.display.set_mode((504, 552))

# Holds the level layout in a list of strings.
level = [
"BBBBBBBBBBBBBBBBBBBBB",
"BWWWWWWWWWWWWWWWWWWWB",
"BWTCCTCCCTWTCCCTCCTWB",
"BWUWWCWWWCWCWWWCWWUWB",
"BWTCCTCTCTCTCTCTCCTWB",
"BWCWWCWCWWWWWCWCWWCWB",
"BWTCCTWTCTWTCTWTCCTWB",
"BWWWWCWWWCWCWWWCWWWWB",
"BBBBWCWTCTTTCTWTWBBBB",
"WWWWWCWCWW1WWCWCWWWWW",
"CCCCCTCTW234WTCTCCCCC",
"WWWWWCWCWWWWWCWCWWWWW",
"BBBBWCWTCCCCCTWCWBBBB",
"BWWWWCWCWWWWWCWCWWWWB",
"BWTCCTCTCTWTCTCTCCTWB",
"BWCWWCWWWCWCWWWCWWCWB",
"BWTTWTCTCTBTCTCTWTTWB",
"BWWCWCWCWWWWWCWCWCWWB",
"BWPTCTWTCTWTCTWTCTPWB",
"BWCWWWWWWCWCWWWWWWCWB",
"BWTCCCCCCTCTCCCCCCTWB",
"BWWWWWWWWWWWWWWWWWWWB",
"BBBBBBBBBBBBBBBBBBBBB",
]



# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
	for col in row:
		if col == "W":
			Wall((x, y))
		if col == "C":
			Coin((x, y))
		if col == "T":
			Coin((x, y))
			Turn((x, y))
		if col == "1":
			ghost1 = Ghost((x,y),ghost1colour)
			Turn((x, y))
		if col == "2":
			ghost2 = Ghost((x,y),ghost2colour)
			Turn((x, y))
		if col == "3":
			ghost3 = Ghost((x,y),ghost3colour)
			Turn((x, y))
		if col == "4":
			ghost4 = Ghost((x,y),ghost4colour)
			Turn((x, y))
		if col == "P":
			Turn((x, y))
			Powerup((x, y))
		if col == "U":
			Powerup((x, y))
		x += 24
	y += 24
	x = 0




while game.running:
	
	milliseconds = clock.tick(FPS)
	playtime += milliseconds / 1000.0
	
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			game.running = False
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			game.running = False
	
	player.get_powerup_end(player.powerupend, playtime)

	# Move the player if an arrow key is pressed
	key = pygame.key.get_pressed()
	if key[pygame.K_LEFT]:
		player.move(-player.speed, 0)
	if key[pygame.K_RIGHT]:
		player.move(player.speed, 0)
	if key[pygame.K_UP]:
		player.move(0, -player.speed)
	if key[pygame.K_DOWN]:
		player.move(0, player.speed)

	#SCREEN WRAP
	if player.rect.right < 0:
		player.rect.left = 504
	if player.rect.left > 504:
		player.rect.right = 0

	for ghost in ghosts:
		if ghost.rect.right < 0:
			ghost.rect.left = 504
		if ghost.rect.left > 504:
			ghost.rect.right = 0

	if coins == []:
		game.running = False
		print('You won!')

	for ghost in ghosts:
		ghost.move(ghost.direction)


	# Draw the scene
	screen.fill((0, 0, 0))
	for wall in walls:
		pygame.draw.rect(screen, (255, 255, 255), wall.rect)
#	for point in turningPoints:
#		pygame.draw.rect(screen, (50,50,50), point.rect)
	for coin in coins:
		pygame.draw.rect(screen, (255, 255, 0), coin.rect)
	pygame.draw.rect(screen, (255, 200, 0), player.rect)
	if player.rect.right<0:
		player.rect.left = 504


	for ghost in ghosts:
		pygame.draw.rect(screen, ghost.colour, ghost.rect)
	for powerup in powerups:
		pygame.draw.rect(screen, (255, 0, 150), powerup.rect)


	pygame.display.set_caption('PacMan -- Score: {0:.0f}		Time: {1:.2f}'.format(player.score,playtime))
	pygame.display.flip()

pygame.quit()
print('Final Score: {0:.1f}		Time: {1:.2f}'.format(player.score,playtime))