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


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
# define game variables
clock = pygame.time.Clock()
run = True
level= 1
pending = False
game_over = 0
main_menu = True
setting_menu = False
score = 0
move_tracking = ""
# init screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")


# create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

# Dlib  / Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

# Dlib landmark / Get face landmarks
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Dlib Resnet Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

# Create a connection to the database
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Create a table for the current date
current_date = datetime.datetime.now().strftime("%Y_%m_%d")  # Replace hyphens with underscores
table_name = "attendance" 
create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (name TEXT, score TEXT, date DATE, UNIQUE(name, date))"
cursor.execute(create_table_sql)


# Commit changes and close the connection
conn.commit()
conn.close()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function to reset level
def reset_level(player, level):
    print("level: " + str(level))
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()
    player.reset(100, screen_height - 130)
    # load in level data and create world
    world_data = load_world_data()
    world = World(
        screen,
        world_data,
        blob_group,
        platform_group,
        lava_group,
        coin_group,
        exit_group,
    )
    # create dummy coin for showing the score
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)
    return world


def draw_grid():
    for c in range(21):
        # vertical lines
        pygame.draw.line(
            screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin)
        )
        # horizontal lines
        pygame.draw.line(
            screen, white, (0, c * tile_size), (screen_width - 200, c * tile_size)
        )


