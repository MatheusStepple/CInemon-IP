import pygame
import os
from config import BRANCO, PRETO, VERMELHO, AZUL, VERDE, AMARELO, CINZA, ROXO, LARANJA, MARROM, AZUL_ESCURO

class Inimigo:
    def __init__(self, x, y, nome):
        self.x = x
        self.y = y
        self.nome = nome
        self.rect = pygame.Rect(x, y, 40, 60)

        # Define a cor e a imagem com base no nome do inimigo
        if nome == 'Pedro':
            self.cor = VERMELHO
            caminho_imagem = os.path.join("Desktop", "CInemon-IP", "graphics", "Fotos", "pedro.manhas.jpeg")
            
            self.imagem = pygame.image.load(caminho_imagem)
            self.imagem = pygame.transform.scale(self.imagem, (20, 30))
            self.tem_imagem = True
            
        elif nome == 'pooh':
            self.cor = VERDE
            caminho_imagem = os.path.join("Desktop", "CInemon-IP", "sprites", "spr_ricardo.png")
            
            self.imagem = pygame.image.load(caminho_imagem)
            self.imagem = pygame.transform.scale(self.imagem, (31, 31))
            self.tem_imagem = True
            
        elif nome == 'Gusto':
            self.cor = LARANJA
            caminho_imagem = os.path.join("Desktop", "CInemon-IP", "sprites", "spr_fernanda_madeiral.png")
            
            self.imagem = pygame.image.load(caminho_imagem)
            self.imagem = pygame.transform.scale(self.imagem, (20, 30))
            self.tem_imagem = True
        else:
            self.cor = CINZA
            self.tem_imagem = False

    def desenhar(self, tela, camera, zoom):
        # Calcula as dimensões e posição escaladas com base no zoom
        scaled_width = int(40 * zoom)
        scaled_height = int(60 * zoom)
        pos_x = (self.x - camera.x) * zoom
        pos_y = (self.y - camera.y) * zoom
        rect_scaled = pygame.Rect(pos_x, pos_y, scaled_width, scaled_height)

        if self.tem_imagem and (self.nome == 'Pedro' or self.nome == 'pooh'):
            # Escala a imagem com base no zoom e desenha
            imagem_scaled = pygame.transform.scale(self.imagem, (scaled_width, scaled_height))
            tela.blit(imagem_scaled, (pos_x, pos_y))
        else:
            # Desenha um retângulo colorido para inimigos sem imagem
            pygame.draw.rect(tela, self.cor, rect_scaled)
            # Detalhes do rosto escalados
            centro_x = pos_x + scaled_width // 2
            centro_y = pos_y + scaled_height // 4
            raio_cabeca = int(10 * zoom)
            pygame.draw.circle(tela, (200, 150, 100), (centro_x, centro_y), raio_cabeca)  # Cabeça
            pygame.draw.rect(tela, PRETO, 
                            (centro_x - int(10 * zoom), centro_y - int(2.5 * zoom), int(20 * zoom), int(5 * zoom)), 2)  # Boca
            pygame.draw.rect(tela, PRETO, 
                            (centro_x - int(15 * zoom), centro_y - int(2.5 * zoom), int(5 * zoom), int(5 * zoom)), 2)  # Olho esquerdo
            pygame.draw.rect(tela, PRETO, 
                            (centro_x + int(10 * zoom), centro_y - int(2.5 * zoom), int(5 * zoom), int(5 * zoom)), 2)  # Olho direito