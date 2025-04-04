import pygame
import sys
import os
import math
import random
from jogo_base import JogoBase
from batalha_ui import BatalhaUI
from personagem import Personagem
from inimigo import Inimigo
from cinemon import CInemon
from config import (tela, fonte, fonte_grande, relogio, BRANCO, PRETO, VERMELHO, AZUL, VERDE, 
                    AMARELO, CINZA, ROXO, AZUL_ESCURO, LARGURA, ALTURA, SISTEMA_DE_TIPOS)
from pytmx.util_pygame import load_pygame

class JogoUI(JogoBase):
    def __init__(self):
        super().__init__()
        self.batalha_ui = BatalhaUI()
        self.zoom = 1.9
        self.mostrar_status = False
        self.mostrar_mensagem_gemas = False
        self.tempo_mensagem_gemas = 0

    def _atualizar_camera(self):
        x = self.jogador.x - (LARGURA // 2) / self.zoom
        y = self.jogador.y - (ALTURA // 2) / self.zoom
        x = max(0, min(x, self.map_width - LARGURA / self.zoom))
        y = max(0, min(y, self.map_height - ALTURA / self.zoom))
        self.camera.topleft = (x, y)

    def ajustar_zoom(self, incremento):
        self.zoom += incremento
        self.zoom = max(0.5, min(self.zoom, 3.0))
        self._atualizar_camera()

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

    def renderizar_dialogo_npc(self):
        tela.fill(AZUL_ESCURO)
        pygame.draw.rect(tela, BRANCO, (50, ALTURA - 200, LARGURA - 100, 150))
        pygame.draw.rect(tela, PRETO, (50, ALTURA - 200, LARGURA - 100, 150), 2)
        
        texto = fonte.render(self.mensagem_dialogo[self.dialogo_atual], True, PRETO)
        tela.blit(texto, (70, ALTURA - 180))
        
        if self.dialogo_atual == 1 and self.jogador.dinheiro >= 50:
            instrucao = fonte.render("S para Sim | N para Não", True, PRETO)
        else:
            instrucao = fonte.render("Pressione ESPAÇO para continuar", True, PRETO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 50))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if self.dialogo_atual < len(self.mensagem_dialogo) - 1:
                        self.dialogo_atual += 1
                    else:
                        self.em_dialogo_npc = False
                        self.estado = "mapa"
                elif self.dialogo_atual == 1 and self.jogador.dinheiro >= 50:
                    if evento.key == pygame.K_s:
                        self.responder_dialogo_npc('sim')
                    elif evento.key == pygame.K_n:
                        self.responder_dialogo_npc('nao')

    def mostrar_status_cinemons(self):
        tela.fill(AZUL_ESCURO)
        pygame.draw.rect(tela, BRANCO, (50, 50, LARGURA - 100, ALTURA - 100))
        pygame.draw.rect(tela, PRETO, (50, 50, LARGURA - 100, ALTURA - 100), 2)

        titulo = fonte_grande.render("Seus CInemons", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 70))

        for i, cinemon in enumerate(self.jogador_cinemons):
            y_pos = 150 + i * 100
            nome = fonte.render(f"Nome: {cinemon.nome}", True, PRETO)
            hp = fonte.render(f"HP: {cinemon.hp}/{cinemon.hp_max}", True, PRETO if cinemon.hp > 0 else VERMELHO)
            status = fonte.render("Vivo" if cinemon.hp > 0 else "Morto", True, VERDE if cinemon.hp > 0 else VERMELHO)
            
            tela.blit(nome, (100, y_pos))
            tela.blit(hp, (100, y_pos + 30))
            tela.blit(status, (100, y_pos + 60))

        instrucao = fonte.render("Pressione ESC para voltar ao mapa", True, PRETO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 70))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.mostrar_status = False

    def verificar_coleta_gemas(self):
        for gema in self.gemas:
            if not gema.collected and self.jogador.rect.colliderect(gema.rect):
                gema.collected = True
                self.gemas_coletadas += 1
                print(f"Gema coletada! Total: {self.gemas_coletadas}")
                
                if self.gemas_coletadas == 4:
                    for cinemon in self.jogador_cinemons:
                        cinemon.hp_max += 20
                        cinemon.hp = cinemon.hp_max
                    self.mostrar_mensagem_gemas = True
                    self.tempo_mensagem_gemas = 180

    def mapa(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.mostrar_status = not self.mostrar_status
                elif evento.key == pygame.K_z:
                    print(f"Zoom antes: {self.zoom}")
                    self.ajustar_zoom(0.1)
                    print(f"Zoom depois: {self.zoom}")
                elif evento.key == pygame.K_x:
                    print(f"Zoom antes: {self.zoom}")
                    self.ajustar_zoom(-0.1)
                    print(f"Zoom depois: {self.zoom}")
                elif evento.key == pygame.K_SPACE and self.verificar_interacao_npc():
                    self.estado = "dialogo_npc"
                    self.processar_dialogo_npc()
        
        if self.mostrar_status:
            self.mostrar_status_cinemons()
            return

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
        self.verificar_coleta_gemas()
        self._atualizar_camera()

        tela.fill((0, 0, 0))
        mapa_surface = pygame.Surface((self.map_width, self.map_height))
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles'):
                for x, y, surf in layer.tiles():
                    if surf:
                        mapa_surface.blit(surf, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))
        
        scaled_width = int(self.map_width * self.zoom)
        scaled_height = int(self.map_height * self.zoom)
        mapa_scaled = pygame.transform.scale(mapa_surface, (scaled_width, scaled_height))
        camera_x = int(self.camera.x * self.zoom)
        camera_y = int(self.camera.y * self.zoom)
        tela.blit(mapa_scaled, (0, 0), (camera_x, camera_y, LARGURA, ALTURA))

        self.jogador.desenhar(tela, self.camera, self.zoom)
        self.pedro.desenhar(tela, self.camera, self.zoom)
        self.gusto.desenhar(tela, self.camera, self.zoom)
        self.pooh.desenhar(tela, self.camera, self.zoom)
        self.fernanda.desenhar(tela, self.camera, self.zoom)  # Desenha o NPC
        
        for gema in self.gemas:
            gema.desenhar(tela, self.camera, self.zoom)

        instrucao = fonte.render("WASD/Setas: Mover | ESC: Status | ESPAÇO: Falar com NPC", True, BRANCO)
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
            
        texto_dinheiro = fonte.render(f'Você tem {self.jogador.dinheiro} créditos', True, AMARELO)
        tela.blit(texto_dinheiro, (10, 40))
        
        texto_gemas = fonte.render(f"Gemas: {self.gemas_coletadas}", True, AMARELO)
        tela.blit(texto_gemas, (10, 70))

        if self.gemas_coletadas >= 4 and self.mostrar_mensagem_gemas:
            mensagem = fonte_grande.render("Parabéns! Você pegou as 4 gemas!", True, VERDE)
            mensagem2 = fonte.render("Seus CInemons ganharam 20 de HP máximo!", True, VERDE)
            tela.blit(mensagem, (LARGURA//2 - mensagem.get_width()//2, ALTURA//2 - 50))
            tela.blit(mensagem2, (LARGURA//2 - mensagem2.get_width()//2, ALTURA//2 + 10))
            self.tempo_mensagem_gemas -= 1
            if self.tempo_mensagem_gemas <= 0:
                self.mostrar_mensagem_gemas = False

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
            elif self.estado == "dialogo_npc":
                self.renderizar_dialogo_npc()

            pygame.display.flip()
            relogio.tick(60)

def main():
    jogo = JogoUI()
    jogo.rodar()

if __name__ == "__main__":
    main()