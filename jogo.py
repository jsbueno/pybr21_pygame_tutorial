import pygame
import random

FUNDO = 0, 0, 0
W, H = TAMANHO = 640, 480
w, h = 32, 24
BLOCO = BL = W / w

def movimento(eventos, x, y, vx, vy):
    v = 1 / 3
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT: vx = -v
            if evento.key == pygame.K_RIGHT: vx = v
            if evento.key == pygame.K_DOWN: vy = v
            if evento.key == pygame.K_UP: vy = -v
            if evento.key == pygame.K_ESCAPE: return
        if evento.type == pygame.KEYUP:
            vx = vy = 0
    x = x + vx
    y = y + vy
    if x < 0: x= 0
    if y < 0: y= 0
    if x >= w: x = w - 1
    if y >= h: y = h - 1
    return x, y, vx, vy

def desenha(tela, x, y):
            tela.fill(FUNDO)
            pygame.draw.rect(tela, (255, 0, 0), (int(x) * BL , int(y) * BL, BL, BL))
            pygame.display.flip()


def principal():
    tela = pygame.display.set_mode(TAMANHO)
    x, y = (0, 0)
    vx, vy = 0, 0

    while True:
        eventos = pygame.event.get()
        x, y, vx, vy = movimento(eventos, x, y, vx, vy)
        desenha(tela, x, y)
        pygame.time.delay(60)

try:
    principal()
finally:
    pygame.quit()


