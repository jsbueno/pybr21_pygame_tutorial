import pygame
import random

FUNDO = 0, 0, 0
W, H = TAMANHO = 640, 480
w, h = 16, 12
BLOCO = BL = W / w
v = 1 / 3

class GameOver(Exception):
    pass

paredes = {
    "#": (255, 255, 128),
    "*": (255, 0, 0),
}

def lemapa(nome):
    dados = open(nome).readlines()
    mapa = {}
    for y, linha in enumerate(dados):
        linha = linha.strip("\n")
        for x, letra in enumerate(linha):
            mapa[x, y] = letra
    return mapa


class Personagem:
    def __init__(self, caminho, mapa, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mapa = mapa
        self.carrega_imagem(caminho)

    def movimento(self, eventos):
        ox, oy = self.x, self.y
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT: self.vx = -v
                if evento.key == pygame.K_RIGHT: self.vx = v
                if evento.key == pygame.K_DOWN: self.vy = v
                if evento.key == pygame.K_UP:
                    self.vy = -v * 3
                if evento.key == pygame.K_ESCAPE:
                    raise GameOver()
            if evento.type == pygame.KEYUP:
                self.vx = 0
                self.vy = 0
        self.x += self.vx
        self.y += self.vy
        if self.x < 0: self.x= 0
        if self.y < 0: self.y= 0
        if self.x >= w: self.x = w - 1
        if self.y >= h: self.y = h - 1

        cod = self.mapa.get((round(self.x), round(self.y)), " ")
        if cod != " ":
            self.x, self.y = ox, oy
        else:
            chao = self.mapa.get((round(self.x), round(self.y) + 1), " ")
            if chao == " ":
                self.y += v

    def carrega_imagem(self, caminho):
        imagem = pygame.image.load(caminho)
        escala = 1 / (imagem.get_width() / BL)
        imagem = pygame.transform.rotozoom(imagem, 0, escala)
        self.imagem = imagem

def desenha(tela, personagem, mapa, x, y):
            tela.fill(FUNDO)
            for mx in range(0, w):
                for my in range(0, h):
                    cod =  mapa.get((mx, my), " ")
                    if cod != " ":
                        pygame.draw.rect(tela, paredes[cod] , (mx * BL, my * BL, BL, BL))

            tela.blit(personagem, (round(x) * BL , round(y) * BL))
            # pygame.draw.rect(tela, (255, 0, 0), (int(x) * BL , int(y) * BL, BL, BL))
            pygame.display.flip()




def principal():
    tela = pygame.display.set_mode(TAMANHO)
    mapa = lemapa("mapa0.txt")
    personagem = Personagem("hominho.png", mapa, 0, 7)

    while True:
        eventos = pygame.event.get()
        personagem.movimento(eventos)
        desenha(tela, personagem.imagem, mapa, personagem.x, personagem.y)
        pygame.time.delay(60)

try:
    principal()
except GameOver:
    print("Jogo terminado sem erros!")
finally:
    pygame.quit()


