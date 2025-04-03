import pygame

class Personagem:
    def __init__(self, x, y, map_width, map_height):
        self.x = x
        self.y = y
        self.x_anterior = x
        self.y_anterior = y
        self.map_width = map_width
        self.map_height = map_height
        self.rect = pygame.Rect(x, y, 40, 60)
        self.dinheiro = 0

    def mover(self, dx, dy):
        self.x_anterior = self.x
        self.y_anterior = self.y
        self.x += dx * 5
        self.y += dy * 5
        self.rect.topleft = (self.x, self.y)

    def desenhar(self, tela, camera, zoom):
        scaled_width = int(40 * zoom)
        scaled_height = int(60 * zoom)
        rect_scaled = pygame.Rect((self.x - camera.x) * zoom, (self.y - camera.y) * zoom, scaled_width, scaled_height)
        pygame.draw.rect(tela, (0, 255, 0), rect_scaled)  # Jogador verde