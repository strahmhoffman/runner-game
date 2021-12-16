import pygame
from sys import exit

WIDTH, HEIGHT = 800, 600

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Runner')
	clock = pygame.time.Clock()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		pygame.display.update()
		clock.tick(60)
