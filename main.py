import pygame
from pygame.locals import *
from os import path
import pickle
import random
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
from env.constants import yellow
from env.constants import green

# import img
from assets.assets import background
from assets.assets import setting_background
from assets.assets import menu_background
from assets.assets import play_btn
from assets.assets import exit_btn
from assets.assets import setting_btn
from assets.assets import back_btn
from assets.assets import save_btn
from assets.assets import load_btn
from assets.assets import restart_btn
from assets.assets import menu_btn
from assets.assets import logo

from assets.assets import blob_group
from assets.assets import lava_group
from assets.assets import exit_group
from assets.assets import platform_group
from assets.assets import coin_group
from assets.assets import coin_fx
# import font
from assets.assets import font
from assets.assets import font_main
from assets.assets import font_score




from components.Coin import Coin
from components.World import World
from components.Button import Button

# for editor
# for editer
from assets.assets import margin
from assets.assets import dirt_img 
from assets.assets import grass_img 
from assets.assets import blob_img 
from assets.assets import platform_x_img 
from assets.assets import platform_y_img 
from assets.assets import lava_img 
from assets.assets import coin_img 
from assets.assets import exit_img2 


import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


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
score = 0
pedding=False
up_action = False
left_action = False
right_action = False
reset_up_action = False
mode="EASY"

my_background = background[0]
# init screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')




