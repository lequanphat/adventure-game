import pygame
from pygame.locals import *
from os import path
import pickle
from pygame import mixer
from assets.assets import game_over_fx
from assets.assets import jump_fx
# from env
from env.constants import tile_size
from env.constants import screen_width
from env.constants import screen_height
from env.constants import fps
from env.constants import white
from env.constants import blue

# import img
from assets.assets import bg_img
from assets.assets import sun_img

from assets.assets import blob_group
from assets.assets import lava_group
from assets.assets import exit_group
from assets.assets import platform_group
from assets.assets import coin_group
from assets.assets import coin_fx
# import font
from assets.assets import font
from assets.assets import font_score
from assets.assets import restart_img
from assets.assets import start_img
from assets.assets import exit_img



from components.Coin import Coin
from components.World import World
from components.Button import Button

#define game variables
game_over = 0
main_menu = True
level = 1
max_levels = 7
score = 0

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
clock = pygame.time.Clock()


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
#create buttons
restart_button = Button(screen, screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen, screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen, screen_width // 2 + 150, screen_height // 2, exit_img)
#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#function to reset level
def reset_level(player,  level):
	blob_group.empty()
	platform_group.empty()
	coin_group.empty()
	lava_group.empty()
	exit_group.empty()
	player.reset(100, screen_height - 130)
	#load in level data and create world
	if path.exists(f'./src/env/level{level}_data'):
		pickle_in = open(f'./src/env/level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(screen, world_data, blob_group, platform_group, lava_group, coin_group, exit_group)
	#create dummy coin for showing the score
	score_coin = Coin(tile_size // 2, tile_size // 2)
	coin_group.add(score_coin)
	return world

#load in level data and create world
if path.exists(f'./src/env/level{level}_data'):
	pickle_in = open(f'./src/env/level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)

class Player():
	def __init__(self, screen,  x, y):
		self.reset(x, y)
		self.screen = screen
		self.world = world
		self.blob_group = blob_group
		self.platform_group = platform_group
		self.lava_group = lava_group
		self.exit_group = exit_group

	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 5
		col_thresh = 20

		if game_over == 0:
			#get keypresses
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				jump_fx.play()
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#handle animation
			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#check for collision
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#check for collision with enemies
			if pygame.sprite.spritecollide(self, self.blob_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with lava
			if pygame.sprite.spritecollide(self, self.lava_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with exit
			if pygame.sprite.spritecollide(self, self.exit_group, False):
				game_over = 1


			#check for collision with platforms
			for platform in self.platform_group:
				#collision in the x direction
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#collision in the y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
						self.vel_y = 0
						dy = platform.rect.bottom - self.rect.top
					#check if above platform
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						dy = 0
					#move sideways with the platform
					if platform.move_x != 0:
						self.rect.x += platform.move_direction


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy


		elif game_over == -1:
			self.image = self.dead_image
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
			if self.rect.y > 200:
				self.rect.y -= 5

		#draw player onto screen
		self.screen.blit(self.image, self.rect)

		return game_over


	def reset(self,  x, y):
		
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 5):
			img_right = pygame.image.load(f'./src/resources/img/guy{num}.png')
			img_right = pygame.transform.scale(img_right, (40, 80))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('./src/resources/img/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True


world = World(screen, world_data, blob_group, platform_group, lava_group, coin_group, exit_group)
player = Player(screen, 100, screen_height - 130)
run = True
while run:

	clock.tick(fps) 
        
	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (100, 100))

	if main_menu == True:
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
	else:
		world.draw()

		if game_over == 0:
			blob_group.update()
			platform_group.update()
			#update score
			#check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
				coin_fx.play()
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
		
		blob_group.draw(screen)
		platform_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)
		game_over = player.update(game_over)
		#if player has died
		if game_over == -1:
			if restart_button.draw():
				world_data = []
				world = reset_level(player,  level)
				game_over = 0
				score = 0

		#if player has completed the level
		if game_over == 1:
			#reset game and go to next level
			level += 1
			if level <= max_levels:
				#reset level
				world_data = []
				world = reset_level(player, level)
				game_over = 0
			else:
				draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2)
				if restart_button.draw():
					level = 1
					#reset level
					world_data = []
					
					world = reset_level(player, level)
					game_over = 0
					score = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
