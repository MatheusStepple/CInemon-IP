import pygame
import os

class Protagonista:
    def __init__(self, x, y):
        self.x = x  # Centro horizontal do personagem (incluindo sprite)
        self.y = y  # Centro vertical do personagem (incluindo sprite)
        self.raio = 10  # Tamanho da hitbox (diâmetro 20px)
        self.velocidade = 3
        self.cor = (255, 255, 0)  # Cor de fallback (se o sprite não carregar)

        # Configurações do sprite
        self.sprite_size = (96, 96)  # Tamanho do sprite na tela
        self.sprite_offset_x = 0  # Se quiser ajustar a posição do sprite (não da hitbox)
        self.sprite_offset_y = 0

        # Configurações de animação
        self.anim_frame = 0
        self.anim_speed = 100
        self.last_anim_update = pygame.time.get_ticks()
        self.direction = "baixo"
        self.esta_movendo = False  # Novo atributo para rastrear movimento

        # Carregar spritesheet
        sprite_path = r"C:\Users\Gabriel Sousa\OneDrive - UFPE\Área de Trabalho\Project-Pacman-2\sprites\protagonista.png"

        self.spritesheet = pygame.image.load(sprite_path).convert_alpha()
        print(f"Spritesheet carregado: {self.spritesheet.get_size()}")
        # Extrair sprites
        self.sprites = self.get_sprites(self.spritesheet, 54, 13, 64, 64)
        self.animations = {
            "baixo": self.sprites[130:139],
            "esquerda": self.sprites[117:126],
            "direita": self.sprites[143:152],
            "cima": self.sprites[104:113]
        }

    def get_sprites(self, sheet, linhas, colunas, largura, altura):
        sprites = []
        for linha in range(min(linhas, sheet.get_height() // altura)):
            for coluna in range(min(colunas, sheet.get_width() // largura)):
                x = coluna * largura
                y = linha * altura
                sprite = sheet.subsurface(pygame.Rect(x, y, largura, altura))
                sprite = pygame.transform.scale(sprite, (64, 64))  # Redimensiona se necessário
                sprites.append(sprite)
        return sprites

    def modelo_personagem(self, tela):
        now = pygame.time.get_ticks()
        # Só atualiza a animação se o personagem estiver se movendo
        if self.esta_movendo and now - self.last_anim_update > self.anim_speed:
            self.anim_frame = (self.anim_frame + 1) % len(self.animations[self.direction])
            self.last_anim_update = now
        elif not self.esta_movendo:
            self.anim_frame = 0  # Reseta para o primeiro frame (sprite parado)

        sprite = self.animations[self.direction][self.anim_frame]
        # Desenha o sprite com o offset aplicado (se necessário)
        tela.blit(
            sprite,
            (int(self.x - self.sprite_size[0] // 2 + self.sprite_offset_x),
                int(self.y - self.sprite_size[1] // 2 + self.sprite_offset_y))
        )
    def mover(self, teclas, paredes):
        dx = 0
        dy = 0
        if teclas[pygame.K_LEFT]:
            dx = -self.velocidade
            self.direction = "esquerda"
        if teclas[pygame.K_RIGHT]:
            dx = self.velocidade
            self.direction = "direita"
        if teclas[pygame.K_UP]:
            dy = -self.velocidade
            self.direction = "cima"
        if teclas[pygame.K_DOWN]:
            dy = self.velocidade
            self.direction = "baixo"

        # Define se o personagem está se movendo
        self.esta_movendo = dx != 0 or dy != 0

        # Hitbox centralizada no personagem (self.x, self.y)
        hitbox = pygame.Rect(
            self.x - self.raio,  # Centro X - raio
            self.y - self.raio,  # Centro Y - raio
            self.raio * 2,       # Largura = diâmetro
            self.raio * 2        # Altura = diâmetro
        )

        # Testa colisão em X
        hitbox.x += dx
        for parede in paredes:
            if hitbox.colliderect(parede):
                if dx > 0:
                    hitbox.right = parede.left
                elif dx < 0:
                    hitbox.left = parede.right
                dx = 0

        # Testa colisão em Y
        hitbox.y += dy
        for parede in paredes:
            if hitbox.colliderect(parede):
                if dy > 0:
                    hitbox.bottom = parede.top
                elif dy < 0:
                    hitbox.top = parede.bottom
                dy = 0

        # Atualiza a posição central do personagem
        self.x = hitbox.centerx
        self.y = hitbox.centery

    def limitar_bordas(self, largura_tela, altura_tela):
        # Garante que o centro do personagem não saia da tela
        self.x = max(self.raio, min(largura_tela - self.raio, self.x))
        self.y = max(self.raio, min(altura_tela - self.raio, self.y))

    def colidiu_com_parede(self, paredes):
        hitbox = pygame.Rect(
            self.x - self.raio,
            self.y - self.raio,
            self.raio * 2,
            self.raio * 2
        )
        for parede in paredes:
            if hitbox.colliderect(parede):
                return True
        return False