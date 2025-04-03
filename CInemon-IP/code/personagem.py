import pygame
import os
from config import BRANCO, PRETO, VERMELHO, AZUL, VERDE, AMARELO, CINZA, ROXO, LARANJA, MARROM, AZUL_ESCURO

class Personagem:
    def __init__(self, x, y, map_width, map_height):
        self.x = x
        self.y = y
        self.x_anterior = x  # Posição anterior para colisão
        self.y_anterior = y
        self.velocidade = 5  # Velocidade de movimento
        self.map_width = map_width
        self.map_height = map_height
        self.rect = pygame.Rect(x + 10, y + 15, 20, 30)  # Hitbox reduzido (centralizado no sprite)
        self.direcao = "baixo"  # Direção inicial
        self.dinheiro = 0  # Variável de dinheiro

        # Carrega o sprite do personagem com caminho relativo
        try:
            sprite_path = os.path.join("Desktop", "CInemon-IP", "sprites", "sprite_principal.png")
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            # Mantém o tamanho original do sprite
            self.sprite = pygame.transform.scale(self.sprite, (40, 60))  # Tamanho visual: 40x60
        except Exception as e:
            print(f"Erro ao carregar sprite: {e}")
            # Fallback para um retângulo azul caso o sprite não carregue
            self.sprite = None
            self.cor = AZUL

    def mover(self, dx, dy):
        # Guarda a posição anterior antes de mover
        self.x_anterior = self.x
        self.y_anterior = self.y
        
        # Calcula a nova posição
        self.x += dx * self.velocidade
        self.y += dy * self.velocidade
        
        # Atualiza direção com base no movimento
        if dx > 0:
            self.direcao = "direita"
        elif dx < 0:
            self.direcao = "esquerda"
        if dy > 0:
            self.direcao = "baixo"
        elif dy < 0:
            self.direcao = "cima"
            
        # Mantém dentro dos limites do mapa (baseado no sprite 40x60)
        self.x = max(0, min(self.map_width - 40, self.x))
        self.y = max(0, min(self.map_height - 60, self.y))
        # Atualiza o hitbox para seguir a posição, centralizado no sprite
        self.rect.topleft = (self.x + 10, self.y + 15)

    def desenhar(self, tela, camera, zoom):
        # Calcula posição escalada com base no zoom (para o sprite)
        pos_x = (self.x - camera.x) * zoom
        pos_y = (self.y - camera.y) * zoom

        if self.sprite:
            # Escala o sprite com base no zoom, mantendo tamanho original
            scaled_width = int(40 * zoom)  # Tamanho visual: 40
            scaled_height = int(60 * zoom)  # Tamanho visual: 60
            sprite_scaled = pygame.transform.scale(self.sprite, (scaled_width, scaled_height))

            # Ajusta a rotação ou flip do sprite com base na direção
            if self.direcao == "esquerda":
                sprite_scaled = pygame.transform.flip(sprite_scaled, True, False)  # Flip horizontal para esquerda
            elif self.direcao =="direita":
                sprite_scaled = sprite_scaled  # Sem flip, assume sprite voltado para a direita por padrão

            # Desenha o sprite na tela
            tela.blit(sprite_scaled, (pos_x, pos_y))
        else:
            # Fallback para desenho geométrico se o sprite não carregar
            scaled_width = int(40 * zoom)
            scaled_height = int(60 * zoom)
            rect_scaled = pygame.Rect(pos_x, pos_y, scaled_width, scaled_height)
            pygame.draw.rect(tela, self.cor, rect_scaled)