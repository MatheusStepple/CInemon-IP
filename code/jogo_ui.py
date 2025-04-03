import pygame
import sys
import os
import math
import random
from personagem import Personagem
from inimigo import Inimigo
from cinemon import CInemon
from config import (tela, fonte, fonte_grande, relogio, BRANCO, PRETO, VERMELHO, AZUL, VERDE, 
                    AMARELO, CINZA, ROXO, AZUL_ESCURO, LARGURA, ALTURA)
from pytmx.util_pygame import load_pygame

class JogoUI:
    def __init__(self):  # Corrigido de "init" para "__init__"
        self.estado = "menu"
        # Carrega o mapa TMX
        caminho_mapa = os.path.join("Desktop","CInemon-IP", "data", "basic.tmx")  # Caminho relativo corrigido
        try:
            self.tmx_data = load_pygame(caminho_mapa)
            print("Mapa carregado com sucesso:", self.tmx_data.width, "x", self.tmx_data.height)
        except Exception as e:
            print("Erro ao carregar o mapa:", e)
            sys.exit()
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight

        self.jogador = Personagem(self.map_width//2, self.map_height//2, self.map_width, self.map_height)
        self.pedro = Inimigo(self.map_width - 200, 350, 'Pedro')
        self.gusto = Inimigo(700, 500, 'Gusto')
        self.pooh = Inimigo(900, 500, 'pooh')
        self.camera = pygame.Rect(0, 0, LARGURA, ALTURA)
        self.zoom = 1.0  # Adicionado para funcionalidade de zoom
        
        self.inimigo_atual = None
        self.jogador_cinemons = []
        self.cinemons_disponiveis = self.criar_cinemons_disponiveis()
        self.cinemons_escolhidos = []
        self.pedro_cinemons = [
            CInemon("Paradoxium", "ESPECIAL", 15, 20, [("Paradoxo Lógico", 30), ("Indução Forte", 40)])
        ]
        self.gusto_cinemons = [
            CInemon("Discretex", "ESPECIAL", 15, 20, [("Dano Imoral", 30), ("Chama", 40)])
        ]
        self.pooh_cinemons = [
            CInemon("Discretex", "ESPECIAL", 15, 20, [("Dano Imoral", 30), ("Chama", 40)])
        ]
        self.em_batalha = False
        self.turno_jogador = True
        self.mensagem_atual = ""
        self.fase_batalha = 0
        self.acao_selecionada = None
        self.cinemon_jogador_atual = None
        self.cinemon_inimigo_atual = None
        self.rects_cinemon = []
        self.aguardando_espaco = False
        self.distancia_batalha = 100
        self.mensagem_dialogo = []
        self.dialogo_atual = 0
        self.batalha_vencida_pedro = False
        self.batalha_vencida_gusto = False
        self.batalha_vencida_pooh = False
        
        self.camada_colisao = self.tmx_data.get_layer_by_name("colisao")
        self.mapa_colisao = self._criar_mapa_colisao()

    def _criar_mapa_colisao(self):
        mapa_colisao = [[False for _ in range(self.tmx_data.height)] 
                       for _ in range(self.tmx_data.width)]
        if self.camada_colisao:
            for x, y, tile in self.camada_colisao.tiles():
                if tile:
                    mapa_colisao[x][y] = True
        return mapa_colisao

    def verificar_colisao_tile(self, x, y):
        tile_x = int(x // self.tmx_data.tilewidth)
        tile_y = int(y // self.tmx_data.tileheight)
        if 0 <= tile_x < self.tmx_data.width and 0 <= tile_y < self.tmx_data.height:
            return self.mapa_colisao[tile_x][tile_y]
        return True

    def verificar_colisao_personagem(self, rect):
        pontos = [
            (rect.left, rect.top), (rect.right, rect.top),
            (rect.left, rect.bottom), (rect.right, rect.bottom)
        ]
        for px, py in pontos:
            if self.verificar_colisao_tile(px, py):
                return True
        return False

    def criar_cinemons_disponiveis(self):
        return [
            CInemon("Heatbug", "FOGO", 10, 120, [("Bug Flamejante", 25), ("Firewall", 20)]),
            CInemon("Pikacode", "ELETRICO", 10, 110, [("Raio Código", 30), ("Compile Shock", 25)]),
            CInemon("Minerbit", "TERRA", 10, 130, [("Terrabyte", 20), ("Overclock Quake", 35)]),
            CInemon("Hydrabyte", "AGUA", 10, 125, [("Onda de Dados", 25), ("Debbubble", 30)]),
            CInemon("Dataflora", "PLANTA", 10, 115, [("Árvore Binária", 20), ("Trepadeira Viral", 25)]),
            CInemon("Ampereon", "ELETRICO", 10, 105, [("Nanotrovoada", 30), ("Corrente de Dados", 20)]),
            CInemon("Terrabyte", "TERRA", 10, 135, [("Código Sísmico", 35), ("Data Geodo", 25)]),
            CInemon("Debbubble", "AGUA", 10, 120, [("Bubblesorted", 25), ("Maremoto Quântico", 30)]),
            CInemon("Treebit", "PLANTA", 10, 125, [("Cipó Cibernético", 20), ("Sistema de Vinhas", 25)]),
            CInemon("Patchburn", "FOGO", 10, 110, [("Vírus Ígneo", 30), ("Nano Queimadura", 20)])
        ]

    def verificar_colisao(self):
        distancia_pedro = math.sqrt((self.jogador.x - self.pedro.x)**2 + (self.jogador.y - self.pedro.y)**2)
        distancia_gusto = math.sqrt((self.jogador.x - self.gusto.x)**2 + (self.jogador.y - self.gusto.y)**2)
        distancia_pooh = math.sqrt((self.jogador.x - self.pooh.x)**2 + (self.jogador.y - self.pooh.y)**2)
        
        if (distancia_pedro < self.distancia_batalha and not self.em_batalha 
                and len(self.jogador_cinemons) > 0 and not self.batalha_vencida_pedro):
            self.inimigo_atual = 'Pedro'
            self.mensagem_dialogo = [
                "Pedro Manhães: Você ousa se opor à minha revolução?",
                "Pedro Manhães: Prepare-se para enfrentar as consequências!",
                "Pedro Manhães: Vamos resolver isso com uma batalha de CInemons!"
            ]
            self.dialogo_atual = 0
            self.estado = "dialogo"
            self.aguardando_espaco = True
        
        if (distancia_gusto < self.distancia_batalha and not self.em_batalha 
                and len(self.jogador_cinemons) > 0 and not self.batalha_vencida_gusto):
            self.inimigo_atual = 'Gusto'
            self.mensagem_dialogo = [
                "Gusto: Como você ousa falar mal de front end",
                "Gusto: Prepare-se para enfrentar as consequências!",
                "Gusto: Vamos resolver isso com uma batalha de CInemons!"
            ]
            self.dialogo_atual = 0
            self.estado = "dialogo"
            self.aguardando_espaco = True
        
        if (distancia_pooh < self.distancia_batalha and not self.em_batalha 
                and len(self.jogador_cinemons) > 0 and not self.batalha_vencida_pooh):
            self.inimigo_atual = 'pooh'
            self.mensagem_dialogo = [
                "pooh: como você ousa falar mal do meu lol",
                "pooh: Prepare-se para enfrentar as consequências!",
                "pooh: Vamos resolver isso com uma batalha de CInemons!"
            ]
            self.dialogo_atual = 0
            self.estado = "dialogo"
            self.aguardando_espaco = True

    def verificar_colisao_barreiras(self):
        temp_rect = pygame.Rect(self.jogador.x, self.jogador.y, 40, 60)
        if self.verificar_colisao_personagem(temp_rect):
            self.jogador.x = self.jogador.x_anterior
            self.jogador.y = self.jogador.y_anterior
            self.jogador.rect = pygame.Rect(self.jogador.x, self.jogador.y, 40, 60)
            return True
        return False

    def iniciar_batalha(self):
        self.em_batalha = True
        self.turno_jogador = True
        self.fase_batalha = 0
        self.cinemon_jogador_atual = self.jogador_cinemons[0]
        if self.inimigo_atual == 'Pedro':
            self.cinemon_inimigo_atual = self.pedro_cinemons[0]
        elif self.inimigo_atual == 'Gusto':
            self.cinemon_inimigo_atual = self.gusto_cinemons[0]
        elif self.inimigo_atual == 'pooh':
            self.cinemon_inimigo_atual = self.pooh_cinemons[0]
        self.mensagem_atual = f"{self.inimigo_atual} enviou {self.cinemon_inimigo_atual.nome}!"
        self.aguardando_espaco = True

    def calcular_dano(self, atacante, defensor, ataque_idx):
        ataque_nome, dano_base = atacante.ataques[ataque_idx]
        multiplicador = SISTEMA_DE_TIPOS[atacante.tipo].get(defensor.tipo, 1.0)
        dano = int(dano_base * multiplicador)
        
        mensagem = f"{atacante.nome} usou {ataque_nome}!\n"
        if multiplicador > 1:
            mensagem += "Foi SUPER EFETIVO!\n"
        elif multiplicador < 1:
            mensagem += "Não foi muito efetivo...\n"
        else:
            mensagem += "Dano normal.\n"
        mensagem += f"Causou {dano} de dano!"
        
        return dano, mensagem

    def processar_batalha(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and self.aguardando_espaco:
                    self.aguardando_espaco = False
                    if self.cinemon_inimigo_atual.hp <= 0:
                        self.proximo_inimigo()
                    elif self.cinemon_jogador_atual.hp <= 0 and any(c.hp > 0 for c in self.jogador_cinemons):
                        self.estado = "trocar_cinemon"
                    elif self.fase_batalha == 1:
                        self.fase_batalha = 2
                        self.turno_jogador = False
                        self.mensagem_atual = f"{self.cinemon_inimigo_atual.nome} está atacando..."
                        pygame.time.delay(1000)
                        self.executar_ataque_inimigo()
                    elif self.fase_batalha == 3:
                        self.fase_batalha = 0
                        self.turno_jogador = True
                if self.fase_batalha == 0 and self.turno_jogador and not self.aguardando_espaco:
                    if evento.key == pygame.K_1:
                        self.acao_selecionada = 0
                        self.executar_ataque_jogador()
                    elif evento.key == pygame.K_2:
                        self.acao_selecionada = 1
                        self.executar_ataque_jogador()
                    elif evento.key == pygame.K_3:
                        self.estado = "trocar_cinemon"

    def executar_ataque_jogador(self):
        if self.acao_selecionada is not None:
            dano, mensagem = self.calcular_dano(self.cinemon_jogador_atual, self.cinemon_inimigo_atual, self.acao_selecionada)
            self.cinemon_inimigo_atual.hp -= dano
            self.mensagem_atual = mensagem
            self.acao_selecionada = None
            self.aguardando_espaco = True
            self.fase_batalha = 1
            if self.cinemon_inimigo_atual.hp <= 0:
                self.mensagem_atual += f"\n{self.cinemon_inimigo_atual.nome} desmaiou!"

    def executar_ataque_inimigo(self):
        dano, mensagem = self.calcular_dano(self.cinemon_inimigo_atual, self.cinemon_jogador_atual, random.randint(0, 1))
        self.cinemon_jogador_atual.hp -= dano
        self.mensagem_atual = mensagem
        self.aguardando_espaco = True
        self.fase_batalha = 3
        if self.cinemon_jogador_atual.hp <= 0:
            self.mensagem_atual += f"\n{self.cinemon_jogador_atual.nome} desmaiou!"
            if any(c.hp > 0 for c in self.jogador_cinemons):
                self.mensagem_atual += "\nEscolha outro CInemon!"
            else:
                self.mensagem_atual += "\nVocê perdeu a batalha!"

    def proximo_inimigo(self):
        if self.inimigo_atual == 'Pedro':
            inimigos = self.pedro_cinemons
        elif self.inimigo_atual == 'Gusto':
            inimigos = self.gusto_cinemons
        elif self.inimigo_atual == 'pooh':
            inimigos = self.pooh_cinemons

        for cinemon in inimigos:
            if cinemon.hp > 0:
                self.cinemon_inimigo_atual = cinemon
                self.mensagem_atual = f"{self.inimigo_atual} enviou {cinemon.nome}!"
                self.fase_batalha = 0
                self.turno_jogador = True
                self.aguardando_espaco = True
                return
        self.em_batalha = False
        self.estado = "mapa"
        if self.inimigo_atual == 'Pedro':
            self.batalha_vencida_pedro = True
            self.jogador.dinheiro += 100
        elif self.inimigo_atual == 'Gusto':
            self.batalha_vencida_gusto = True
            self.jogador.dinheiro += 100
        elif self.inimigo_atual == 'pooh':
            self.batalha_vencida_pooh = True
            self.jogador.dinheiro += 100
        self.mensagem_atual = "Você venceu a batalha!"
        self.aguardando_espaco = True

    def _atualizar_camera(self):
        x = self.jogador.x - (LARGURA // 2) / self.zoom
        y = self.jogador.y - (ALTURA // 2) / self.zoom
        x = max(0, min(x, self.map_width - LARGURA / self.zoom))
        y = max(0, min(y, self.map_height - ALTURA / self.zoom))
        self.camera.topleft = (x, y)

    def ajustar_zoom(self, incremento):
        self.zoom += incremento
        self.zoom = max(0.5, min(self.zoom, 3.0))  # Aumentado limite para 3.0x
        self._atualizar_camera()

    # Métodos de renderização
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
                elif evento.key == pygame.K_z:  # Mudado para Z para aumentar zoom
                    print(f"Zoom antes: {self.zoom}")
                    self.ajustar_zoom(0.1)
                    print(f"Zoom depois: {self.zoom}")
                elif evento.key == pygame.K_x:  # Mudado para X para diminuir zoom
                    print(f"Zoom antes: {self.zoom}")
                    self.ajustar_zoom(-0.1)
                    print(f"Zoom depois: {self.zoom}")
        
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
        
        instrucao = fonte.render("WASD/Setas: Mover | Z/X: Zoom | ESC: Menu", True, BRANCO)
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

    def rodar(self):
        while True:
            if self.estado == "menu":
                self.menu_principal()
            elif self.estado == "escolher_cinemon":
                self.tela_escolha_cinemon()
            elif self.estado == "mapa":
                self.mapa()
            elif self.estado == "batalha":
                self.processar_batalha()
                self.renderizar_batalha()
            elif self.estado == "trocar_cinemon":
                self.tela_trocar_cinemon()
            elif self.estado == "dialogo":
                self.renderizar_dialogo()

            pygame.display.flip()
            relogio.tick(60)

    # Métodos adicionais para batalha e troca de CInemon
    def renderizar_batalha(self):
        tela.fill(PRETO)
        if self.cinemon_jogador_atual:
            info_jogador = fonte.render(f"{self.cinemon_jogador_atual.nome} HP: {self.cinemon_jogador_atual.hp}/{self.cinemon_jogador_atual.hp_max}", True, BRANCO)
            tela.blit(info_jogador, (50, ALTURA - 100))
        if self.cinemon_inimigo_atual:
            info_inimigo = fonte.render(f"{self.cinemon_inimigo_atual.nome} HP: {self.cinemon_inimigo_atual.hp}/{self.cinemon_inimigo_atual.hp_max}", True, BRANCO)
            tela.blit(info_inimigo, (LARGURA - 300, 50))
        
        mensagem = fonte.render(self.mensagem_atual, True, BRANCO)
        tela.blit(mensagem, (50, ALTURA - 50))
        
        if self.turno_jogador and not self.aguardando_espaco:
            opcoes = fonte.render("1: Ataque 1 | 2: Ataque 2 | 3: Trocar", True, BRANCO)
            tela.blit(opcoes, (50, ALTURA - 150))

    def tela_trocar_cinemon(self):
        tela.fill((240, 240, 240))
        titulo = fonte_grande.render("Trocar CInemon", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                for i, cinemon in enumerate(self.jogador_cinemons):
                    if evento.key == getattr(pygame, f"K_{i+1}") and cinemon.hp > 0:
                        self.cinemon_jogador_atual = cinemon
                        self.estado = "batalha"
                        self.mensagem_atual = f"Você escolheu {cinemon.nome}!"
                        self.aguardando_espaco = True
                        self.fase_batalha = 0
                        self.turno_jogador = True

        for i, cinemon in enumerate(self.jogador_cinemons):
            x = 150 + (i % 3) * 200
            y = 150 + (i // 3) * 150
            pygame.draw.rect(tela, BRANCO, (x, y, 150, 100))
            pygame.draw.rect(tela, PRETO, (x, y, 150, 100), 2)
            nome = fonte.render(f"{i+1}: {cinemon.nome}", True, PRETO)
            hp = fonte.render(f"HP: {cinemon.hp}/{cinemon.hp_max}", True, PRETO)
            tela.blit(nome, (x + 10, y + 20))
            tela.blit(hp, (x + 10, y + 50))

def main():
    jogo = JogoUI()
    jogo.rodar()

if __name__ == "__main__":
    main()