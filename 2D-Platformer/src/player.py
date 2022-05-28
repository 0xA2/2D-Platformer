import pygame

from support import importFolder
from time import time

class Player(pygame.sprite.Sprite):
	def __init__(self, pos):

		# Player Setup
		super().__init__()
		self.importCharacterAssets()
		self.frameIndex = 0
		self.animationSpeed = 0.15
		self.image = self.animations['idle'][self.frameIndex]
		self.hitbox = pygame.Surface((72,84))
		self.rect = self.hitbox.get_rect(topleft = pos)

		# Player Movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 7
		self.gravity = 0.8
		self.jumpSpeed = -16
		self.doubleJump = True
		self.jumpCount = 0
		self.attackFlag = False
		self.attackStart = 0
		self.blockFlag = False
		self.cooldown = False
		self.cooldownTimer = 0

		# Player Status
		self.status = 'idle'
		self.facingRight = 	True
		self.onGround = False
		self.onCeiling = False
		self.onLeft = False
		self.onRight = False

	def importCharacterAssets(self):
		characterPath = '../art/player/'
		self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[], 'attack':[], 'block':[], 'dash':[]}
		for animation in self.animations.keys():
			fullPath = characterPath + animation
			self.animations[animation] = importFolder(fullPath)

	def animate(self):
		animation = self.animations[self.status]
		self.frameIndex += self.animationSpeed
		if self.frameIndex >= len(animation):
			self.frameIndex = 0

		image = animation[int(self.frameIndex)]
		if self.facingRight:
			self.image = image
		else:
			flip = pygame.transform.flip(image, True, False)
			self.image = flip

		# Ajust rectangle
		if self.onGround and self.onRight:
			self.rect = self.hitbox.get_rect(bottomright = self.rect.bottomright)
		elif self.onGround and self.onLeft:
			self.rect = self.hitbox.get_rect(bottomleft = self.rect.bottomleft)
		elif self.onGround:
			self.rect = self.hitbox.get_rect(midbottom = self.rect.midbottom)
		elif self.onCeiling and self.onRight:
			self.rect = self.hitbox.get_rect(topright = self.rect.topright)
		elif self.onCeiling and self.onLeft:
			self.rect = self.hitbox.get_rect(topleft = self.rect.topleft)
		elif self.onCeiling:
			self.rect = self.hitbox.get_rect(midtop = self.rect.midtop)

		if self.onGround:
			self.jumpCount = 0

	def getInput(self):
		keys = pygame.key.get_pressed()

		# Attacking
		if keys[pygame.K_u] and self.onGround and not self.status == 'run' and not self.status == 'block' and not self.cooldown:
				self.attackStart = time()
				self.attackFlag = True
				self.cooldownTimer = time()
				self.cooldown = True

		# Blocking
		if keys[pygame.K_i] and self.onGround and not self.status == 'run' and not self.status == 'attack' and not self.cooldown:
			self.blockFlag = True

		# Moving
		if keys[pygame.K_a] and not self.attackFlag and not self.blockFlag:
			self.direction.x = -1
			self.facingRight = False
		elif keys[pygame.K_d] and not self.attackFlag and not self.blockFlag:
			self.direction.x = 1
			self.facingRight = True
		else:
			self.direction.x = 0

		# Jumping
		if keys[pygame.K_SPACE] and self.onGround and not self.attackFlag:
			self.jump()

		# Double jump
		if keys[pygame.K_SPACE] and self.status == 'fall' and self.jumpCount < 1:
			self.jump()
			self.jumpCount += 1

	def getStatus(self):

		# Player is jumping
		if self.direction.y < 0:
			self.status = 'jump'

		# Player is falling
		elif self.direction.y > (self.gravity + 0.1):
			self.status = 'fall'

		else:

			# Player is running
			if self.direction.x != 0:
				self.status = 'run'

			else:
				self.status = 'idle'

		# Player is attacking
		curTime = time()
		if self.attackFlag:
			self.status = 'attack'
			diffAttack = curTime - self.attackStart
			if diffAttack > 0.20:
				self.attackFlag = False


		# Player is blocking
		if self.blockFlag:
			self.status = 'block'
			self.blockFlag = False

		diffCooldown = curTime - self.cooldownTimer
		if diffCooldown > 0.60:
			self.cooldown = False


		#print (self.status)

	def jump(self):
		self.direction.y = self.jumpSpeed

	def applyGravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def update(self):
		self.getInput()
		self.getStatus()
		self.animate()
