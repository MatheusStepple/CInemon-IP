import pygame
import sys
import os
import math
import random
from personagem import Personagem
from inimigo import Inimigo
from cinemon import CInemon
from config import LARGURA, ALTURA, SISTEMA_DE_TIPOS
from pytmx.util_pygame import load_pygame

class JogoBase:
    def __init__(self):
        self.estado = "menu"
        # Carrega o mapa TMX com tratamento de erro
        caminho_mapa = os.path.join("Desktop", "CInemon-IP", "data", "basic.tmx")
        try:
            self.tmx_data = load_pygame(caminho_mapa)
            print("Mapa carregado com sucesso:", self.tmx_data.width, "x", self.tmx_data.height)
        except Exception as e:
            print(f"Erro ao carregar o mapa: {e}")
            sys.exit()
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight
        
        self.jogador = Personagem(self.map_width//2, self.map_height//2, self.map_width, self.map_height)
        self.pedro = Inimigo(self.map_width - 200, 350, 'Pedro')
        self.gusto = Inimigo(700, 500, 'Gusto')
        self.pooh = Inimigo(900, 500, 'pooh')
        self.camera = pygame.Rect(0, 0, LARGURA, ALTURA)
        
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
        """Verifica colisão em uma posição específica do mundo"""
        tile_x = int(x // self.tmx_data.tilewidth)
        tile_y = int(y // self.tmx_data.tileheight)
        
        if 0 <= tile_x < self.tmx_data.width and 0 <= tile_y < self.tmx_data.height:
            return self.mapa_colisao[tile_x][tile_y]
        return True  # Considera fora do mapa como colisão

    def verificar_colisao_personagem(self, rect):
        """Verifica colisão para um retângulo do personagem"""
        # Verifica os pontos ao redor do hitbox, não apenas os cantos
        pontos = []
        step = 4  # Verifica a cada 4 pixels para melhor precisão
        
        # Pontos ao longo das bordas
        for x in range(rect.left, rect.right, step):
            pontos.append((x, rect.top))
            pontos.append((x, rect.bottom))
        
        for y in range(rect.top, rect.bottom, step):
            pontos.append((rect.left, y))
            pontos.append((rect.right, y))
        
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
        # Primeiro guarda a posição atual
        temp_x, temp_y = self.jogador.x, self.jogador.y
        
        # Verifica colisão apenas se o personagem está se movendo
        if (self.jogador.x != self.jogador.x_anterior or 
            self.jogador.y != self.jogador.y_anterior):
            
            if self.verificar_colisao_personagem(self.jogador.rect):
                # Colisão detectada - volta para posição anterior
                self.jogador.x = self.jogador.x_anterior
                self.jogador.y = self.jogador.y_anterior
                self.jogador.rect.x = self.jogador.x + 8
                self.jogador.rect.y = self.jogador.y + 18
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
        x = self.jogador.x - LARGURA // 2
        y = self.jogador.y - ALTURA // 2
        x = max(0, min(x, self.map_width - LARGURA))
        y = max(0, min(y, self.map_height - ALTURA))
        self.camera = pygame.Rect(x, y, LARGURA, ALTURA)