import pygame
pygame.init()
from env.constants import tile_size
from components.Enemy import Enemy
from components.Platform import Platform
from components.Lava import Lava
from components.Coin import Coin
from components.Exit import Exit

class World():
	def __init__(self, screen, data, blob_group, platform_group, lava_group, coin_group, exit_group):
		self.tile_list = []
		self.screen = screen
		self.blob_group = blob_group
		self.platform_group = platform_group
		self.lava_group = lava_group
		self.coin_group = coin_group
		self.exit_group = exit_group

		#load images
		dirt_img = pygame.image.load('./resources/img/dirt.png')
		grass_img = pygame.image.load('./resources/img/grass.png')
		
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
					self.blob_group.add(blob)
				if tile == 4:
					platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
					self.platform_group.add(platform)
				if tile == 5:
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
					self.platform_group.add(platform)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					self.lava_group.add(lava)
				if tile == 7:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					self.coin_group.add(coin)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					self.exit_group.add(exit)
				col_count += 1
			row_count += 1


	def draw(self):
		for tile in self.tile_list:
			self.screen.blit(tile[0], tile[1])