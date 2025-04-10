import pygame
import os
import jogo_base



class Gema:
    def __init__(self, x, y):
        self.x = x  # Posição X no mundo
        self.y = y  # Posição Y no mundo
        self.collected = False  # Estado de coleta
        self.width = 32  # Tamanho visual do sprite
        self.height = 32
        self.rect = pygame.Rect(self.x + 8, self.y + 8, 16, 16)  # Hitbox menor para colisão
        
        # Carrega o sprite da gema
        sprite_path = os.path.join("Desktop", "CInemon-IP", "sprites", "spr_gema_coletável_2.png")
        
        
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
        

    def desenhar(self, tela, camera, zoom):
        if not self.collected:
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