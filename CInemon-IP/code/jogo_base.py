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
from gema import Gema
from npc import NPC  # Importa a nova classe NPC

class JogoBase:
    def __init__(self):
        self.estado = "menu"

        # Define o mapa inicial
        caminho_mapa = os.path.join("Desktop", "CInemon-IP", "data", "basic.tmx")  # Começa com basic.tmx
        self.mapa_atual = "basic.tmx"  # Mapa atual
        self.mapa_anterior = None  # Rastreia o mapa de origem

        # Carrega o mapa TMX com tratamento de erro
        try:
            self.tmx_data = load_pygame(caminho_mapa)
            print("Mapa carregado com sucesso:", self.tmx_data.width, "x", self.tmx_data.height)
        except Exception as e:
            print(f"Erro ao carregar o mapa: {e}")
            sys.exit()

        # Agora que tmx_data está definido, inicialize as camadas
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight
        self.camada_porta = self.tmx_data.get_layer_by_name("porta") if "porta" in [layer.name for layer in self.tmx_data.layers] else None
        self.camada_colisao = self.tmx_data.get_layer_by_name("colisao")
        self.mapa_colisao = self._criar_mapa_colisao()

        
        self.jogador = None
        self.pedro = None
        self.Sergio = None
        self.Fernanda = None
        self.Ricardo = None
        self.npcs = []  
        self.gemas = []
        
        self.definir_posicoes()
        
        self.camera = pygame.Rect(0, 0, LARGURA, ALTURA)
        
        self.inimigo_atual = None
        self.jogador_cinemons = []
        self.cinemons_disponiveis = self.criar_cinemons_disponiveis()
        self.cinemons_escolhidos = []
        self.pedro_cinemons = [
            CInemon("Paradoxium", "ESPECIAL", 5, 20, [("Paradoxo Lógico", 30), ("Indução Forte", 40)])
            
        ]
        self.Sergio_cinemons = [
            CInemon("Redlion", "FOGO", 15, 20, [("Vírus Ígneo", 30), ("Nano Queimadura", 40)]),
            CInemon("Serpython", "FOGO", 15, 20, [("Dano Imoral", 30), ("Chama", 40)]) ##### se liga
        ]
        self.Fernanda_cinemons = [
            CInemon("Butterfault", "PLANTA", 15, 20, [("Dano Imoral", 30), ("Chama", 40)])
        ]
        self.Ricardo_cinemons = [
            CInemon("MinerByte", "TERRA", 15, 20, [("Dano Imoral", 30), ("Chama", 40)])
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
        self.batalha_vencida_Sergio = False
        self.batalha_vencida_Fernanda = False
        self.batalha_vencida_Ricardo = False

        self.pedacos_cracha = 0
        self.cracha_completo = 0
        


        self.camada_colisao = self.tmx_data.get_layer_by_name("colisao")
        self.mapa_colisao = self._criar_mapa_colisao()
        
        self.gemas_coletadas = 0
        self.em_dialogo_npc = False  # Controla o diálogo com o NPC
        self.resposta_npc = None  # Armazena a resposta do jogador ('sim' ou 'nao')

    
    
    def verificar_colisao_porta(self):
        """Verifica se o jogador colidiu com uma porta e troca o mapa se necessário"""
        if not self.camada_porta:
            return False

        # Pega a posição do jogador em tiles
        tile_x = int(self.jogador.x // self.tmx_data.tilewidth)
        tile_y = int(self.jogador.y // self.tmx_data.tileheight)

        # Verifica os tiles ao redor do jogador
        for x, y, tile in self.camada_porta.tiles():
            if tile and tile_x == x and tile_y == y:
                if self.cracha_completo == 1:
                    indice_camada_porta = self.tmx_data.layers.index(self.camada_porta)
                    propriedades = self.tmx_data.get_tile_properties(x, y, indice_camada_porta)
                    if propriedades and propriedades.get("porta", False):
                        destino = propriedades.get("destino", "cin.tmx")  # Mapa destino
                        spawn_x = 450  # Posição de spawn (opcional)
                        spawn_y = 950
                        self.trocar_mapa(destino, spawn_x, spawn_y)
                        return True
        return False
            
        return False
    def trocar_mapa(self, novo_mapa, spawn_x=None, spawn_y=None):
        """Troca o mapa atual para um novo mapa TMX e rastreia o mapa anterior"""
        # Armazena o mapa atual como anterior antes de trocar
        self.mapa_anterior = self.mapa_atual
        caminho_mapa = os.path.join("Desktop", "CInemon-IP", "data", novo_mapa)
        
        try:
            self.tmx_data = load_pygame(caminho_mapa)
            print(f"Mapa trocado para {novo_mapa} com sucesso: {self.tmx_data.width}x{self.tmx_data.height}")
            self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
            self.map_height = self.tmx_data.height * self.tmx_data.tileheight
            self.mapa_atual = novo_mapa

            # Atualiza as camadas
            self.camada_colisao = self.tmx_data.get_layer_by_name("colisao")
            self.mapa_colisao = self._criar_mapa_colisao()
            self.camada_porta = self.tmx_data.get_layer_by_name("porta") if "porta" in [layer.name for layer in self.tmx_data.layers] else None

            # Reposiciona o jogador
            self.jogador.x = spawn_x if spawn_x is not None else self.map_width // 2
            self.jogador.y = spawn_y if spawn_y is not None else self.map_height // 2
            self.jogador.rect.x = self.jogador.x + 8
            self.jogador.rect.y = self.jogador.y + 18

            # Atualiza a câmera
            self._atualizar_camera()

            
            

        except Exception as e:
            print(f"Erro ao trocar o mapa: {e}")
            sys.exit()

    

    
    def verificar_colisao_porta_retorno(self):
        """Verifica se o jogador quer voltar ao mapa anterior"""
        if not self.camada_porta or not self.mapa_anterior:
            return False

        tile_x = int(self.jogador.x // self.tmx_data.tilewidth)
        tile_y = int(self.jogador.y // self.tmx_data.tileheight)

        for x, y, tile in self.camada_porta.tiles():
            if tile and tile_x == x and tile_y == y:
                propriedades = self.tmx_data.get_tile_properties(x, y, self.tmx_data.layers.index(self.camada_porta))
                if propriedades and propriedades.get("porta", False):
                    spawn_x = propriedades.get("spawn_x", self.map_width // 2)
                    spawn_y = propriedades.get("spawn_y", self.map_height // 2)
                    self.trocar_mapa(self.mapa_anterior, spawn_x, spawn_y)
                    print(f"Porta encontrada! Destino: {propriedades.get('destino')}")
                    return True
        return False











    def definir_posicoes(self):
        self.jogador = Personagem(1695, 710, self.map_width, self.map_height)
        self.pedro = Inimigo(450, 140 , 'Pedro')
        self.Ricardo = Inimigo(450, 295, 'Ricardo')
        self.Sergio = Inimigo(1345, 765, 'Sergio')
        self.Fernanda = Inimigo(192, 988, 'Fernanda')
        self.npcs = [
        NPC(770, 900, 'Fernanda1', "spr_enfermeira_joy.png"),
        
    ]
        self.gemas = [
            Gema(400, 520),
            Gema(450, 100),
            Gema(1675, 1045),
            Gema(320, 1230),
        ]

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
        pontos = []
        step = 4
        
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
            CInemon("Firewall", "FOGO", 10, 120, [("Bug Flamejante", 25), ("Firewall", 20)]),
            CInemon("Pikacode", "ELETRICO", 10, 110, [("Raio Código", 30), ("Compile Shock", 25)]),
            CInemon("Terrabyte", "TERRA", 10, 130, [("Terrabyte", 20), ("Overclock Quake", 35)]),
            CInemon("Aqualynx", "AGUA", 10, 125, [("Onda de Dados", 25), ("Debbubble", 30)]),
            CInemon("Grasscat", "PLANTA", 10, 115, [("Árvore Binária", 20), ("Trepadeira Viral", 25)]),
            CInemon("Aetherbyte", "ELETRICO", 10, 105, [("Nanotrovoada", 30), ("Corrente de Dados", 20)]),
            CInemon("Granitex", "TERRA", 10, 135, [("Código Sísmico", 35), ("Data Geodo", 25)]),
            CInemon("Bitwhale", "AGUA", 10, 120, [("Bubblesorted", 25), ("Maremoto Quântico", 30)]),
            CInemon("Leafbyte", "PLANTA", 10, 125, [("Cipó Cibernético", 20), ("Sistema de Vinhas", 25)]),
            CInemon("Emberfang", "FOGO", 10, 110, [("Vírus Ígneo", 30), ("Nano Queimadura", 20)])
        ]

    def verificar_colisao(self):
        distancia_pedro = math.sqrt((self.jogador.x - self.pedro.x)**2 + (self.jogador.y - self.pedro.y)**2)
        distancia_Sergio = math.sqrt((self.jogador.x - self.Sergio.x)**2 + (self.jogador.y - self.Sergio.y)**2)
        distancia_Fernanda = math.sqrt((self.jogador.x - self.Fernanda.x)**2 + (self.jogador.y - self.Fernanda.y)**2)
        distancia_Ricardo = math.sqrt((self.jogador.x - self.Ricardo.x)**2 + (self.jogador.y - self.Ricardo.y)**2)
        if self.mapa_atual == 'cin.tmx':
            if (distancia_pedro < self.distancia_batalha and not self.em_batalha 
                    and len(self.jogador_cinemons) > 0 and not self.batalha_vencida_pedro):
                self.inimigo_atual = 'Pedro'
                #dialogos pedro
                self.mensagem_dialogo = [
                    "Pedro Manhães: Você ousa se opor à minha revolução?",
                    "Pedro Manhães: Prepare-se para enfrentar as consequências!",
                    "Pedro Manhães: Vamos resolver isso com uma batalha de CInemons!"
                ]
                self.dialogo_atual = 0
                self.estado = "dialogo"
                self.aguardando_espaco = True
        if self.mapa_atual == 'basic.tmx':
            if (distancia_Sergio < self.distancia_batalha and not self.em_batalha 
                    and len(self.jogador_cinemons) > 0 and not self.batalha_vencida_Sergio):
                self.inimigo_atual = 'Sergio'
                #dialogos sergio
                self.mensagem_dialogo = [
                    "Sergio: Como você ousa falar mal de front end",
                    "Sergio: Prepare-se para enfrentar as consequências!",
                    "Sergio: Vamos resolver isso com uma batalha de CInemons!"
                ]
                self.dialogo_atual = 0
                self.estado = "dialogo"
                self.aguardando_espaco = True
            
            if (distancia_Fernanda < self.distancia_batalha and not self.em_batalha 
                    and len(self.jogador_cinemons) > 0 and not self.batalha_vencida_Fernanda):
                self.inimigo_atual = 'Fernanda'
                #dialogos Fernanda
                self.mensagem_dialogo = [
                    "Fernanda: como você ousa falar mal do meu lol",
                    "Fernanda: Prepare-se para enfrentar as consequências!",
                    "Fernanda: Vamos resolver isso com uma batalha de CInemons!"
                ]
                self.dialogo_atual = 0
                self.estado = "dialogo"
                self.aguardando_espaco = True
            if (distancia_Ricardo < self.distancia_batalha and not self.em_batalha 
                    and len(self.jogador_cinemons) > 0 and not self.batalha_vencida_Ricardo):
                self.inimigo_atual = 'Ricardo'
                #dialogos Ricardo
                self.mensagem_dialogo = [
                    "ricardo: como você ousa falar mal do meu cin",
                    "ricardo: Prepare-se para enfrentar as consequências!",
                    "ricardo: Vamos resolver isso com uma batalha de CInemons!"
                ]
                self.dialogo_atual = 0
                self.estado = "dialogo"
                self.aguardando_espaco = True

    def verificar_colisao_barreiras(self):
        temp_x, temp_y = self.jogador.x, self.jogador.y
        
        if (self.jogador.x != self.jogador.x_anterior or 
            self.jogador.y != self.jogador.y_anterior):
            
            if self.verificar_colisao_personagem(self.jogador.rect):
                self.jogador.x = self.jogador.x_anterior
                self.jogador.y = self.jogador.y_anterior
                self.jogador.rect.x = self.jogador.x + 8
                self.jogador.rect.y = self.jogador.y + 18
                return True
    
        return False

    def verificar_coleta_gemas(self):
        for gema in self.gemas:
            if not gema.collected and self.jogador.rect.colliderect(gema.rect):
                gema.collected = True
                self.gemas_coletadas += 1
                print(f"Gema coletada! Total: {self.gemas_coletadas}")

    def verificar_interacao_npc(self):
        distancia_fernanda = math.sqrt((self.jogador.x - self.fernanda.x)**2 + (self.jogador.y - self.fernanda.y)**2)
        if self.mapa_atual == 'basic.tmx':
            if distancia_fernanda < 50:  # Distância para interação
                return True
        return False

    def processar_dialogo_npc(self):
        if self.jogador.dinheiro >= 50:
            self.mensagem_dialogo = [
                "Fernanda: Quer gastar 50 créditos para reanimar e curar seus CInemons?",
                "Pressione S para Sim ou N para Não"
            ]
        else:
            self.mensagem_dialogo = [
                "Fernanda: Você não tem créditos suficientes!",
                "Volte quando tiver pelo menos 50 créditos."
            ]
        self.em_dialogo_npc = True
        self.dialogo_atual = 0
        self.resposta_npc = None

    def responder_dialogo_npc(self, resposta):
        if resposta == 'sim' and self.jogador.dinheiro >= 50:
            self.jogador.dinheiro -= 50
            for cinemon in self.jogador_cinemons:
                cinemon.hp = cinemon.hp_max  # Cura total
            self.mensagem_dialogo = ["Fernanda: Seus CInemons estão como novos!"]
            self.dialogo_atual = 0
        elif resposta == 'nao':
            self.mensagem_dialogo = ["Fernanda: Tudo bem, volte quando precisar!"]
            self.dialogo_atual = 0
        self.resposta_npc = None

    def iniciar_batalha(self):
        self.em_batalha = True
        self.turno_jogador = True
        self.fase_batalha = 0
        self.cinemon_jogador_atual = self.jogador_cinemons[0]
        if self.inimigo_atual == 'Pedro':
            self.cinemon_inimigo_atual = self.pedro_cinemons[0]
        elif self.inimigo_atual == 'Sergio':
            self.cinemon_inimigo_atual = self.Sergio_cinemons[0]
        elif self.inimigo_atual == 'Fernanda':
            self.cinemon_inimigo_atual = self.Fernanda_cinemons[0]
        elif self.inimigo_atual == 'Ricardo':
            self.cinemon_inimigo_atual = self.Fernanda_cinemons[0]
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
            self.cinemon_inimigo_atual.hp = max(0, self.cinemon_inimigo_atual.hp - dano)  # Limita HP a 0
            self.mensagem_atual = mensagem
            self.acao_selecionada = None
            self.aguardando_espaco = True
            self.fase_batalha = 1
            if self.cinemon_inimigo_atual.hp <= 0:
                self.mensagem_atual += f"\n{self.cinemon_inimigo_atual.nome} desmaiou!"

    def executar_ataque_inimigo(self):
        dano, mensagem = self.calcular_dano(self.cinemon_inimigo_atual, self.cinemon_jogador_atual, random.randint(0, 1))
        self.cinemon_jogador_atual.hp = max(0, self.cinemon_jogador_atual.hp - dano)  # Limita HP a 0
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
        elif self.inimigo_atual == 'Sergio':
            inimigos = self.Sergio_cinemons
        elif self.inimigo_atual == 'Fernanda':
            inimigos = self.Fernanda_cinemons
        elif self.inimigo_atual == 'Ricardo':
            inimigos = self.Ricardo_cinemons
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
        elif self.inimigo_atual == 'Sergio':
            self.batalha_vencida_Sergio = True
            self.jogador.dinheiro += 100
        elif self.inimigo_atual == 'Fernanda':
            self.batalha_vencida_Fernanda = True
            self.jogador.dinheiro += 100
        elif self.inimigo_atual == 'Ricardo':
            self.batalha_vencida_Ricardo = True
            self.jogador.dinheiro += 100
        self.mensagem_atual = "Você venceu a batalha!"
        self.aguardando_espaco = True

        if self.inimigo_atual == 'Pedro':
            self.batalha_vencida_pedro = True
            self.jogador.dinheiro += 100
            if self.cracha_completo == 0:
                self.pedacos_cracha += 1

        elif self.inimigo_atual == 'Sergio':
            self.batalha_vencida_Sergio = True
            self.jogador.dinheiro += 100
            if self.cracha_completo == 0:
                self.pedacos_cracha += 1

        elif self.inimigo_atual == 'Fernanda':
            self.batalha_vencida_Fernanda = True
            self.jogador.dinheiro += 100
            if self.cracha_completo == 0:
                self.pedacos_cracha += 1
        elif self.inimigo_atual == 'Ricardo':
            self.batalha_vencida_Ricardo = True
            self.jogador.dinheiro += 100
            if self.cracha_completo == 0:
                self.pedacos_cracha += 1
                
        if self.cracha_completo == 0:
            if self.pedacos_cracha >= 3:
                self.cracha_completo = 1
                self.pedacos_cracha = 0
                self.mensagem_atual = "Você venceu a batalha e formou o Crachá Completo!"
            else:
                self.mensagem_atual = f"Você venceu a batalha e ganhou um pedaço de crachá! ({self.pedacos_cracha}/3)"
        else:
            self.mensagem_atual = "Você venceu a batalha!"

        self.aguardando_espaco = True
        

    def _atualizar_camera(self):
        x = self.jogador.x - LARGURA // 2
        y = self.jogador.y - ALTURA // 2
        x = max(0, min(x, self.map_width - LARGURA))
        y = max(0, min(y, self.map_height - ALTURA))
        self.camera = pygame.Rect(x, y, LARGURA, ALTURA)