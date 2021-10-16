import pygame
import random

FUNDO = 0, 0, 0
W, H = TAMANHO = 640, 480
w, h = 32, 24
BLOCO = BL = W / w

def principal():
    tela = pygame.display.set_mode(TAMANHO)
    x, y = (0, 0)
    vx, vy = 0, 0
    while True:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type != pygame.KEYDOWN:
                continue
            if evento.key == pygame.K_LEFT: vx = -1
            if evento.key == pygame.K_RIGHT: vx = 1
            if evento.key == pygame.K_DOWN: vy = 1
            if evento.key == pygame.K_UP: vy = -1
        x = x + vx
        y = y + vy
        if x < 0: x= 0
        if y < 0: y= 0
        if x >= w: x = w - 1
        if y >= h: y = h - 1

        tela.fill(FUNDO)
        pygame.draw.rect(tela, (255, 0, 0), (x * BL , y * BL, BL, BL))
        pygame.display.flip()
        pygame.time.delay(60)

try:
    principal()
finally:
    pygame.quit()


