import pygame
import os
from config import BRANCO,PRETO,VERMELHO,AZUL,VERDE,AMARELO,CINZA,ROXO,LARANJA,MARROM,AZUL_ESCURO
 
class Inimigo:
    def __init__(self, x, y, nome):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 40, 60)
        if nome == 'Pedro':
            self.cor = VERMELHO
            caminho_imagem = os.path.join("Desktop", "CInemon-IP","graphics", "Fotos", "pedro.manhas.jpeg")
            self.imagem = pygame.image.load(caminho_imagem)
            self.imagem = pygame.transform.scale(self.imagem, (40, 60))
        elif nome == 'pooh':
            self.cor = VERDE
            caminho_imagem = os.path.join("Desktop", "CInemon-IP","graphics", "Fotos", "pooh.png")
            self.imagem = pygame.image.load(caminho_imagem)
            self.imagem = pygame.transform.scale(self.imagem, (40, 60))
        elif nome == 'Gusto':
            self.cor = LARANJA
        else:
            self.cor = CINZA
        self.nome = nome
       
    def desenhar(self, tela, camera):
        rect_tela = pygame.Rect(self.x - camera.x, self.y - camera.y, 40, 60)
        if self.nome == 'Pedro':
            tela.blit(self.imagem, rect_tela)
        elif self.nome == 'pooh':
            tela.blit(self.imagem, rect_tela)
        else: 
            pygame.draw.rect(tela, self.cor, rect_tela)
            pygame.draw.circle(tela, (200, 150, 100), 
                            (self.x - camera.x + 20, self.y - camera.y + 15), 10)
            pygame.draw.rect(tela, PRETO, 
                            (self.x - camera.x + 10, self.y - camera.y + 10, 20, 5), 2)
            pygame.draw.rect(tela, PRETO, 
                            (self.x - camera.x + 5, self.y - camera.y + 10, 5, 5), 2)
            pygame.draw.rect(tela, PRETO, 
                            (self.x - camera.x + 25, self.y - camera.y + 10, 5, 5), 2)