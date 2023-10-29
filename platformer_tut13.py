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
from env.constants import green

# import img
from assets.assets import bg_img
from assets.assets import sun_img
from assets.assets import bg_imgSetting
from assets.assets import play_btn
from assets.assets import exit_btn
from assets.assets import setting_btn
from assets.assets import back_btn
from assets.assets import save_btn
from assets.assets import load_btn
from assets.assets import restart_btn

from assets.assets import blob_group
from assets.assets import lava_group
from assets.assets import exit_group
from assets.assets import platform_group
from assets.assets import coin_group
from assets.assets import coin_fx
# import font
from assets.assets import font
from assets.assets import font_score




from components.Coin import Coin
from components.World import World
from components.Button import Button



pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
#define game variables
clock = pygame.time.Clock()
run = True
game_over = 0
main_menu = True
setting_menu = False
level = 1
max_levels = 7
score = 0

# init screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')


# for editer
margin = 200
dirt_img = pygame.image.load('./resources/img/dirt.png')
grass_img = pygame.image.load('./resources/img/grass.png')
blob_img = pygame.image.load('./resources/img/blob.png')
platform_x_img = pygame.image.load('./resources/img/platform_x.png')
platform_y_img = pygame.image.load('./resources/img/platform_y.png')
lava_img = pygame.image.load('./resources/img/lava.png')
coin_img = pygame.image.load('./resources/img/coin.png')
exit_img2 = pygame.image.load('./resources/img/exit.png')

#create buttons
# for edit
load_button = Button(screen, screen_width - 165, 30, load_btn)
save_button = Button(screen, screen_width - 165, 80, save_btn)
back_button = Button(screen, screen_width - 165, 130, back_btn)
# for game
restart_button = Button(screen, screen_width // 2 - 50, screen_height // 2 + 100, restart_btn)
start_button = Button(screen, screen_width // 2 - 350, screen_height // 2, play_btn)
exit_button = Button(screen, screen_width // 2 + 150, screen_height // 2, exit_btn)
setting_button = Button(screen, screen_width // 2 -100 , screen_height // 2, setting_btn)


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
	if path.exists(f'./env/level{level}_data'):
		pickle_in = open(f'./env/level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(screen, world_data, blob_group, platform_group, lava_group, coin_group, exit_group)
	#create dummy coin for showing the score
	score_coin = Coin(tile_size // 2, tile_size // 2)
	coin_group.add(score_coin)
	return world
def draw_grid():
	for c in range(21):
		#vertical lines
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
		#horizontal lines
		pygame.draw.line(screen, white, (0, c * tile_size ), (screen_width-200, c * tile_size ))


def draw_world():
	for row in range(20):
		for col in range(20):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#dirt blocks
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size , row * tile_size ))
				if world_data[row][col] == 2:
					#grass blocks
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size , row * tile_size ))
				if world_data[row][col] == 3:
					#enemy blocks
					img = pygame.transform.scale(blob_img, (tile_size, int(tile_size * 0.75)))
					screen.blit(img, (col * tile_size , row * tile_size + (tile_size * 0.25) ))
				if world_data[row][col] == 4:
					#horizontally moving platform
					img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size , row * tile_size ))
				if world_data[row][col] == 5:
					#vertically moving platform
					img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size , row * tile_size ))
				if world_data[row][col] == 6:
					#lava
					img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size , row * tile_size + (tile_size // 2) ))
				if world_data[row][col] == 7:
					#coin
					img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4) , row * tile_size + (tile_size // 4) ))
				if world_data[row][col] == 8:
					#exit
					img = pygame.transform.scale(exit_img2, (tile_size, int(tile_size * 1.5)))
					screen.blit(img, (col * tile_size , row * tile_size - (tile_size // 2) ))


#load in level data and create world
if path.exists(f'./env/level{level}_data'):
	pickle_in = open(f'./env/level{level}_data', 'rb')
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
			img_right = pygame.image.load(f'./resources/img/guy{num}.png')
			img_right = pygame.transform.scale(img_right, (32, 68))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('./resources/img/ghost.png')
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

while run:
	clock.tick(fps) 
	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (100, 100))

	if main_menu == True:
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
		if setting_button.draw():
			setting_menu = True
			main_menu = False
			tile_size = 30
	elif setting_menu == True:
		#draw background
		screen.fill(green)
		screen.blit(bg_imgSetting, (0,0))
		screen.blit(sun_img, (tile_size * 2 + 100, tile_size * 2+ 50))

		#load and save level
		if save_button.draw():
			#save level data
			pickle_out = open(f'./env/level{level}_data', 'wb')
			pickle.dump(world_data, pickle_out)
			pickle_out.close()
			print('Save data here')
			world = World(screen, world_data, blob_group, platform_group, lava_group, coin_group, exit_group)
			player = Player(screen, 100, screen_height - 130)
		if load_button.draw():
			#load in level data
			if path.exists(f'./env/level{level}_data'):
				pickle_in = open(f'./env/level{level}_data', 'rb')
				world_data = pickle.load(pickle_in)
		if back_button.draw():
			setting_menu = False
			main_menu = True


		#show the grid and draw the level tiles
		draw_grid()
		draw_world()


		#text showing current level
		draw_text(f'Level: {level}', pygame.font.SysFont('Futura', 32), white, 100, screen_height - 140)
		draw_text('Press UP or DOWN to change level', pygame.font.SysFont('Futura', 32), white, 100, screen_height - 110)

		#event handler
		for event in pygame.event.get():
			#quit game
			if event.type == pygame.QUIT:
				run = False
			#mouseclicks to change tiles
			if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
				clicked = True
				pos = pygame.mouse.get_pos()
				x = pos[0] // tile_size
				y = pos[1] // tile_size
				#check that the coordinates are within the tile area
				if x < 20 and y < 20:
					#update tile value
					if pygame.mouse.get_pressed()[0] == 1:
						world_data[y][x] += 1
						if world_data[y][x] > 8:
							world_data[y][x] = 0
					elif pygame.mouse.get_pressed()[2] == 1:
						world_data[y][x] -= 1
						if world_data[y][x] < 0:
							world_data[y][x] = 8
			if event.type == pygame.MOUSEBUTTONUP:
				clicked = False
			#up and down key presses to change level number
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					level += 1
				elif event.key == pygame.K_DOWN and level > 1:
					level -= 1

		#update game display window
		pygame.display.update()


		# end
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
			draw_text('X ' + str(score), font_score, white, tile_size , 5)
		
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
