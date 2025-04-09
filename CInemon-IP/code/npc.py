import pygame
import os

class NPC:
    def __init__(self, x, y, nome, sprite_file="spr_fernanda_madeiral.png"):
        self.x = x
        self.y = y
        self.nome = nome
        self.width = 40
        self.height = 60
        self.rect = pygame.Rect(self.x + 8, self.y + 18, 24, 36)  # Hitbox ajustada
        
        try:
            sprite_path = os.path.join("Desktop", "CInemon-IP", "sprites", sprite_file)
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
        except Exception as e:
            print(f"Erro ao carregar sprite do NPC {self.nome}: {e}")
            self.sprite = None
            self.cor = (0, 255, 255)  # Ciano como fallback

    def desenhar(self, tela, camera, zoom):
        pos_x = (self.x - camera.x) * zoom
        pos_y = (self.y - camera.y) * zoom
        scaled_width = int(self.width * zoom)
        scaled_height = int(self.height * zoom)
        
        if self.sprite:
            sprite_scaled = pygame.transform.scale(self.sprite, (scaled_width, scaled_height))
            tela.blit(sprite_scaled, (pos_x, pos_y))
        else:
            rect_scaled = pygame.Rect(pos_x, pos_y, scaled_width, scaled_height)
            pygame.draw.rect(tela, self.cor, rect_scaled)