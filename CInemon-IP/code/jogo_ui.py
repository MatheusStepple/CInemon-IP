import pygame
import sys
from jogo_base import JogoBase
from batalha_ui import BatalhaUI
from config import (tela, fonte, fonte_grande, relogio, BRANCO, PRETO, VERMELHO, AZUL, VERDE, AMARELO, 
                    CINZA, ROXO, AZUL_ESCURO, LARGURA, ALTURA)

class JogoUI(JogoBase):
    def __init__(self):
        super().__init__()
        self.batalha_ui = BatalhaUI()  # Instância de BatalhaUI para gerenciar batalhas

    def menu_principal(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    self.estado = "escolher_cinemon"
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        tela.fill(VERDE)
        titulo = fonte_grande.render("CINEMON IP - A Revolução", True, BRANCO)
        subtitulo = fonte.render("Contra a Revolução de Pedro Manhães", True, BRANCO)
        instrucao = fonte.render("Pressione ENTER para começar", True, BRANCO)

        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 200))
        tela.blit(subtitulo, (LARGURA//2 - subtitulo.get_width()//2, 300))
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, 400))

    def tela_escolha_cinemon(self):
        tela.fill((240, 240, 240))
        titulo = fonte_grande.render("Escolha 3 CInemons", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    for i, rect in enumerate(self.rects_cinemon):
                        if rect.collidepoint(evento.pos) and len(self.cinemons_escolhidos) < 3:
                            if i not in self.cinemons_escolhidos:
                                self.cinemons_escolhidos.append(i)
                            else:
                                self.cinemons_escolhidos.remove(i)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and len(self.cinemons_escolhidos) == 3:
                    self.jogador_cinemons = [self.cinemons_disponiveis[i] for i in self.cinemons_escolhidos]
                    self.estado = "mapa"
                    self.cinemon_jogador_atual = self.jogador_cinemons[0]

        self.rects_cinemon = []
        for i, cinemon in enumerate(self.cinemons_disponiveis):
            x = 150 + (i % 5) * 180
            y = 150 + (i // 5) * 180
            rect = pygame.Rect(x, y, 150, 150)
            self.rects_cinemon.append(rect)

            cor_fundo = ROXO if i in self.cinemons_escolhidos else BRANCO
            pygame.draw.rect(tela, cor_fundo, rect)
            pygame.draw.rect(tela, PRETO, rect, 2)

            nome = fonte.render(cinemon.nome, True, PRETO)
            tipo = fonte.render(cinemon.tipo, True, cinemon.cor)
            tela.blit(nome, (x + 75 - nome.get_width()//2, y + 20))
            tela.blit(tipo, (x + 75 - tipo.get_width()//2, y + 50))

            status = fonte.render(f"HP: {cinemon.hp} ATQ: {cinemon.ataques[0][1]}", True, PRETO)
            tela.blit(status, (x + 75 - status.get_width()//2, y + 80))

        instrucao = fonte.render(f"Selecionados: {len(self.cinemons_escolhidos)}/3 - ENTER para confirmar", True, PRETO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 50))

    def renderizar_dialogo(self):
        tela.fill(AZUL_ESCURO)
        pygame.draw.rect(tela, BRANCO, (50, ALTURA - 200, LARGURA - 100, 150))
        pygame.draw.rect(tela, PRETO, (50, ALTURA - 200, LARGURA - 100, 150), 2)
        
        texto = fonte.render(self.mensagem_dialogo[self.dialogo_atual], True, PRETO)
        tela.blit(texto, (70, ALTURA - 180))
        
        instrucao = fonte.render("Pressione ESPAÇO para continuar", True, PRETO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 50))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                self.dialogo_atual += 1
                if self.dialogo_atual >= len(self.mensagem_dialogo):
                    self.estado = "batalha"
                    self.iniciar_batalha()

    def mapa(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.estado = "menu"
        
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
            
        self.jogador.mover(dx, dy)
        self.verificar_colisao_barreiras()
        self.verificar_colisao()
        self._atualizar_camera()

        tela.fill((50, 50, 50))
        for layer in self.tmx_data.layers:
            if hasattr(layer, 'tiles'):
                for x, y, surf in layer.tiles():
                    tela.blit(surf, 
                            (x * self.tmx_data.tilewidth - self.camera.x, 
                             y * self.tmx_data.tileheight - self.camera.y))
            if hasattr(layer, 'objects'):
                for obj in layer.objects:
                    if obj.shape == 'rectangle':
                        pygame.draw.rect(tela, obj.color, 
                                        pygame.Rect(obj.x - self.camera.x, obj.y - self.camera.y, 
                                                    obj.width, obj.height))
                        text_surface = fonte.render("Rectangle", True, (255, 255, 255))
                        tela.blit(text_surface, (obj.x - self.camera.x, obj.y - self.camera.y - 20))
                    elif obj.shape == 'ellipse':
                        pygame.draw.ellipse(tela, obj.color, 
                                            pygame.Rect(obj.x - self.camera.x, obj.y - self.camera.y, 
                                                        obj.width, obj.height))
                        text_surface = fonte.render("Ellipse", True, (255, 255, 255))
                        tela.blit(text_surface, (obj.x - self.camera.x, obj.y - self.camera.y - 20))
                    elif obj.shape == 'point':
                        pygame.draw.circle(tela, obj.color, 
                                        (obj.x - self.camera.x, obj.y - self.camera.y), 5)
                        text_surface = fonte.render("Point", True, (255, 255, 255))
                        tela.blit(text_surface, (obj.x - self.camera.x, obj.y - self.camera.y - 20))
                    elif obj.shape == 'image':
                        image = pygame.image.load(obj.image)
                        tela.blit(image, (obj.x - self.camera.x, obj.y - self.camera.y))
                        text_surface = fonte.render("Image", True, (255, 255, 255))
                        tela.blit(text_surface, (obj.x - self.camera.x, obj.y - self.camera.y - 20))

        self.pedro.desenhar(tela, self.camera)
        self.gusto.desenhar(tela, self.camera)
        self.pooh.desenhar(tela, self.camera)
        self.jogador.desenhar(tela, self.camera)
        
        instrucao = fonte.render("Use WASD ou setas para mover. ESC para voltar ao menu", True, BRANCO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 30))
        
        if self.cinemon_jogador_atual:
            cinemon_info = fonte.render(
                f"CInemon atual: {self.cinemon_jogador_atual.nome} (HP: {self.cinemon_jogador_atual.hp}/{self.cinemon_jogador_atual.hp_max})", 
                True, BRANCO)
            tela.blit(cinemon_info, (10, 10))
        
        if self.batalha_vencida_pedro:
            mensagem = fonte.render("Você já derrotou Pedro Manhães!", True, AZUL)
            tela.blit(mensagem, (LARGURA//2 - mensagem.get_width()//2, 50))
            
        if self.batalha_vencida_gusto:
            mensagem = fonte.render("Você já derrotou Gusto!", True, VERDE)
            tela.blit(mensagem, (LARGURA//2 - mensagem.get_width()//2, 90))
            
        if self.batalha_vencida_pooh: 
            mensagem = fonte.render("Você já derrotou pooh!", True, VERMELHO)
            tela.blit(mensagem, (LARGURA//2 - mensagem.get_width()//2, 110))
            
        texto_dinheiro = fonte.render(f'Você tem {self.jogador.dinheiro} creditos', True, AMARELO)
        tela.blit(texto_dinheiro, (10, 40))

    def rodar(self):
        while True:
            if self.estado == "menu":
                self.menu_principal()
            elif self.estado == "escolher_cinemon":
                self.tela_escolha_cinemon()
            elif self.estado == "mapa":
                self.mapa()
            elif self.estado == "batalha":
                self.batalha_ui.processar_batalha(self)
                self.batalha_ui.renderizar_batalha(self)
            elif self.estado == "trocar_cinemon":
                self.batalha_ui.tela_trocar_cinemon(self)
            elif self.estado == "dialogo":
                self.renderizar_dialogo()

            pygame.display.flip()
            relogio.tick(60)