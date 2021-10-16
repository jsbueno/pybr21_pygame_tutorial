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


class Mapa:
    def __init__(self, caminho, deslocamento=0, des_y=0):
        self.dados = self.le_mapa(caminho)
        self.deslocamento = deslocamento
        self.des_y = des_y

    def le_mapa(self, nome):
        dados = open(nome).readlines()
        mapa = {}
        max_x = 0
        for y, linha in enumerate(dados):
            linha = linha.strip("\n")
            for x, letra in enumerate(linha):
                mapa[x, y] = letra
            if x > max_x:
                max_x = x
        self.altura = len(dados)
        self.largura = max_x
        return mapa

    def __getitem__(self, posicao):
        x, y = posicao
        valor = self.dados.get((round(x) , round(y)) )
        if valor == " ":
            valor = None
        return valor



class Personagem:
    def __init__(self, caminho, mapa, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mapa = mapa
        self.carrega_imagem(caminho)
        self.pulo = False
        self.tempo_de_queda = 0

    def movimento(self, eventos):
        ox, oy = self.x, self.y
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT: self.vx = -v
                if evento.key == pygame.K_RIGHT: self.vx = v
                if evento.key == pygame.K_DOWN: self.vy = v
                if evento.key == pygame.K_UP:
                    if self.tempo_de_queda == 0:
                        self.vy = -v * 3
                        self.pulo = True
                    elif self.tempo_de_queda == 1 and self.pulo:
                        self.vy = -v * 3
                        self.pulo = True

                if evento.key == pygame.K_ESCAPE:
                    raise GameOver()
            if evento.type == pygame.KEYUP:
                self.vx = 0
                self.vy = 0
        self.x += self.vx
        self.y += self.vy

        parede_direita = self.mapa.deslocamento + w
        if self.x > parede_direita - 4 and (self.mapa.largura - self.mapa.deslocamento) > w:
            self.mapa.deslocamento += 6

        if self.x <  self.mapa.deslocamento + 4 and (self.mapa.deslocamento > 0):
            self.mapa.deslocamento -= 6
            #if self.mapa.deslocamento < 0:
                #self.mapa.deslocamento = 0

        if self.x < 0: self.x= 0
        if self.y < 0: self.y= 0
        if self.x >= self.mapa.largura: self.x = self.mapa.largura - 1
        if self.y >= self.mapa.altura: self.y = self.mapa.altura - 1

        if self.mapa[self.x, self.y]:
            self.x, self.y = ox, oy
        else:
            chao = self.mapa[self.x, self.y + 1]
            if not chao:
                self.y += v
                self.tempo_de_queda += 1
                if self.vy > 0:
                    self.vy -= v
            else:
                self.pulo = False
                self.tempo_de_queda = 0

    def carrega_imagem(self, caminho):
        imagem = pygame.image.load(caminho)
        escala = 1 / (imagem.get_width() / BL)
        imagem = pygame.transform.rotozoom(imagem, 0, escala)
        self.imagem = imagem

def desenha(tela, personagem, mapa):
            tela.fill(FUNDO)
            for mx in range(w):
                for my in range(h):
                    valor = mapa[mapa.deslocamento + mx, mapa.des_y + my]
                    if valor:
                        pygame.draw.rect(tela, paredes[valor] , (mx * BL, my * BL, BL, BL))

            x = round((personagem.x - mapa.deslocamento) * BL)
            y = round((personagem.y - mapa.des_y) * BL)
            tela.blit(personagem.imagem, (x, y))
            # pygame.draw.rect(tela, (255, 0, 0), (int(x) * BL , int(y) * BL, BL, BL))
            pygame.display.flip()


def principal():
    tela = pygame.display.set_mode(TAMANHO)
    mapa = Mapa("mapa0.txt")
    personagem = Personagem("hominho.png", mapa, 0, 7)

    while True:
        eventos = pygame.event.get()
        personagem.movimento(eventos)
        desenha(tela, personagem, mapa,)
        pygame.time.delay(60)

try:
    principal()
except GameOver:
    print("Jogo terminado sem erros!")
finally:
    pygame.quit()


