import pygame
pygame.init()
#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)
#load images   
sun_img = pygame.image.load('./resources/img/sun.png')
bg_img = pygame.image.load('./resources/img/sky.png')
background2 = pygame.image.load('./resources/img/background2.jpg')
logo = pygame.image.load('./resources/img/logo.png')
setting_background = pygame.transform.scale(bg_img , (600,600))
background2 = pygame.transform.scale(bg_img , (800,800))



play_btn = pygame.image.load('./resources/img/play_btn.png')
exit_btn = pygame.image.load('./resources/img/exit_btn.png')
setting_btn = pygame.image.load('./resources/img/setting_btn.png')
back_btn = pygame.image.load('./resources/img/back_btn.png')
save_btn = pygame.image.load('./resources/img/save_btn.png')
load_btn = pygame.image.load('./resources/img/load_btn.png')
restart_btn = pygame.image.load('./resources/img/restart_btn.png')
menu_btn = pygame.image.load('./resources/img/menu_btn.png')


save_btn = pygame.transform.scale(save_btn , (130,40))
back_btn = pygame.transform.scale(back_btn , (130,40))
load_btn = pygame.transform.scale(load_btn , (130,40))

setting_btn = pygame.transform.scale(setting_btn , (240,90))
play_btn = pygame.transform.scale(play_btn , (240,90))
exit_btn = pygame.transform.scale(exit_btn , (240,90))

logo = pygame.transform.scale(logo , (400,300))
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