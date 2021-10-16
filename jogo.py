import pygame
import random

FUNDO = 0, 0, 0
W, H = TAMANHO = 640, 480
w, h = 16, 12
BLOCO = BL = W / w
v = 1 / 3

def movimento(eventos, x, y, vx, vy):
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

def desenha(tela, personagem, x, y):
            tela.fill(FUNDO)
            tela.blit(personagem, (round(x) * BL , round(y) * BL))
            # pygame.draw.rect(tela, (255, 0, 0), (int(x) * BL , int(y) * BL, BL, BL))
            pygame.display.flip()

def principal():
    tela = pygame.display.set_mode(TAMANHO)
    personagem = pygame.image.load("hominho.png")
    escala = 1 / (personagem.get_width() / BL)
    personagem = pygame.transform.rotozoom(personagem, 0, escala)

    x, y = (0, 0)
    vx, vy = 0, 0

    while True:
        eventos = pygame.event.get()
        x, y, vx, vy = movimento(eventos, x, y, vx, vy)
        desenha(tela, personagem, x, y)
        pygame.time.delay(60)

try:
    principal()
finally:
    pygame.quit()


