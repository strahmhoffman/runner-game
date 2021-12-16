import pygame
from sys import exit

WIDTH, HEIGHT = 800, 400

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Runner')
	clock = pygame.time.Clock()
	test_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)

	sky_surface = pygame.image.load('assets/graphics/Sky.png').convert()
	ground_surface = pygame.image.load('assets/graphics/ground.png').convert()
	text_surface = test_font.render('My game', False, 'Black')

	snail_surface = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
	snail_x_pos = 800

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		screen.blit(sky_surface, (0, 0))
		screen.blit(ground_surface, (0, 300))
		screen.blit(text_surface, (300, 50))

		if snail_x_pos < -100:
			snail_x_pos = 800
		snail_x_pos -= 4
		screen.blit(snail_surface, (snail_x_pos, 250))

		pygame.display.update()

		clock.tick(60)
