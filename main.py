import pygame
from sys import exit

WIDTH, HEIGHT = 800, 400

if __name__ == '__main__':
	def display_score():
		curr_time = pygame.time.get_ticks() // 100 - start_time
		score_surf = score_font.render(f'Score: {curr_time}', False, (64, 64, 64))
		score_rect = score_surf.get_rect(center=(400, 50))
		screen.blit(score_surf, score_rect)
		return curr_time


	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('space runner')
	clock = pygame.time.Clock()
	score_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
	title_font = pygame.font.Font('assets/font/Pixeltype.ttf', 80)
	game_active = False
	start_time = 0
	round_score = 0

	sky_surf = pygame.image.load('assets/graphics/Sky.png').convert()
	ground_surf = pygame.image.load('assets/graphics/ground.png').convert()

	title_surf = title_font.render('"SPACE RUNNER"', True, (111, 196, 169))
	title_rect = title_surf.get_rect(center=(WIDTH // 2, 65))

	hint_surf = score_font.render('Press Space to run!', True, (111, 196, 169))
	hint_rect = hint_surf.get_rect(center=(WIDTH // 2, HEIGHT - 65))

	# score_surf = score_font.render('My game', False, (64, 64, 64))
	# score_rect = score_surf.get_rect(center=(WIDTH / 2, 50))

	snail_surf = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
	snail_rect = snail_surf.get_rect(bottomright=(WIDTH // 2, 300))

	player_surf = pygame.image.load('assets/graphics/player/player_walk_1.png').convert_alpha()
	player_rect = player_surf.get_rect(midbottom=(80, 300))
	player_gravity = 0

	# Intro screen
	player_stand = pygame.image.load('assets/graphics/player/player_stand.png').convert_alpha()
	player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
	player_stand_rect = player_stand.get_rect(center=(WIDTH // 2, HEIGHT // 2))

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
					start_time = pygame.time.get_ticks() // 100
					snail_rect.left = WIDTH
					player_rect.bottom = 300
					player_gravity = -9

		if game_active:
			screen.blit(sky_surf, (0, 0))
			screen.blit(ground_surf, (0, 300))

			# pygame.draw.rect(screen, '#c0e8ec', score_rect)
			# pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
			# screen.blit(score_surf, score_rect)
			round_score = display_score()

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
				round_score = pygame.time.get_ticks() // 100 - start_time

		else:
			screen.fill((94, 129, 162))

			screen.blit(title_surf, title_rect)

			score_message = score_font.render(f'Your score: {round_score}', True, (111, 196, 169))
			score_message_rect = score_message.get_rect(center=(WIDTH // 2, HEIGHT - 65))

			if round_score:
				screen.blit(score_message, score_message_rect)
			else:
				screen.blit(hint_surf, hint_rect)

			screen.blit(player_stand, player_stand_rect)

		pygame.display.update()

		clock.tick(60)
