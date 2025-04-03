import pygame

class Inimigo:
    def __init__(self, x, y, nome):
        self.x = x
        self.y = y
        self.nome = nome
        self.rect = pygame.Rect(x, y, 40, 60)

    def desenhar(self, tela, camera, zoom):
        scaled_width = int(40 * zoom)
        scaled_height = int(60 * zoom)
        rect_scaled = pygame.Rect((self.x - camera.x) * zoom, (self.y - camera.y) * zoom, scaled_width, scaled_height)
        pygame.draw.rect(tela, (255, 0, 0), rect_scaled)  # Inimigo vermelho