#create buttons
# for edit
load_button = Button(screen, screen_width - 165, 30, load_btn)
save_button = Button(screen, screen_width - 165, 80, save_btn)
back_button = Button(screen, screen_width - 165, 130, back_btn)
# for game
restart_button = Button(screen, screen_width // 2 - 50, screen_height // 2 - 100, restart_btn)
menu_button = Button(screen, screen_width // 2 - 50, screen_height // 2 - 20, menu_btn)


start_button = Button(screen, 180, 400, play_btn)
start_with_hand_button = Button(screen, screen_width - 360, 400, play_btn)

setting_button = Button(screen, 180 , 550, setting_btn)
register_button = Button(screen, screen_width -360 , 550, setting_btn)

rank_button = Button(screen, 180, 700 , exit_btn)
exit_button = Button(screen, screen_width - 360, 700 , exit_btn)


#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#function to reset level
def reset_level(player,  level):
	print('level: '+str(level))
	blob_group.empty()
	platform_group.empty()
	coin_group.empty()
	lava_group.empty()
	exit_group.empty()
	player.reset(100, screen_height - 130)
	#load in level data and create world
	world_data = load_world_data()
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
		pygame.draw.line(screen, white, (0, c * tile_size ), (screen_width-margin, c * tile_size ))


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
def generate_new_world():
	new_world = []
	for i in range(0,20):
		list = []
		for j in range(0, 20):
			list.append(0)
		new_world.append(list)
	for i in range(0,20):
		new_world[0][i] = 1
		new_world[19][i] = 1
		new_world[i][0] = 1
		new_world[i][19] = 1
	return new_world

def load_world_data():
	if path.exists(f'./env/level{level}_data'):
		pickle_in = open(f'./env/level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
		return world_data
	

def load_background():
	my_background = background[random.randint(0,1)]
	return my_background

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
			if pedding == False:
				# key event
				if key[pygame.K_SPACE] and self.jumped == False  and self.in_air == False:
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
				# hand event
				if mode == "HARD":
					if up_action == True and self.jumped == False  and self.in_air == False:
						jump_fx.play()
						self.vel_y = -15
						self.jumped = True
					if up_action == False:
						self.jumped = False

					if left_action == True:
						dx -= 5
						self.counter += 1
						self.direction = -1

					if right_action == True:
						dx += 5
						self.counter += 1
						self.direction = 1

					if left_action == False and right_action == False:
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


				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0

				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			if pygame.sprite.spritecollide(self, self.blob_group, False):
				game_over = -1
				game_over_fx.play()

			if pygame.sprite.spritecollide(self, self.lava_group, False):
				game_over = -1
				game_over_fx.play()

			if pygame.sprite.spritecollide(self, self.exit_group, False):
				game_over = 1


			
			for platform in self.platform_group:
				
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				
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
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 180, screen_height // 2 - 215 )
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

world_data = load_world_data()
world = World(screen, world_data, blob_group, platform_group, lava_group, coin_group, exit_group)
player = Player(screen, 100, screen_height - 130)
# capture
cap = cv2.VideoCapture(0)

# run 
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
	
	while run:

		if mode == "HARD":
			success, image = cap.read()
			if not success:
				print("Ignoring empty camera frame.")
				continue
				
			image.flags.writeable = False
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			results = hands.process(image)
			image.flags.writeable = True
			image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
			if results.multi_hand_landmarks:
				for hand_landmarks in results.multi_hand_landmarks:
					mp_drawing.draw_landmarks(
						image,
						hand_landmarks,
						mp_hands.HAND_CONNECTIONS,
						mp_drawing_styles.get_default_hand_landmarks_style(),
						mp_drawing_styles.get_default_hand_connections_style())
				
				for hand_landmarks in results.multi_hand_landmarks:
					handList = []
					for landmark in hand_landmarks.landmark:
						x = landmark.x
						y = landmark.y
						z = landmark.z
						handList.append([x,y,z])
					if (handList[6][1] - handList[8][1])*1000 > 70:
						if reset_up_action == True:
							up_action = True
							reset_up_action = False
							print('up_action: '+str(up_action))
						else:
							up_action = False
						
					if handList[8][1] > handList[6][1]:
						reset_up_action = True
						up_action = False
					if (handList[18][1] - handList[20][1])*1000 > 70:
						right_action = True
						print('left_action: '+str(right_action))
						
					if (handList[4][0] - handList[2][0])*1000 > 70:
						left_action = True
						print('right_action: '+str(left_action))
							
					# reset
					if handList[20][1] > handList[18][1]:
						right_action = False
					if handList[2][0] > handList[4][0]:
						left_action = False
			cv2.imshow('Hand detector', cv2.flip(image, 1))
			if cv2.waitKey(1) == ord('q'):
				break
		else:
			cv2.destroyAllWindows()
		# ---
		clock.tick(fps) 
		screen.blit(menu_background, (0, 0))
		
		# screen.blit(sun_img, (100, 100))

		if main_menu == True:
			#draw logo
			screen.blit(logo, (screen_width // 2 - 200,20))
			draw_text("EASY", font_main, yellow, 180, 350)
			draw_text("HARD", font_main, yellow, screen_width - 360, 350)
			# handle logic
			if exit_button.draw():
				run = False
			if start_button.draw():
				mode="EASY"
				main_menu = False
			if start_with_hand_button.draw():
				mode="HARD"
				main_menu = False
			if setting_button.draw():
				setting_menu = True
				main_menu = False
				tile_size = 30
			if register_button.draw():
				pass
			if rank_button.draw():
				pass
				
		elif setting_menu == True:
			#draw background
			screen.fill(green)
			screen.blit(setting_background, (0,0))
			#load and save level
			if save_button.draw():
				#save level data
				pickle_out = open(f'./env/level{level}_data', 'wb')
				pickle.dump(world_data, pickle_out)
				pickle_out.close()
				world = reset_level(player, level)
				print('Save data here')
			if load_button.draw():
				#load in level data
				world_data = load_world_data()
				if world_data == None:
					world_data = generate_new_world()
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
			screen.blit(my_background, (0, 0))
			world.draw()
			if game_over == 0:
				blob_group.update()
				platform_group.update()
				#update score
				#check if a coin has been collected

				if pygame.sprite.spritecollide(player, coin_group, True):
					score += 1
					coin_fx.play()
				draw_text('X ' + str(score), font_score, white, tile_size , 6)
			
			blob_group.draw(screen)
			platform_group.draw(screen)
			lava_group.draw(screen)
			coin_group.draw(screen)
			exit_group.draw(screen)
			game_over = player.update(game_over)
			# if you click ESC

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pedding = True

			# pedding state

			if pedding==True:
				if restart_button.draw():
					pedding=False
				if menu_button.draw():
					world_data = load_world_data()
					world = reset_level(player,  level)
					game_over = 0
					score = 0
					main_menu = True
					pedding=False

			#if player has died

			if game_over == -1:
				if restart_button.draw():
					world_data = []
					world = reset_level(player,  level)
					game_over = 0
					score = 0
				if menu_button.draw():
					world_data = load_world_data()
					world = reset_level(player,  level)
					game_over = 0
					score = 0
					main_menu = True

			#if player has completed the level
			if game_over == 1:
				level += 1

				if load_world_data() != None:
					my_background = load_background()
					world_data = []
					world = reset_level(player, level)
					game_over = 0

				else:
					draw_text('YOU WIN!', font, yellow, (screen_width // 2) - 140, screen_height // 2 - 215)
					if restart_button.draw():
						level = 1
						#reset level
						world_data = []
						world = reset_level(player, level)
						game_over = 0
						score = 0
					if menu_button.draw():
						level = 1
						#reset level
						world_data = load_world_data()
						world = reset_level(player, level)
						main_menu = True
						game_over = 0
						score = 0

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

pygame.quit()
cap.release()
cv2.destroyAllWindows()