import pygame
from sys import exit

WIDTH, HEIGHT = 800, 400

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Runner')
	clock = pygame.time.Clock()
	test_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)

	sky_surf = pygame.image.load('assets/graphics/Sky.png').convert()
	ground_surf = pygame.image.load('assets/graphics/ground.png').convert()
	text_surf = test_font.render('My game', False, 'Black')

	snail_surf = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
	snail_rect = snail_surf.get_rect(bottomright=(800, 300))

	player_surf = pygame.image.load('assets/graphics/player/player_walk_1.png').convert_alpha()
	player_rect = player_surf.get_rect(midbottom=(80, 300))

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		screen.blit(sky_surf, (0, 0))
		screen.blit(ground_surf, (0, 300))
		screen.blit(text_surf, (300, 50))

		if snail_rect.right <= 0:
			snail_rect.left = 800
		snail_rect.x -= 4
		screen.blit(snail_surf, snail_rect)

		screen.blit(player_surf, player_rect)

		pygame.display.update()

		clock.tick(60)
