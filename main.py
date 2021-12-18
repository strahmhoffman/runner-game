import pygame
from sys import exit
from random import randint

WIDTH, HEIGHT = 800, 400

if __name__ == '__main__':
	def display_score():
		curr_time = pygame.time.get_ticks() // 100 - start_time
		score_surf = score_font.render(f'Score: {curr_time}', False, (64, 64, 64))
		score_rect = score_surf.get_rect(center=(400, 50))
		screen.blit(score_surf, score_rect)
		return curr_time


	def obstacle_movement(obstacle_list):
		if obstacle_list:
			for obstacle_rect in obstacle_list:
				obstacle_rect.x -= 4

				screen.blit(snail_surf if obstacle_rect.bottom == 300 else fly_surf, obstacle_rect)

			obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

			return obstacle_list
		return []


	def collisions(player, obstacles):
		if obstacles:
			for obstacle_rect in obstacles:
				if player.colliderect(obstacle_rect):
					return False
		return True


	def player_animation():
		global player_surf, player_index

		if player_rect.bottom < 300:
			player_surf = player_jump
		else:
			player_surf = player_frames[player_frame_index]


	# play walking animation if player is on floor
	# play the jump surface when player is not on floor

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

	# Obstacles
	snail_frame_1 = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
	snail_frame_2 = pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()
	snail_frames = [snail_frame_1, snail_frame_2]
	snail_surf = snail_frame_1
	fly_frame_1 = pygame.image.load('assets/graphics/fly/fly1.png').convert_alpha()
	fly_frame_2 = pygame.image.load('assets/graphics/fly/fly2.png').convert_alpha()
	fly_frames = [fly_frame_1, fly_frame_2]
	fly_surf = fly_frame_1
	snail_frame_index = fly_frame_index = 0

	obstacle_rect_list = []

	player_walk_1 = pygame.image.load('assets/graphics/player/player_walk_1.png').convert_alpha()
	player_walk_2 = pygame.image.load('assets/graphics/player/player_walk_2.png').convert_alpha()
	player_frames = [player_walk_1, player_walk_2]
	player_frame_index = 0
	player_jump = pygame.image.load('assets/graphics/player/jump.png').convert_alpha()

	player_surf = player_walk_1
	player_rect = player_surf.get_rect(midbottom=(80, 300))
	player_gravity = 0

	# Intro screen
	player_stand = pygame.image.load('assets/graphics/player/player_stand.png').convert_alpha()
	player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
	player_stand_rect = player_stand.get_rect(center=(WIDTH // 2, HEIGHT // 2))

	# Timer
	obstacle_timer = pygame.USEREVENT + 1
	pygame.time.set_timer(obstacle_timer, 1500)

	player_animation_timer = pygame.USEREVENT + 2
	pygame.time.set_timer(player_animation_timer, 200)

	snail_animation_timer = pygame.USEREVENT + 3
	pygame.time.set_timer(snail_animation_timer, 500)

	fly_animation_timer = pygame.USEREVENT + 4
	pygame.time.set_timer(fly_animation_timer, 200)

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
					obstacle_rect_list.clear()
					start_time = pygame.time.get_ticks() // 100
					player_rect.bottom = 300
					player_gravity = 0

			if game_active:
				if event.type == obstacle_timer:
					if randint(0, 1):
						obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
					else:
						obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 200)))

				if event.type == player_animation_timer:
					if player_frame_index:
						player_frame_index = 0
					else:
						player_frame_index = 1

				if event.type == snail_animation_timer:
					if snail_frame_index:
						snail_frame_index = 0
					else:
						snail_frame_index = 1
					snail_surf = snail_frames[snail_frame_index]

				if event.type == fly_animation_timer:
					if fly_frame_index:
						fly_frame_index = 0
					else:
						fly_frame_index = 1
					fly_surf = fly_frames[fly_frame_index]

		if game_active:
			screen.blit(sky_surf, (0, 0))
			screen.blit(ground_surf, (0, 300))

			round_score = display_score()

			# Player
			player_gravity += .3
			player_rect.y += player_gravity
			player_rect.bottom = min(player_rect.bottom, 300)
			player_animation()
			screen.blit(player_surf, player_rect)

			# Obstacle movement
			obstacle_rect_list = obstacle_movement(obstacle_rect_list)

			# Collision
			game_active = collisions(player_rect, obstacle_rect_list)

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
