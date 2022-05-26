import pygame
import sys

from level import Level
from settings import *
from tiles import Tile


def main():

	# Setup

	pygame.init()
	screen = pygame.display.set_mode((screenWidth, screenHeight))
	clock = pygame.time.Clock()
	level = Level(map, screen)

	# Game loop

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		screen.fill('grey')
		level.run()

		pygame.display.update()
		clock.tick(60)

if __name__ == "__main__":
	main()


