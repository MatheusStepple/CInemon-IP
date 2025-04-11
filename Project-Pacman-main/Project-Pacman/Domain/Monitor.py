import pygame
import random
import os
from Coletaveis import Coletaveis
class Monitor(Coletaveis):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.raio = 8
        self.cor = (128, 0, 128)  # Cor de fallback
        self.sprite_size = (64, 64)  # Tamanho do sprite na tela
        
        # Carrega um sprite aleatório
        self.sprite = self.carregar_sprite_aleatorio()
        
    def carregar_sprite_aleatorio(self):
        # Lista de possíveis arquivos de sprite
        sprite_files = ["monitor1.png", "monitor2.png", "monitor3.png"]
        sprite_dir = r"C:\Users\Gabriel Sousa\OneDrive - UFPE\Área de Trabalho\Project-Pacman-2\sprites"
        
        # Escolhe um arquivo aleatório
        sprite_file = random.choice(sprite_files)
        sprite_path = os.path.join(sprite_dir, sprite_file)
        
        try:
            sprite = pygame.image.load(sprite_path).convert_alpha()
            return pygame.transform.scale(sprite, self.sprite_size)
        except:
            print(f"Erro ao carregar sprite: {sprite_path}")
            return None
    
    def desenhar(self, tela):
        if self.sprite:
            # Desenha o sprite centralizado na posição do monitor
            tela.blit(
                self.sprite,
                (int(self.x - self.sprite_size[0] // 2),
                 int(self.y - self.sprite_size[1] // 2))
            )
        else:
            # Fallback: desenha círculo roxo se o sprite não carregou
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)

    @staticmethod
    def criar_monitores_na_matriz(matriz, tamanho_tile):
        monitores = []
        for y in range(len(matriz)):
            for x in range(len(matriz[y])):
                if matriz[y][x] == 2:  # Verifica se é chão
                    # Calcula a posição central do tile
                    pos_x = x * tamanho_tile + tamanho_tile // 2
                    pos_y = y * tamanho_tile + tamanho_tile // 2
                    monitores.append(Monitor(pos_x, pos_y))
        return monitores