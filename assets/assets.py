import pygame
pygame.init()
#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)
#load images   
sun_img = pygame.image.load('./resources/img/sun.png')
bg_img = pygame.image.load('./resources/img/sky.png')
restart_img = pygame.image.load('./resources/img/restart_btn.png')
start_img = pygame.image.load('./resources/img/start_btn.png')
exit_img = pygame.image.load('./resources/img/exit_btn.png')
# scale image 
start_img = pygame.transform.scale(start_img , (200,100))
exit_img = pygame.transform.scale(exit_img , (200,100))
#load sounds
pygame.mixer.music.load('./resources/audio/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('./resources/audio/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('./resources/audio/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('./resources/audio/game_over.wav')
game_over_fx.set_volume(0.5)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()




