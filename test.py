
import pygame
import sys
# Khởi tạo Pygame
pygame.init()
# Cấu hình một số thông số cửa sổ
window_width, window_height = 400, 300
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Hello, Pygame!')
# Màu sắc (RGB)
white = (255, 255, 255)
black = (0, 0, 0)
# Font và văn bản
font = pygame.font.Font(None, 36)
text = font.render('Hello, World!', True, black)
text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Xóa màn hình và vẽ văn bản
    window.fill(white)
    window.blit(text, text_rect)
    pygame.display.flip()

# Kết thúc Pygame khi kết thúc chương trình
pygame.quit()
sys.exit()


