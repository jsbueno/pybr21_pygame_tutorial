import pygame
import random

FUNDO = 0, 0, 0
W, H = TAMANHO = 640, 480
w, h = 16, 12
BLOCO = BL = W / w
v = 1 / 3

class GameMessage(Exception):
    pass

class GameOver(GameMessage):
    pass

class GameNextStage(GameMessage):
    pass

monstros = []

class Mapa:
    def __init__(self, caminho, deslocamento=0, des_y=0):
        self.personagem = None
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
                atributos = objetos.get(letra, {"color": (255, 255, 255)})
                if not atributos:
                    continue
                if (classe:= atributos.get("class")):
                    entidade = classe(self, x, y)
                    if classe is Personagem:
                        self.personagem = entidade
                    else:
                        monstros.append(entidade)
                    atributos = None

                mapa[x, y] = atributos
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

class Base:
    arquivo_imagem: str

    def __init__(self,mapa, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mapa = mapa
        self.carrega_imagem()
        self.tempo_de_pulo = 0

    @property
    def esta_no_chao(self):
        return self.mapa[self.ix, self.iy + 1] is not None

    def movimento(self):
        if self.vx or self.vy:
            self.x += self.vx
            self.y += self.vy
        else:
            self.x= self.ix
            self.y= self.iy

        if self.x < 0: self.x= 0
        if self.y < 0: self.y= 0
        if self.x >= self.mapa.largura:
            self.x = self.mapa.largura - 1
        if self.y >= self.mapa.altura:
            self.y = self.mapa.altura - 1

    @property
    def ix(self):
        return round(self.x)

    @property
    def iy(self):
        return round(self.y)

    def carrega_imagem(self):
        imagem = pygame.image.load(self.arquivo_imagem)
        escala = 1 / (imagem.get_width() / BL)
        imagem = pygame.transform.rotozoom(imagem, 0, escala)
        self.imagem = imagem


class Personagem(Base):
    arquivo_imagem = "hominho.png"

    def testa_colisao(self):
        for monstro in monstros:
            if monstro.ix == self.ix and monstro.iy == self.iy:
                raise GameOver()

    def movimento(self, eventos):
        ox, oy = self.x, self.y
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT: self.vx = -v
                if evento.key == pygame.K_RIGHT: self.vx = v
                if evento.key == pygame.K_DOWN: self.vy = v
                if evento.key == pygame.K_UP or evento.key == pygame.K_SPACE:
                    if self.esta_no_chao:
                        self.vy = -v * 3
                        self.tempo_de_pulo = 2
                if evento.key == pygame.K_ESCAPE:
                    raise GameOver()
            if evento.type == pygame.KEYUP:
                self.vx = 0
                self.vy = 0

        super().movimento()

        parede_direita = self.mapa.deslocamento + w
        if self.x > parede_direita - 4 and (self.mapa.largura - self.mapa.deslocamento) > w:
            self.mapa.deslocamento += 6

        if self.x <  self.mapa.deslocamento + 4 and (self.mapa.deslocamento > 0):
            self.mapa.deslocamento -= 6

        valor = self.mapa[self.x, self.y]
        if valor:
            if valor.get("exit"):
                raise GameNextStage()

            self.x, self.y = ox, oy
        if not self.esta_no_chao:
            if self.tempo_de_pulo == 0:
                self.y += v
                if self.vy < v:
                    self.vy += v
        self.tempo_de_pulo = max(self.tempo_de_pulo - 1, 0)
        self.testa_colisao()

class Monstro(Base):
    arquivo_imagem = "personagem.png"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vx = -v

    def movimento(self):
        ox, oy = self.x, self.y
        super().movimento()
        if self.mapa[self.x, self.y] or not self.esta_no_chao:
            self.x = ox
            self.y = oy
            self.vx = -self.vx

objetos = {
    " ": None,
    "#": {"color":(255, 255, 128)},
    "*": { "color": (255, 0, 0)},
    "E": {"exit": True, "color": (0, 255, 0)},
    "M": {"class": Monstro, "color": (0, 0, 255)},
    "P": {"class": Personagem, "color": (0, 0, 255)},
}

def desenha(tela, personagens, mapa):
            tela.fill(FUNDO)

            # desenha mapa
            for mx in range(w):
                for my in range(h):
                    valor = mapa[mapa.deslocamento + mx, mapa.des_y + my]
                    if valor:
                        pygame.draw.rect(tela, valor["color"] , (mx * BL, my * BL, BL, BL))

            # desenha personagens:
            for personagem in personagens:
                if personagem.vx or personagem.vy:
                    x = (personagem.ix - mapa.deslocamento) * BL
                    y = (personagem.iy - mapa.des_y) * BL
                else:
                    x = round((personagem.ix - mapa.deslocamento) * BL)
                    y = round((personagem.iy - mapa.des_y) * BL)
                if x >= 0 and x + BL < W and y >= 0 and y + BL < H:
                    tela.blit(personagem.imagem, (x, y))

            pygame.display.flip()


def principal():
    tela = pygame.display.set_mode(TAMANHO)
    mapa = Mapa("mapa0.txt")

    while True:
        eventos = pygame.event.get()
        try:
            mapa.personagem.movimento(eventos)
        except GameNextStage:
            print("Essa era a última fase: você ganhou")
            raise
        for monstro in monstros:
            monstro.movimento()

        desenha(tela, [mapa.personagem, *monstros], mapa)
        pygame.time.delay(60)

try:
    principal()
except GameMessage:
    print("Jogo terminado sem erros!")
finally:
    pygame.quit()


