import pygame
from sys import exit
from random import randint, choice

WIDTH, HEIGHT = 800, 400

if __name__ == '__main__':
	class Player(pygame.sprite.Sprite):
		def __init__(self):
			super().__init__()
			self.frame_walk_1 = pygame.image.load('assets/graphics/player/player_walk_1.png').convert_alpha()
			self.frame_walk_2 = pygame.image.load('assets/graphics/player/player_walk_2.png').convert_alpha()
			self.move_frames = [self.frame_walk_1, self.frame_walk_2]
			self.frame_index = 0
			self.frame_jump = pygame.image.load('assets/graphics/player/jump.png').convert_alpha()

			self.image = self.move_frames[self.frame_index]
			self.rect = self.image.get_rect(midbottom=(80, 300))
			self.gravity = 0

			self.jump_sound = pygame.mixer.Sound('assets/audio/jump.mp3')
			self.jump_sound.set_volume(.2)

		def player_input(self):
			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE] and self.rect.bottom >= 300 and game_active:
				self.gravity = -9
				self.jump_sound.play()

		def apply_gravity(self):
			self.gravity += .3
			self.rect.y += self.gravity
			self.rect.bottom = min(self.rect.bottom, 300)

		def animation_state(self):
			if self.rect.bottom < 300:
				self.image = self.frame_jump
			else:
				self.frame_index += 0.05
				if self.frame_index > len(self.move_frames) - 1:
					self.frame_index = 0
				self.image = self.move_frames[round(self.frame_index)]

		def update(self):
			self.player_input()
			self.apply_gravity()
			self.animation_state()


	class Obstacle(pygame.sprite.Sprite):
		def __init__(self, type: str):
			super().__init__()
			self.type = type
			if type == 'fly':
				self.frame_1 = pygame.image.load('assets/graphics/fly/fly1.png').convert_alpha()
				self.frame_2 = pygame.image.load('assets/graphics/fly/fly2.png').convert_alpha()
				y_pos = 200
			else:
				self.frame_1 = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
				self.frame_2 = pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()
				y_pos = 300

			self.move_frames = [self.frame_1, self.frame_2]
			self.frame_index = 0
			self.image = self.move_frames[self.frame_index]
			self.rect = self.image.get_rect(bottomright=(randint(800, 1100), y_pos))

		def animation_state(self):
			if self.type == 'fly':
				self.frame_index += 0.1
			else:
				self.frame_index += 0.025

			if self.frame_index > len(self.move_frames) - 1:
				self.frame_index = 0

			self.image = self.move_frames[round(self.frame_index)]

		def update(self):
			self.animation_state()
			self.rect.x -= 4
			self.destroy()

		def destroy(self):
			if self.rect.right < 0:
				self.kill()


	def display_score():
		curr_time = pygame.time.get_ticks() // 100 - start_time
		score_surf = score_font.render(f'Score: {curr_time}', False, (64, 64, 64))
		score_rect = score_surf.get_rect(center=(400, 50))
		screen.blit(score_surf, score_rect)
		return curr_time


	def collision_sprite():
		if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
			obstacle_group.empty()
			return False
		return True


	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('space runner')
	clock = pygame.time.Clock()
	score_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
	title_font = pygame.font.Font('assets/font/Pixeltype.ttf', 80)
	game_active = False
	start_time = 0
	round_score = 0
	bg_music = pygame.mixer.Sound('assets/audio/music.wav')
	bg_music.set_volume(.1)

	# Groups
	player = pygame.sprite.GroupSingle()
	player.add(Player())

	obstacle_group = pygame.sprite.Group()

	# Background
	sky_surf = pygame.image.load('assets/graphics/Sky.png').convert()
	ground_surf = pygame.image.load('assets/graphics/ground.png').convert()

	# Intro screen
	title_surf = title_font.render('"SPACE RUNNER"', True, (111, 196, 169))
	title_rect = title_surf.get_rect(center=(WIDTH // 2, 65))

	hint_surf = score_font.render('Press Space to run!', True, (111, 196, 169))
	hint_rect = hint_surf.get_rect(center=(WIDTH // 2, HEIGHT - 65))

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

	bg_music.play(loops=-1)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if not game_active:
				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					game_active = True
					start_time = pygame.time.get_ticks() // 100

			if game_active:
				if event.type == obstacle_timer:
					obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

		if game_active:
			screen.blit(sky_surf, (0, 0))
			screen.blit(ground_surf, (0, 300))

			round_score = display_score()

			player.draw(screen)
			player.update()

			obstacle_group.draw(screen)
			obstacle_group.update()

			game_active = collision_sprite()

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
