import dlib
import numpy as np
import cv2
import os
import pandas as pd
import time
import logging
import sqlite3
import datetime
import mediapipe as mp
from PIL import Image, ImageTk
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


from assets.assets import back_btn
from assets.assets import save_btn
from assets.assets import load_btn
from assets.assets import restart_btn
from assets.assets import menu_btn
from assets.assets import playnow_btn
from assets.assets import register_btn
from assets.assets import exit_btn
from assets.assets import ranking_btn
from assets.assets import easy_btn
from assets.assets import hard_btn
from assets.assets import setting_btn
from assets.assets import back_from_main_btn

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

import components.Face_Detected.get_faces_from_camera_tkinter as register
import statistic
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
main_menu = False
setting_menu = False
login_screen = True
level = 1
score = 0
pedding=False
up_action = False
left_action = False
right_action = False
reset_up_action = False
accept_save_database = True

mode="EASY"
player_name = ""

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



playnow_button = Button(screen, screen_width // 2 - 90, 450 , playnow_btn)
register_button = Button(screen, screen_width // 2 - 90 , 560, register_btn)
exit_button = Button(screen, screen_width // 2 - 90 , 670, exit_btn)



easy_button = Button(screen, 180 , 400, easy_btn)
hard_button = Button(screen, screen_width - 360 , 400, hard_btn)
setting_button = Button(screen, 180 , 500, setting_btn)
ranking_button = Button(screen, screen_width - 360, 500, ranking_btn)
exit_from_main_button = Button(screen, 180, 700 , exit_btn)
back_from_main_button = Button(screen, screen_width - 360, 700 , back_from_main_btn)
#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)


# Dlib  / Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

# Dlib landmark / Get face landmarks
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Dlib Resnet Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

# Create a connection to the database
conn = sqlite3.connect("statistic.db")
cursor = conn.cursor()

# Create a table for the current date

table_name = "statistic" 
create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, player_name TEXT, score TEXT, level TEXT, mode TEXT)"
cursor.execute(create_table_sql)


# Commit changes and close the connection
conn.commit()
conn.close()

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
				if mode== "EASY":
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
				elif mode == "HARD":
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
class Face_Recognizer:
    def __init__(self):
        self.font = cv2.FONT_ITALIC

        # FPS
        self.frame_time = 0
        self.frame_start_time = 0
        self.fps = 0
        self.fps_show = 0
        self.start_time = time.time()

        # cnt for frame
        self.frame_cnt = 0

        #  Save the features of faces in the database
        self.face_features_known_list = []
        # / Save the name of faces in the database
        self.face_name_known_list = []

        #  List to save centroid positions of ROI in frame N-1 and N
        self.last_frame_face_centroid_list = []
        self.current_frame_face_centroid_list = []

        # List to save names of objects in frame N-1 and N
        self.last_frame_face_name_list = []
        self.current_frame_face_name_list = []

        #  cnt for faces in frame N-1 and N
        self.last_frame_face_cnt = 0
        self.current_frame_face_cnt = 0

        # Save the e-distance for faceX when recognizing
        self.current_frame_face_X_e_distance_list = []

        # Save the positions and names of current faces captured
        self.current_frame_face_position_list = []
        #  Save the features of people in current frame
        self.current_frame_face_feature_list = []

        # e distance between centroid of ROI in last and current frame
        self.last_current_frame_centroid_e_distance = 0

        #  Reclassify after 'reclassify_interval' frames
        self.reclassify_interval_cnt = 0
        self.reclassify_interval = 10

    #  "features_all.csv"  / Get known faces from "features_all.csv"
    def get_face_database(self):
        if os.path.exists("data/features_all.csv"):
            path_features_known_csv = "data/features_all.csv"
            csv_rd = pd.read_csv(path_features_known_csv, header=None)
            for i in range(csv_rd.shape[0]):
                features_someone_arr = []
                self.face_name_known_list.append(csv_rd.iloc[i][0])
                for j in range(1, 129):
                    if csv_rd.iloc[i][j] == '':
                        features_someone_arr.append('0')
                    else:
                        features_someone_arr.append(csv_rd.iloc[i][j])
                self.face_features_known_list.append(features_someone_arr)
            logging.info("Faces in Database： %d", len(self.face_features_known_list))
            return 1
        else:
            logging.warning("'features_all.csv' not found!")
            logging.warning("Please run 'get_faces_from_camera.py' "
                            "and 'features_extraction_to_csv.py' before 'face_reco_from_camera.py'")
            return 0

    def update_fps(self):
        now = time.time()
        # Refresh fps per second
        if str(self.start_time).split(".")[0] != str(now).split(".")[0]:
            self.fps_show = self.fps
        self.start_time = now
        self.frame_time = now - self.frame_start_time
        self.fps = 1.0 / self.frame_time
        self.frame_start_time = now

    @staticmethod
    # / Compute the e-distance between two 128D features
    def return_euclidean_distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

    
    # / Use centroid tracker to link face_x in current frame with person_x in last frame
    def centroid_tracker(self):
        for i in range(len(self.current_frame_face_centroid_list)):
            e_distance_current_frame_person_x_list = []
            #  For object 1 in current_frame, compute e-distance with object 1/2/3/4/... in last frame
            for j in range(len(self.last_frame_face_centroid_list)):
                self.last_current_frame_centroid_e_distance = self.return_euclidean_distance(
                    self.current_frame_face_centroid_list[i], self.last_frame_face_centroid_list[j])

                e_distance_current_frame_person_x_list.append(
                    self.last_current_frame_centroid_e_distance)

            last_frame_num = e_distance_current_frame_person_x_list.index(
                min(e_distance_current_frame_person_x_list))
            self.current_frame_face_name_list[i] = self.last_frame_face_name_list[last_frame_num]

    #  cv2 window / putText on cv2 window
    def draw_note(self, img_rd):
        #  / Add some info on windows
        cv2.putText(img_rd, "Face Recognizer with Deep Learning", (20, 40), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Frame:  " + str(self.frame_cnt), (20, 100), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "FPS:    " + str(self.fps.__round__(2)), (20, 130), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Faces:  " + str(self.current_frame_face_cnt), (20, 160), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Quit", (20, 450), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        # self.findFaceMesh(img_rd)

    # insert data in database

    


def save_statistic(name, score, level, mode):
	conn = sqlite3.connect("statistic.db")
	cursor = conn.cursor()
	cursor.execute("INSERT INTO statistic (player_name, score, level, mode) VALUES (?, ?, ?,?)", (name, score, level,mode))
	conn.commit()
	conn.close()

def get_statistic():
	conn = sqlite3.connect("statistic.db")
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM statistic")
	rows = cursor.fetchall()
	print(len(rows))
	for row in rows:
		print(row)  # Hiển thị thông tin của từng hàng
	conn.close()

get_statistic()
world_data = load_world_data()
world = World(screen, world_data, blob_group, platform_group, lava_group, coin_group, exit_group)
player = Player(screen, 100, screen_height - 130)
face_recognizer = Face_Recognizer()
# capture
cap = cv2.VideoCapture(0)
# run 
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
	
	while run:	
		# hand detector
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
		if login_screen == True:
			if player_name == "":
				if face_recognizer.get_face_database():
					face_recognizer.frame_cnt += 1
					logging.debug("Frame " + str(face_recognizer.frame_cnt) + " starts")
					flag, img_rd = cap.read()
					faces = detector(img_rd, 0)
					face_recognizer.last_frame_face_cnt = face_recognizer.current_frame_face_cnt
					face_recognizer.current_frame_face_cnt = len(faces)

					face_recognizer.last_frame_face_name_list = face_recognizer.current_frame_face_name_list[:]

					face_recognizer.last_frame_face_centroid_list = face_recognizer.current_frame_face_centroid_list
					face_recognizer.current_frame_face_centroid_list = []

					logging.debug("scene 2: / Faces cnt changes in this frame")
					face_recognizer.current_frame_face_position_list = []
					face_recognizer.current_frame_face_X_e_distance_list = []
					face_recognizer.current_frame_face_feature_list = []
					face_recognizer.reclassify_interval_cnt = 0

					if face_recognizer.current_frame_face_cnt == 0:
						logging.debug("  / No faces in this frame!!!")
						face_recognizer.current_frame_face_name_list = []
					else:
						logging.debug("  scene 2.2  Get faces in this frame and do face recognition")
						face_recognizer.current_frame_face_name_list = []
						for i in range(len(faces)):
							shape = predictor(img_rd, faces[i])
							face_recognizer.current_frame_face_feature_list.append(
								face_reco_model.compute_face_descriptor(img_rd, shape))
							face_recognizer.current_frame_face_name_list.append("unknown")
							player_name = "unknown"

						for k in range(len(faces)):
							logging.debug("  For face %d in current frame:", k + 1)
							face_recognizer.current_frame_face_centroid_list.append(
								[int(faces[k].left() + faces[k].right()) / 2,
								int(faces[k].top() + faces[k].bottom()) / 2])

							face_recognizer.current_frame_face_X_e_distance_list = []

							face_recognizer.current_frame_face_position_list.append(tuple(
								[faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))

							for i in range(len(face_recognizer.face_features_known_list)):
								if str(face_recognizer.face_features_known_list[i][0]) != '0.0':
									e_distance_tmp = face_recognizer.return_euclidean_distance(
										face_recognizer.current_frame_face_feature_list[k],
										face_recognizer.face_features_known_list[i])
									logging.debug("      with person %d, the e-distance: %f", i + 1, e_distance_tmp)
									face_recognizer.current_frame_face_X_e_distance_list.append(e_distance_tmp)
									
								else:
									face_recognizer.current_frame_face_X_e_distance_list.append(999999999)

							similar_person_num = face_recognizer.current_frame_face_X_e_distance_list.index(
								min(face_recognizer.current_frame_face_X_e_distance_list))

							if min(face_recognizer.current_frame_face_X_e_distance_list) < 0.4:
								face_recognizer.current_frame_face_name_list[k] = face_recognizer.face_name_known_list[similar_person_num]
								logging.debug("  Face recognition result: %s",
											face_recognizer.face_name_known_list[similar_person_num])
								player_name = face_recognizer.face_name_known_list[similar_person_num]
							else:
								logging.debug("  Face recognition result: Unknown person")

				cv2.namedWindow("camera", 1)
				cv2.imshow("camera", img_rd)

			
			screen.blit(logo, (screen_width // 2 - 200,20))
			draw_text("User: "+player_name, font_main, (44, 62, 80), 280, 340)
			if register_button.draw():
				register.main()
			if playnow_button.draw():
				main_menu = True
				login_screen = False
			
			if exit_button.draw():
				run = False
				break
				
		elif main_menu == True:
			screen.blit(logo, (screen_width // 2 - 200,20))
			# handle logic
			if exit_from_main_button.draw():
				run = False
				break
			if easy_button.draw():
				mode="EASY"
				main_menu = False
					
			if hard_button.draw():
				mode="HARD"
				main_menu = False
					
			if setting_button.draw():
				setting_menu = True
				main_menu = False
				tile_size = 30
				
			if back_from_main_button.draw():
				main_menu = False
				
			if ranking_button.draw():
				statistic.app.run(debug=True)
				print('statistic')
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
			pygame.display.update()
			
					
		
			
		
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
				if accept_save_database == True:
					save_statistic(player_name, level, score, mode)
					accept_save_database = False
				if restart_button.draw():
					world_data = []
					world = reset_level(player,  level)
					game_over = 0
					score = 0
					accept_save_database = True
				if menu_button.draw():
					world_data = load_world_data()
					world = reset_level(player,  level)
					game_over = 0
					score = 0
					main_menu = True
					accept_save_database = True

			#if player has completed the level
			if game_over == 1:
				level += 1
				if load_world_data() != None:
					my_background = load_background()
					world_data = []
					world = reset_level(player, level)
					game_over = 0
				else:
					if accept_save_database == True:
						save_statistic(player_name, level, score, mode)
						accept_save_database = False
					draw_text('YOU WIN!', font, yellow, (screen_width // 2) - 140, screen_height // 2 - 215)
					if restart_button.draw():
						level = 1
						#reset level
						world_data = []
						world = reset_level(player, level)
						game_over = 0
						score = 0
						accept_save_database = True
					if menu_button.draw():
						level = 1
						#reset level
						world_data = load_world_data()
						world = reset_level(player, level)
						main_menu = True
						game_over = 0
						score = 0
						accept_save_database = True

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		pygame.display.update()

pygame.quit()
cap.release()
cv2.destroyAllWindows()