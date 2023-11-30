
import pygame
import sys
# Khởi tạo Pygame
pygame.init()
# Cài đặt màu sắc RGB
WHITE = (255, 255, 255)
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Hello, World! with Pygame')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Xóa màn hình với màu trắng
    screen.fill(WHITE)
    # Vẽ chuỗi "Hello, World!"
    font = pygame.font.SysFont(None, 48)
    text = font.render('Hello, World!', True, (0, 0, 0))
    screen.blit(text, (300, 250))
    pygame.display.flip()
# Kết thúc Pygame
pygame.quit()
sys.exit()



