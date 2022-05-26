import pygame

from os import walk

def importFolder(path):

	surfaceList = []

	for _,_,imgFiles in walk(path):
		for image in imgFiles:
			fullPath = path + '/' + image
			imageSurface = pygame.image.load(fullPath).convert_alpha()
			surfaceList.append(imageSurface)

	return surfaceList
