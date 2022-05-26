import pygame

from player import Player
from settings import tileSize, screenWidth, screenHeight
from tiles import Tile

class Level:
	def __init__(self, levelData, surface):

		# Level Setup
		self.displaySurface = surface
		self.setupLevel(levelData)
		self.shiftx = 0
		self.shifty = 0
		self.curX = 0

	def setupLevel(self, layout):

		# Sprite Groups
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()

		for r in range(0, len(layout)):
			row = layout[r]
			for c in range(0,len(row)):

				x = c*tileSize
				y = r*tileSize

				# Place tiles
				if layout[r][c] == 'X':
					tile = Tile((x,y), tileSize, 'white')
					self.tiles.add(tile)

				if layout[r][c] == 'I':
					tile = Tile((x,y), tileSize, 'gray')
					self.tiles.add(tile)

				# Place player
				if layout[r][c] == 'P':
					playerSprite = Player((x,y))
					self.player.add(playerSprite)

	def scrollx(self):
		player = self.player.sprite
		playerx = player.rect.centerx
		directionx = player.direction.x

		if playerx < (screenWidth*(1/4)) and directionx < 0:
			self.shiftx = 5
			player.speed = 0
		elif playerx > (screenWidth*(3/4)) and directionx > 0:
			self.shiftx = -5
			player.speed = 0
		else:
			self.shiftx = 0
			player.speed = 5


	def horizontalCollision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.onLeft = True
					self.curX = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.onRight = True
					self.curX = player.rect.right
		if player.onLeft and (player.rect.left < self.curX or player.direction.x >= 0):
			player.onLeft = False
		if player.onRight and (player.rect.right > self.curX or player.direction.x <= 0):
			player.onRight = False

	def verticalCollision(self):
		player = self.player.sprite
		player.applyGravity()

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > player.gravity:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.onGround = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					self.curX = player.rect.left
					player.onCeiling = True

		if player.onGround and player.direction.y < 0 or player.direction.y > player.gravity:
			player.onGround = False
		if player.onCeiling and player.direction.y > 0:
			player.onCeiling = False


	def run(self):

		# Level Tiles
		self.tiles.update(self.shiftx, self.shifty)
		self.tiles.draw(self.displaySurface)
		#self.scrollx()

		# Player Sprite
		self.player.update()
		self.verticalCollision()
		self.horizontalCollision()
		self.player.draw(self.displaySurface)
