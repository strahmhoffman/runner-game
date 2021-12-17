import pygame
from sys import exit

WIDTH, HEIGHT = 800, 400

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Runner')
	clock = pygame.time.Clock()
	test_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
	game_active = True

	sky_surf = pygame.image.load('assets/graphics/Sky.png').convert()
	ground_surf = pygame.image.load('assets/graphics/ground.png').convert()
	score_surf = test_font.render('My game', False, (64, 64, 64))
	score_rect = score_surf.get_rect(center=(WIDTH / 2, 50))

	snail_surf = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
	snail_rect = snail_surf.get_rect(bottomright=(WIDTH, 300))

	player_surf = pygame.image.load('assets/graphics/player/player_walk_1.png').convert_alpha()
	player_rect = player_surf.get_rect(midbottom=(80, 300))
	player_gravity = 0

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if game_active:
				if event.type == pygame.MOUSEBUTTONDOWN and player_rect.collidepoint(event.pos):
					if player_rect.bottom == 300:
						player_gravity = -9

				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					if player_rect.bottom == 300:
						player_gravity = -9
			else:
				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					game_active = True
					snail_rect.left = WIDTH
					player_rect.bottom = 300
					player_gravity = -9

		if game_active:
			screen.blit(sky_surf, (0, 0))
			screen.blit(ground_surf, (0, 300))

			pygame.draw.rect(screen, '#c0e8ec', score_rect)
			pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
			screen.blit(score_surf, score_rect)

			if snail_rect.right <= 0:
				snail_rect.left = 800
			snail_rect.x -= 4
			screen.blit(snail_surf, snail_rect)

			# Player
			player_gravity += .3
			player_rect.y += player_gravity
			player_rect.bottom = min(player_rect.bottom, 300)
			screen.blit(player_surf, player_rect)

			# Collision
			if snail_rect.colliderect(player_rect):
				game_active = False

		else:
			screen.fill('Yellow')

		pygame.display.update()

		clock.tick(60)
