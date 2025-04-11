import pygame
import os
from config import BRANCO, PRETO, VERMELHO, AZUL, VERDE, AMARELO, CINZA, ROXO, LARANJA, MARROM, AZUL_ESCURO

class Personagem:
    def __init__(self, x, y, map_width, map_height, mapa_atual=None):
        self.x = x
        self.y = y
        self.x_anterior = x
        self.y_anterior = y
        self.velocidade = 5  # Velocidade padrão
        self.mapa_atual = mapa_atual  # Mapa atual (ex.: 'basic.tmx' ou 'cin.tmx')
        self.map_width = map_width
        self.map_height = map_height
        self.hitbox_width = 8
        self.hitbox_height = 8
        self.rect = pygame.Rect(self.x + 16, self.y + 26, self.hitbox_width, self.hitbox_height)
        self.direcao = "baixo"
        self.dinheiro = 0

        # Variáveis para animação
        self.frame = 0  # Índice do frame atual
        self.anim_speed = 0.2  # Velocidade da animação (quanto menor, mais rápido)
        self.anim_counter = 0  # Contador para controlar a troca de frames

        # Dicionário com sprites para cada direção
        self.sprites = {
            "direita": [
                pygame.image.load(os.path.join("Desktop", "CInemon-IP", "sprites", "Protagonista", "protagonista_direita.png")).convert_alpha(),
                pygame.image.load(os.path.join("Desktop", "CInemon-IP", "sprites", "Protagonista", "protagonista_andar_direita.png")).convert_alpha()
            ],
            "esquerda": [
                pygame.image.load(os.path.join("Desktop", "CInemon-IP", "sprites", "Protagonista", "protagonista_esquerda.png")).convert_alpha(),
                pygame.image.load(os.path.join("Desktop", "CInemon-IP", "sprites", "Protagonista", "protagonista_andar_esquerda.png")).convert_alpha()
            ],
            "baixo": [
                pygame.image.load(os.path.join("Desktop", "CInemon-IP", "sprites", "Protagonista", "protagonista_frente.png")).convert_alpha(),
                pygame.image.load(os.path.join("Desktop", "CInemon-IP", "sprites", "Protagonista", "protagonista_andar_baixo.png")).convert_alpha()
            ],
            "cima": [
                pygame.image.load(os.path.join("Desktop", "CInemon-IP", "sprites", "Protagonista", "protagonista_costas.png")).convert_alpha(),
                pygame.image.load(os.path.join("Desktop", "CInemon-IP", "sprites", "Protagonista", "protagonista_andar_cima.png")).convert_alpha()
            ]
        }

        # Redimensiona todos os sprites para 32x32
        for direcao in self.sprites:
            for i in range(len(self.sprites[direcao])):
                self.sprites[direcao][i] = pygame.transform.scale(self.sprites[direcao][i], (32, 32))

        # Sprite inicial
        self.sprite_atual = self.sprites["baixo"][0]

    def mover(self, dx, dy):
        # Ajusta a velocidade: se o mapa for cin.tmx, velocidade vira 1
        if self.mapa_atual == 'cin.tmx':
            self.velocidade = 7
        else:
            self.velocidade = 8

        self.x_anterior = self.x
        self.y_anterior = self.y
        
        self.x += dx * self.velocidade
        self.y += dy * self.velocidade
        
        # Atualiza direção
        if dx > 0:
            self.direcao = "direita"
        elif dx < 0:
            self.direcao = "esquerda"
        elif dy > 0:
            self.direcao = "baixo"
        elif dy < 0:
            self.direcao = "cima"

        # Limites do mapa
        self.x = max(0, min(self.map_width - 40, self.x))
        self.y = max(0, min(self.map_height - 60, self.y))
        
        # Atualiza o hitbox
        self.rect.x = self.x + 16
        self.rect.y = self.y + 26

        # Animação: se está se movendo, alterna os frames
        if dx != 0 or dy != 0:
            self.anim_counter += self.anim_speed
            if self.anim_counter >= 1:
                self.anim_counter = 0
                self.frame = (self.frame + 1) % 2  # Alterna entre 0 (parado) e 1 (andando)
            self.sprite_atual = self.sprites[self.direcao][self.frame]
        else:
            # Se parado, usa o sprite "parado" (frame 0)
            self.frame = 0
            self.anim_counter = 0
            self.sprite_atual = self.sprites[self.direcao][0]

    def desenhar(self, tela, camera, zoom):
        pos_x = (self.x - camera.x) * zoom
        pos_y = (self.y - camera.y) * zoom

        scaled_width = int(20 * zoom)
        scaled_height = int(30 * zoom)
        sprite_scaled = pygame.transform.scale(self.sprite_atual, (scaled_width, scaled_height))

        # Inverte o sprite para a esquerda
        tela.blit(sprite_scaled, (pos_x, pos_y))

        # Desenha o hitbox (opcional, para debug)
        hitbox_pos_x = (self.rect.x - camera.x) * zoom
        hitbox_pos_y = (self.rect.y - camera.y) * zoom
        hitbox_scaled_width = int(self.hitbox_width * zoom)
        hitbox_scaled_height = int(self.hitbox_height * zoom)
        hitbox_scaled = pygame.Rect(hitbox_pos_x, hitbox_pos_y, hitbox_scaled_width, hitbox_scaled_height)