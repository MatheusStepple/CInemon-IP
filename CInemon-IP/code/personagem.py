import pygame
from config import BRANCO,PRETO,VERMELHO,AZUL,VERDE,AMARELO,CINZA,ROXO,LARANJA,MARROM,AZUL_ESCURO


class Personagem:
    def __init__(self, x, y, map_width, map_height):
        self.x = x
        self.y = y
        self.velocidade = 5
        self.rect = pygame.Rect(x, y, 40, 60)
        self.cor = AZUL
        self.direcao = "baixo"
        self.map_width = map_width
        self.map_height = map_height
        self.dinheiro = 0 # inicializa a variavel dinheiro do personagem
        self.x_anterior = x  
        self.y_anterior = y  
        
    def mover(self, dx, dy):
        # Guarda a posição anterior antes de mover
        self.x_anterior = self.x
        self.y_anterior = self.y
        
        # Calcula a nova posição
        self.x += dx * self.velocidade
        self.y += dy * self.velocidade
        
        # Atualiza direção
        if dx > 0:
            self.direcao = "direita"
        elif dx < 0:
            self.direcao = "esquerda"
        if dy > 0:
            self.direcao = "baixo"
        elif dy < 0:
            self.direcao = "cima"
            
        # Mantém dentro dos limites do mapa
        self.x = max(0, min(self.map_width - 40, self.x))
        self.y = max(0, min(self.map_height - 60, self.y))
        self.rect = pygame.Rect(self.x, self.y, 40, 60)
    
    def desenhar(self, tela, camera):
        rect_tela = pygame.Rect(self.x - camera.x, self.y - camera.y, 40, 60)
        pygame.draw.rect(tela, self.cor, rect_tela)
        pygame.draw.circle(tela, (255, 200, 150), 
                         (self.x - camera.x + 20, self.y - camera.y + 15), 10)
        
        if self.direcao == "direita":
            pygame.draw.circle(tela, PRETO, (self.x - camera.x + 25, self.y - camera.y + 13), 3)
        elif self.direcao == "esquerda":
            pygame.draw.circle(tela, PRETO, (self.x - camera.x + 15, self.y - camera.y + 13), 3)
        else:
            pygame.draw.circle(tela, PRETO, (self.x - camera.x + 17, self.y - camera.y + 13), 3)
            pygame.draw.circle(tela, PRETO, (self.x - camera.x + 23, self.y - camera.y + 13), 3)