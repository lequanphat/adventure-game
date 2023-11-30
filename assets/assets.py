import pygame
pygame.init()
#define font

font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 24)
font_main = pygame.font.SysFont('Bauhaus 93', 36)
font_ranking = pygame.font.SysFont('Bauhaus 93', 22)

#load images   

background1 = pygame.image.load('./resources/img/background1.png')
background2 = pygame.image.load('./resources/img/background2.jpg')
background1 = pygame.transform.scale(background1 , (800,800))
background2 = pygame.transform.scale(background2 , (800,800))
background = [background1, background2]

menu_background = pygame.image.load('./resources/img/menu_background.jpg')

logo = pygame.image.load('./resources/img/logo.png')
setting_background = pygame.transform.scale(background1 , (600,600))
menu_background = pygame.transform.scale(menu_background , (800,800))




back_btn = pygame.image.load('./resources/img/back_btn.png')
save_btn = pygame.image.load('./resources/img/save_btn.png')
load_btn = pygame.image.load('./resources/img/load_btn.png')
restart_btn = pygame.image.load('./resources/img/restart_btn.png')
menu_btn = pygame.image.load('./resources/img/menu_btn.png')

#button
playnow_btn =  pygame.image.load('./resources/img/button/playnow.png')
register_btn =  pygame.image.load('./resources/img/button/register.png')
exit_btn =  pygame.image.load('./resources/img/button/exit.png')
ranking_btn =  pygame.image.load('./resources/img/button/ranking.png')
easy_btn = pygame.image.load('./resources/img/button/easy.png')
hard_btn = pygame.image.load('./resources/img/button/hard.png')
setting_btn = pygame.image.load('./resources/img/button/setting.png')
back_from_main_btn = pygame.image.load('./resources/img/button/back.png')
back_from_ranking_btn = pygame.image.load('./resources/img/button/back_arow.png')

#scale button

playnow_btn = pygame.transform.scale(playnow_btn , (180,60))
register_btn = pygame.transform.scale(register_btn , (180,60))
exit_btn = pygame.transform.scale(exit_btn , (180,60))
ranking_btn = pygame.transform.scale(ranking_btn , (180,60))
easy_btn = pygame.transform.scale(easy_btn , (180,60))
hard_btn = pygame.transform.scale(hard_btn , (180,60))
setting_btn = pygame.transform.scale(setting_btn , (180,60))
back_from_main_btn = pygame.transform.scale(back_from_main_btn , (180,60))
back_from_ranking_btn = pygame.transform.scale(back_from_ranking_btn , (120,60))



save_btn = pygame.transform.scale(save_btn , (130,40))
back_btn = pygame.transform.scale(back_btn , (130,40))
load_btn = pygame.transform.scale(load_btn , (130,40))





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