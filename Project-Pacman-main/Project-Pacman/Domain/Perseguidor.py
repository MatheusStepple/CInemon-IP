import pygame
import math
import os
from collections import deque
import heapq

class Perseguidor:
    def __init__(self, x, y):
        self.x = x  # Centro horizontal do personagem
        self.y = y  # Centro vertical do personagem
        self.velocidade = 0.5
        self.raio = 9  # Hitbox circular (mesmo tamanho do protagonista)
        self.cor = (255, 0, 0)  # Vermelho para o perseguidor
        self.direcao = [0, 0]
        self.caminho = []
        self.grid_size = 24
        self.ultima_atualizacao_caminho = 0
        self.intervalo_atualizacao_caminho = 500
        self.velocidade_atual = self.velocidade
        self.fator_velocidade = 0.08
        self.velocidade_max = 3
        self.resetar_tempo()

        # Configurações do sprite (mesmo tamanho do protagonista)
        self.sprite_size = (160, 150)
        self.sprite_offset_x = 0
        self.sprite_offset_y = 0

        # Configurações de animação
        self.anim_frame = 0
        self.anim_speed = 100
        self.last_anim_update = pygame.time.get_ticks()
        self.direction = "baixo"

        # Carregar spritesheet
        sprite_path = r"C:\Users\Gabriel Sousa\OneDrive - UFPE\Área de Trabalho\Project-Pacman-2\sprites\perseguidor.png"

        self.spritesheet = pygame.image.load(sprite_path).convert_alpha()
        print(f"Perseguidor spritesheet carregado: {self.spritesheet.get_size()}")
        
        # Extrair sprites
        self.sprites = self.get_sprites(self.spritesheet, 54, 13, 64, 64)
        
        # Definir animações com verificação de segurança
        self.animations = {
            "baixo": self.sprites[130:139] if len(self.sprites) >= 139 else [self.spritesheet],
            "esquerda": self.sprites[117:126] if len(self.sprites) >= 126 else [self.spritesheet],
            "direita": self.sprites[143:152] if len(self.sprites) >= 152 else [self.spritesheet],
            "cima": self.sprites[104:113] if len(self.sprites) >= 113 else [self.spritesheet]
        }

    def get_sprites(self, sheet, linhas, colunas, largura, altura):
        sprites = []
        sheet_width, sheet_height = sheet.get_size()
        for linha in range(min(linhas, sheet_height // altura)):
            for coluna in range(min(colunas, sheet_width // largura)):
                x = coluna * largura
                y = linha * altura

                sprite = sheet.subsurface(pygame.Rect(x, y, largura, altura))
                sprite = pygame.transform.scale(sprite, (96, 96))  # Redimensiona para o tamanho do sprite
                sprites.append(sprite)
               
        return sprites if sprites else [pygame.Surface((64, 64))]

    def resetar_tempo(self):
        self.tempo_inicial = pygame.time.get_ticks()

    def get_tempo_decorrido(self):
        return (pygame.time.get_ticks() - self.tempo_inicial) / 1000
    
    def get_velocidade_atual(self):
        tempo_decorrido = self.get_tempo_decorrido()
        velocidade_acumulada = self.velocidade_atual + (self.fator_velocidade * tempo_decorrido)
        return min(velocidade_acumulada, self.velocidade_max)

    def desenhar(self, tela):
        now = pygame.time.get_ticks()
        if now - self.last_anim_update > self.anim_speed:
            self.anim_frame = (self.anim_frame + 1) % len(self.animations[self.direction])
            self.last_anim_update = now

        try:
            sprite = self.animations[self.direction][self.anim_frame]
            # Desenha o sprite centralizado (mesmo sistema do protagonista)
            tela.blit(
                sprite,
                (int(self.x - self.sprite_size[0] // 2 + self.sprite_offset_x),
                 int(self.y - self.sprite_size[1] // 2 + self.sprite_offset_y))
            )
            # Removido o desenho da hitbox para torná-la invisível
            # hitbox = self.get_hitbox()
            # pygame.draw.rect(tela, (0, 255, 0), hitbox, 2)
        except IndexError:
            print(f"Erro: Animação inválida ({self.direction}, frame {self.anim_frame})")
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)

    def get_hitbox(self):
        """Retorna a hitbox circular como um retângulo (para colisão)"""
        return pygame.Rect(
            self.x - self.raio,
            self.y - self.raio,
            self.raio * 2,
            self.raio * 2
        )

    def posicao_no_grid(self, x, y):
        return (int(x // self.grid_size), int(y // self.grid_size))
    
    def construir_grid(self, paredes, largura, altura):
        cols = largura // self.grid_size
        rows = altura // self.grid_size
        grid = [[0 for _ in range(cols)] for _ in range(rows)]
        
        for parede in paredes:
            x_start = int(parede.x // self.grid_size)
            y_start = int(parede.y // self.grid_size)
            x_end = int((parede.x + parede.width) // self.grid_size)
            y_end = int((parede.y + parede.height) // self.grid_size)
            for y in range(y_start, y_end):
                for x in range(x_start, x_end):
                    if 0 <= y < rows and 0 <= x < cols:
                        grid[y][x] = 1
        return grid
    
    def a_star(self, inicio, objetivo, grid):
        linhas = len(grid)
        cols = len(grid[0]) if linhas > 0 else 0
        
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        vizinhos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        open_set = []
        heapq.heappush(open_set, (0, inicio))
        veio_de = {}
        g_score = {inicio: 0}
        f_score = {inicio: heuristic(inicio, objetivo)}
        open_set_hash = {inicio}
        
        while open_set:
            atual = heapq.heappop(open_set)[1]
            open_set_hash.remove(atual)
            
            if atual == objetivo:
                caminho = []
                while atual in veio_de:
                    caminho.append(atual)
                    atual = veio_de[atual]
                caminho.reverse()
                return caminho
                
            for dx, dy in vizinhos:
                vizinho = (atual[0] + dx, atual[1] + dy)
                if 0 <= vizinho[0] < cols and 0 <= vizinho[1] < linhas:
                    if grid[vizinho[1]][vizinho[0]] == 1:
                        continue
                    tentative_g_score = g_score[atual] + 1
                    if vizinho not in g_score or tentative_g_score < g_score[vizinho]:
                        veio_de[vizinho] = atual
                        g_score[vizinho] = tentative_g_score
                        f_score[vizinho] = tentative_g_score + heuristic(vizinho, objetivo)
                        if vizinho not in open_set_hash:
                            heapq.heappush(open_set, (f_score[vizinho], vizinho))
                            open_set_hash.add(vizinho)
        return []
    
    def atualizar_caminho(self, player_x, player_y, paredes, largura, altura):
        agora = pygame.time.get_ticks()
        if agora - self.ultima_atualizacao_caminho > self.intervalo_atualizacao_caminho:
            self.ultima_atualizacao_caminho = agora
            inicio = self.posicao_no_grid(self.x, self.y)
            objetivo = self.posicao_no_grid(player_x, player_y)
            grid = self.construir_grid(paredes, largura, altura)
            self.caminho = self.a_star(inicio, objetivo, grid)
    
    def seguir_caminho(self):
        if not self.caminho:
            return [0, 0]
        node_x, node_y = self.caminho[0]
        centro_node_x = node_x * self.grid_size + self.grid_size // 2
        centro_node_y = node_y * self.grid_size + self.grid_size // 2
        dx = centro_node_x - self.x
        dy = centro_node_y - self.y
        distancia = math.sqrt(dx*dx + dy*dy)
        if distancia < 5:
            self.caminho.pop(0)
            return self.seguir_caminho()
        if distancia > 0:
            self.direction = "direita" if dx > abs(dy) else "esquerda" if dx < -abs(dy) else "baixo" if dy > 0 else "cima"
            return [dx/distancia, dy/distancia]
        return [0, 0]
    
    def perseguir(self, player_x, player_y, paredes, largura, altura):
        self.atualizar_caminho(player_x, player_y, paredes, largura, altura)
        self.direcao = self.seguir_caminho()
        self.velocidade_atual = self.get_velocidade_atual()

        dx = self.direcao[0] * self.velocidade_atual
        dy = self.direcao[1] * self.velocidade_atual

        # Usa o mesmo sistema de hitbox do protagonista
        hitbox = self.get_hitbox()
        
        hitbox.x += dx
        for parede in paredes:
            if hitbox.colliderect(parede):
                if dx > 0:
                    hitbox.right = parede.left
                elif dx < 0:
                    hitbox.left = parede.right
                dx = 0
        
        hitbox.y += dy
        for parede in paredes:
            if hitbox.colliderect(parede):
                if dy > 0:
                    hitbox.bottom = parede.top
                elif dy < 0:
                    hitbox.top = parede.bottom
                dy = 0
        
        self.x = hitbox.centerx
        self.y = hitbox.centery
    
    def verificar_colisao(self, player):
        distancia = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        return distancia < (self.raio + player.raio)

    def limitar_bordas(self, largura_tela, altura_tela):
        """Mantém o perseguidor dentro dos limites da tela"""
        self.x = max(self.raio, min(largura_tela - self.raio, self.x))
        self.y = max(self.raio, min(altura_tela - self.raio, self.y))