def draw_world():
    for row in range(20):
        for col in range(20):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    # dirt blocks
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 2:
                    # grass blocks
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 3:
                    # enemy blocks
                    img = pygame.transform.scale(
                        blob_img, (tile_size, int(tile_size * 0.75))
                    )
                    screen.blit(
                        img, (col * tile_size, row * tile_size + (tile_size * 0.25))
                    )
                if world_data[row][col] == 4:
                    # horizontally moving platform
                    img = pygame.transform.scale(
                        platform_x_img, (tile_size, tile_size // 2)
                    )
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 5:
                    # vertically moving platform
                    img = pygame.transform.scale(
                        platform_y_img, (tile_size, tile_size // 2)
                    )
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 6:
                    # lava
                    img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
                    screen.blit(
                        img, (col * tile_size, row * tile_size + (tile_size // 2))
                    )
                if world_data[row][col] == 7:
                    # coin
                    img = pygame.transform.scale(
                        coin_img, (tile_size // 2, tile_size // 2)
                    )
                    screen.blit(
                        img,
                        (
                            col * tile_size + (tile_size // 4),
                            row * tile_size + (tile_size // 4),
                        ),
                    )
                if world_data[row][col] == 8:
                    # exit
                    img = pygame.transform.scale(
                        exit_img2, (tile_size, int(tile_size * 1.5))
                    )
                    screen.blit(
                        img, (col * tile_size, row * tile_size - (tile_size // 2))
                    )


# load in level data and create world
def generate_new_world():
    new_world = []
    for i in range(0, 20):
        list = []
        for j in range(0, 20):
            list.append(0)
        new_world.append(list)
    for i in range(0, 20):
        new_world[0][i] = 1
        new_world[19][i] = 1
        new_world[i][0] = 1
        new_world[i][19] = 1
    return new_world


def load_world_data():
    if path.exists(f"./env/level{level}_data"):
        pickle_in = open(f"./env/level{level}_data", "rb")
        world_data = pickle.load(pickle_in)
        return world_data


def load_background():
    my_background = background[random.randint(0, 1)]
    return my_background


class Player:
    def __init__(self, screen, x, y):
        self.reset(x, y)
        self.screen = screen
        self.world = world
        self.blob_group = blob_group
        self.platform_group = platform_group
        self.lava_group = lava_group
        self.exit_group = exit_group

    def update(self, game_over,move_tracking):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20
        if game_over == 0:
            if pending == False:
                if (
                    move_tracking=="Up"
                    and self.jumped == False
                    and self.in_air == False
                ):
                    jump_fx.play()
                    self.vel_y = -15
                    self.jumped = True
                if move_tracking =="Up" == False:
                    self.jumped = False

                if move_tracking=="Left":
                    dx -= 5
                    self.counter += 1
                    self.direction = -1

                if move_tracking=="Right":
                    dx += 5
                    self.counter += 1
                    self.direction = 1

                if move_tracking=="Left" == False and move_tracking=="Right" == False:
                    self.counter = 0
                    self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(
                    self.rect.x + dx, self.rect.y, self.width, self.height
                ):
                    dx = 0

                if tile[1].colliderect(
                    self.rect.x, self.rect.y + dy, self.width, self.height
                ):
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
                if platform.rect.colliderect(
                    self.rect.x + dx, self.rect.y, self.width, self.height
                ):
                    dx = 0

                if platform.rect.colliderect(
                    self.rect.x, self.rect.y + dy, self.width, self.height
                ):
                    # check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # move sideways with the platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text(
                "GAME OVER!",
                font,
                blue,
                (screen_width // 2) - 180,
                screen_height // 2 - 215,
            )
            if self.rect.y > 200:
                self.rect.y -= 5

        # draw player onto screen
        self.screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        for num in range(1, 5):
            img_right = pygame.image.load(f"./resources/img/guy{num}.png")
            img_right = pygame.transform.scale(img_right, (32, 68))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.dead_image = pygame.image.load("./resources/img/ghost.png")
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
    def __init__(self, move_tracking):

        self.my_background = background[0]
        
        self.load_button = Button(screen, screen_width - 165, 30, load_btn)
        self.save_button = Button(screen, screen_width - 165, 80, save_btn)
        self.back_button = Button(screen, screen_width - 165, 130, back_btn)
        # for game
        self.restart_button = Button(
            screen, screen_width // 2 - 50, screen_height // 2 - 100, restart_btn
        )
        self.menu_button = Button(screen, screen_width // 2 - 50, screen_height // 2 - 20, menu_btn)


        self.start_button = Button(screen, screen_width // 2 - 120, 360, play_btn)
        self.setting_button = Button(screen, screen_width // 2 - 120, 500, setting_btn)
        self.exit_button = Button(screen, screen_width // 2 - 120, 640, exit_btn)
        self.font = cv2.FONT_ITALIC
        self.move_tracking = move_tracking
        # FPS
        self.frame_time = 0
        self.frame_start_time = 0
        self.fps = 0
        self.fps_show = 0
        self.start_time = time.time()

        self.staticMode = False
        self.maxFaces= 3
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode,self.maxFaces)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness =1,circle_radius=1)
        # cnt for frame
        self.frame_cnt = 0
        self.my_background = background[0]
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
    
    def findFaceMesh(self, frame,draw=True):
        self.imgRGB =cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result =self.faceMesh.process(self.imgRGB)
        faces =[]
        if(self.result.multi_face_landmarks):
            for faceLms in self.result.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, faceLms, self.mpFaceMesh.FACEMESH_TESSELATION, self.drawSpec, self.drawSpec)
                face =[]
                for id, lm in enumerate(faceLms.landmark):
                    ih, iw,ic = frame.shape
                    x,y = int(lm.x*iw), int(lm.y*ih)
                    
                    face.append([x,y])
                faces.append(face)
        return frame,faces
    
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
        cv2.putText(img_rd, "Move Tracking:  " + str(self.move_tracking), (20, 190), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Quit", (20, 450), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        # self.findFaceMesh(img_rd)

    # insert data in database

    def attendance(self, name):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        # Check if the name already has an entry for the current date
        cursor.execute("SELECT * FROM attendance WHERE name = ? AND date = ?", (name, current_date))
        existing_entry = cursor.fetchone()

        if existing_entry:
            print(f"{name} is already marked as present for {current_date}")
        else:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            cursor.execute("INSERT INTO attendance (name, time, date) VALUES (?, ?, ?)", (name, current_time, current_date))
            conn.commit()
            print(f"{name} marked as present for {current_date} at {current_time}")

        conn.close()

    #  Face detection and recognition wit OT from input video stream
    def process(self, stream, run, tile_size, world, world_data, pending, game_over, main_menu, setting_menu, level, score):
        # 1.  Get faces known from "features.all.csv"
        if self.get_face_database() :
            while stream.isOpened() and run:
                screen.blit(menu_background, (0, 0))
                self.frame_cnt += 1
                logging.debug("Frame " + str(self.frame_cnt) + " starts")
                flag, img_rd = stream.read()
                kk = cv2.waitKey(1)

                # 2.  Detect faces for frame X
                faces = detector(img_rd, 0)

                # 3.  Update cnt for faces in frames
                self.last_frame_face_cnt = self.current_frame_face_cnt
                self.current_frame_face_cnt = len(faces)

                # 4.  Update the face name list in last frame
                self.last_frame_face_name_list = self.current_frame_face_name_list[:]

                # 5.  update frame centroid list
                self.last_frame_face_centroid_list = self.current_frame_face_centroid_list
                self.current_frame_face_centroid_list = []

                if (self.current_frame_face_cnt == self.last_frame_face_cnt) and (
                        self.reclassify_interval_cnt != self.reclassify_interval):
                    logging.debug("scene 1:   No face cnt changes in this frame!!!")

                    self.current_frame_face_position_list = []

                    if "unknown" in self.current_frame_face_name_list:
                        self.reclassify_interval_cnt += 1

                    if self.current_frame_face_cnt != 0:
                        for k, d in enumerate(faces):
                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])
                            motion_detected = False
                            img_rd = cv2.rectangle(img_rd,
                                                   tuple([d.left(), d.top()]),
                                                   tuple([d.right(), d.bottom()]),
                                                   (255, 255, 255), 2)
                            for i in range(self.current_frame_face_cnt):
                                x_diff = self.current_frame_face_centroid_list[i][0] - self.last_frame_face_centroid_list[i][0]
                                y_diff = self.current_frame_face_centroid_list[i][1] - self.last_frame_face_centroid_list[i][1]

                                if abs(x_diff) > 0.7:
                                    if x_diff < 0:
                                        self.move_tracking = "Left"
                                    else:
                                       self.move_tracking = "Right"
                                    motion_detected = True
                                    break
                                if abs(y_diff) > 0.7:
                                    if y_diff < 0:
                                        self.move_tracking = "Up"
                                    motion_detected = True
                                    break

                            if not motion_detected:
                                self.move_tracking = ""

                    #  Multi-faces in current frame, use centroid-tracker to track
                    if self.current_frame_face_cnt != 1:
                        self.centroid_tracker()

                    for i in range(self.current_frame_face_cnt):
                        # 6.2 Write names under ROI
                        img_rd = cv2.putText(img_rd, self.current_frame_face_name_list[i],
                                             self.current_frame_face_position_list[i], self.font, 0.8, (0, 255, 255), 1,
                                             cv2.LINE_AA)
                    self.draw_note(img_rd)

                # 6.2  If cnt of faces changes, 0->1 or 1->0 or ...
                else:
                    logging.debug("scene 2: / Faces cnt changes in this frame")
                    self.current_frame_face_position_list = []
                    self.current_frame_face_X_e_distance_list = []
                    self.current_frame_face_feature_list = []
                    self.reclassify_interval_cnt = 0

                    # 6.2.1  Face cnt decreases: 1->0, 2->1, ...
                    if self.current_frame_face_cnt == 0:
                        logging.debug("  / No faces in this frame!!!")
                        # clear list of names and features
                        self.current_frame_face_name_list = []
                    # 6.2.2 / Face cnt increase: 0->1, 0->2, ..., 1->2, ...
                    else:
                        logging.debug("  scene 2.2  Get faces in this frame and do face recognition")
                        self.current_frame_face_name_list = []
                        for i in range(len(faces)):
                            shape = predictor(img_rd, faces[i])
                            self.current_frame_face_feature_list.append(
                                face_reco_model.compute_face_descriptor(img_rd, shape))
                            self.current_frame_face_name_list.append("unknown")

                        # 6.2.2.1 Traversal all the faces in the database
                        for k in range(len(faces)):
                            logging.debug("  For face %d in current frame:", k + 1)
                            self.current_frame_face_centroid_list.append(
                                [int(faces[k].left() + faces[k].right()) / 2,
                                 int(faces[k].top() + faces[k].bottom()) / 2])

                            self.current_frame_face_X_e_distance_list = []

                            # 6.2.2.2  Positions of faces captured
                            self.current_frame_face_position_list.append(tuple(
                                [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))

                            # 6.2.2.3 
                            # For every faces detected, compare the faces in the database
                            for i in range(len(self.face_features_known_list)):
                                # 
                                if str(self.face_features_known_list[i][0]) != '0.0':
                                    e_distance_tmp = self.return_euclidean_distance(
                                        self.current_frame_face_feature_list[k],
                                        self.face_features_known_list[i])
                                    logging.debug("      with person %d, the e-distance: %f", i + 1, e_distance_tmp)
                                    self.current_frame_face_X_e_distance_list.append(e_distance_tmp)
                                    
                                else:
                                    #  person_X
                                    self.current_frame_face_X_e_distance_list.append(999999999)

                            # 6.2.2.4 / Find the one with minimum e distance
                            similar_person_num = self.current_frame_face_X_e_distance_list.index(
                                min(self.current_frame_face_X_e_distance_list))

                            if min(self.current_frame_face_X_e_distance_list) < 0.4:
                                self.current_frame_face_name_list[k] = self.face_name_known_list[similar_person_num]
                                logging.debug("  Face recognition result: %s",
                                              self.face_name_known_list[similar_person_num])
                                
                                # Insert attendance record
                                name =self.face_name_known_list[similar_person_num]

                                
                                self.attendance(name)
                            else:
                                logging.debug("  Face recognition result: Unknown person")

                        # 7.  / Add note on cv2 window
                        self.draw_note(img_rd)
                if main_menu == True:
                    # draw logo
                    screen.blit(logo, (screen_width // 2 - 200, 20))
                    # handle logic
                    if self.exit_button.draw():
                        run = False
                    if self.start_button.draw():
                        main_menu = False
                    if self.setting_button.draw():
                        setting_menu = True
                        main_menu = False
                        self.tile_size = 30
                elif setting_menu == True:
                    # draw background
                    screen.fill(green)
                    screen.blit(setting_background, (0, 0))
                    # load and save level
                    if self.save_button.draw():
                        # save level data
                        pickle_out = open(f"./env/level{level}_data", "wb")
                        pickle.dump(world_data, pickle_out)
                        pickle_out.close()
                        world = reset_level(player, level)
                        print("Save data here")
                    if self.load_button.draw():
                        # load in level data
                        world_data = load_world_data()
                        if world_data == None:
                            world_data = generate_new_world()
                    if self.back_button.draw():
                        setting_menu = False
                        main_menu = True

                    # show the grid and draw the level tiles
                    draw_grid()
                    draw_world()

                    # text showing current level
                    draw_text(
                        f"Level: {level}",
                        pygame.font.SysFont("Futura", 32),
                        white,
                        100,
                        screen_height - 140,
                    )
                    draw_text(
                        "Press UP or DOWN to change level",
                        pygame.font.SysFont("Futura", 32),
                        white,
                        100,
                        screen_height - 110,
                    )

                    # event handler
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                            clicked = True
                            pos = pygame.mouse.get_pos()
                            x = pos[0] // tile_size
                            y = pos[1] // tile_size
                            # check that the coordinates are within the tile area
                            if x < 20 and y < 20:
                                # update tile value
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
                        # up and down key presses to change level number
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                level += 1
                            elif event.key == pygame.K_DOWN and level > 1:
                                level -= 1
                    # update game display window
                    pygame.display.update()

                    # end
                else:
                    screen.blit(self.my_background, (0, 0))
                    world.draw()
                    if game_over == 0:
                        blob_group.update()
                        platform_group.update()

                        if pygame.sprite.spritecollide(player, coin_group, True):
                            score += 1
                            coin_fx.play()
                        draw_text("X " + str(score), font_score, white, tile_size, 6)

                    blob_group.draw(screen)
                    platform_group.draw(screen)
                    lava_group.draw(screen)
                    coin_group.draw(screen)
                    exit_group.draw(screen)
                    game_over = player.update(game_over,self.move_tracking)
                    # if you click ESC

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.pending = True

                    # pending state

                    if pending == True:
                        if self.restart_button.draw():
                            pending = False
                        if self.menu_button.draw():
                            world_data = load_world_data()
                            world = reset_level(player, level)
                            game_over = 0
                            score = 0
                            main_menu = True
                            pending = False

                    # if player has died

                    if game_over == -1:
                        if self.restart_button.draw():
                            world_data = []
                            world = reset_level(player, level)
                            game_over = 0
                            score = 0
                        if self.menu_button.draw():
                            world_data = load_world_data()
                            world = reset_level(player, level)
                            game_over = 0
                            score = 0
                            main_menu = True

                    # if player has completed the level
                    if game_over == 1:
                        level += 1

                        if load_world_data() != None:
                            self.my_background = load_background()
                            world_data = []
                            world = reset_level(player, level)
                            game_over = 0

                        else:
                            draw_text(
                                "YOU WIN!",
                                font,
                                yellow,
                                (screen_width // 2) - 140,
                                screen_height // 2 - 215,
                            )
                            if self.restart_button.draw():
                                level = 1
                                # reset level
                                world_data = []
                                world = reset_level(player, level)
                                game_over = 0
                                score = 0
                            if self.menu_button.draw():
                                level = 1
                                # reset level
                                world_data = load_world_data()
                                world = reset_level(player, level)
                                main_menu = True
                                game_over = 0
                                score = 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                pygame.display.update()
                self.update_fps()
                cv2.namedWindow("camera", 1)
                cv2.imshow("camera", img_rd)

                logging.debug("Frame ends\n\n")



world_data = load_world_data()
world = World(
    screen, world_data, blob_group, platform_group, lava_group, coin_group, exit_group
)
player = Player(screen, 100, screen_height - 130)
cap = cv2.VideoCapture(0)
face_reg = Face_Recognizer(move_tracking)

clock.tick(fps)
screen.blit(menu_background, (0, 0))
face_reg.process(cap, run, tile_size, world, world_data, pending, game_over, main_menu, setting_menu, level, score)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
