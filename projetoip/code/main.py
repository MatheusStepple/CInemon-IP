import pygame
import sys
import random
import math
import os
from pytmx.util_pygame import load_pygame

# Inicialização
pygame.init()
LARGURA, ALTURA = 1024, 768
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CINEMON IP - A Revolução")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 24)
fonte_grande = pygame.font.SysFont("Arial", 36)

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 128, 0)
AMARELO = (255, 255, 0)
CINZA = (128, 128, 128)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)
MARROM = (139, 69, 19)
AZUL_ESCURO = (50, 50, 100)

# Sistema de Tipos
SISTEMA_DE_TIPOS = {
    "FOGO": {"AGUA": 0.5, "PLANTA": 2.0},
    "AGUA": {"FOGO": 2.0, "ELETRICO": 0.5},
    "PLANTA": {"TERRA": 2.0, "FOGO": 0.5},
    "ELETRICO": {"AGUA": 2.0, "TERRA": 0.5},
    "TERRA": {"ELETRICO": 2.0, "PLANTA": 0.5},
    "ESPECIAL": {"FOGO": 1.5, "ELETRICO": 1.5}
}

class Jogador:
    def __init__(self, x, y, map_width, map_height):
        # Configurações de movimento
        self.x = x
        self.y = y
        self.velocidade = 5
        self.rect = pygame.Rect(x, y, 40, 60)
        self.cor = AZUL
        self.direcao = "baixo"
        self.map_width = map_width
        self.map_height = map_height
        
        # Para o sistema de batalha
        self.cinemons = []
        self.cinemon_atual = None
        
    def mover(self, dx, dy):
        self.x += dx * self.velocidade
        self.y += dy * self.velocidade
        
        # Atualiza a direção
        if dx > 0:
            self.direcao = "direita"
        elif dx < 0:
            self.direcao = "esquerda"
        if dy > 0:
            self.direcao = "baixo"
        elif dy < 0:
            self.direcao = "cima"
            
        # Mantém dentro da tela/mapa
        self.x = max(0, min(self.map_width - 40, self.x))
        self.y = max(0, min(self.map_height - 60, self.y))
        
        self.rect = pygame.Rect(self.x, self.y, 40, 60)
    
    def desenhar(self, tela, camera):
        # Desenha o personagem com offset da câmera
        rect_tela = pygame.Rect(
            self.x - camera.x,
            self.y - camera.y,
            self.rect.width,
            self.rect.height
        )
        
        pygame.draw.rect(tela, self.cor, rect_tela)
        # Desenha cabeça
        pygame.draw.circle(tela, (255, 200, 150), 
                         (self.x - camera.x + 20, self.y - camera.y + 15), 10)
        
        # Desenha olhos baseado na direção
        if self.direcao == "direita":
            pygame.draw.circle(tela, PRETO, (self.x - camera.x + 25, self.y - camera.y + 13), 3)
        elif self.direcao == "esquerda":
            pygame.draw.circle(tela, PRETO, (self.x - camera.x + 15, self.y - camera.y + 13), 3)
        else:
            pygame.draw.circle(tela, PRETO, (self.x - camera.x + 17, self.y - camera.y + 13), 3)
            pygame.draw.circle(tela, PRETO, (self.x - camera.x + 23, self.y - camera.y + 13), 3)

class Inimigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 40, 60)
        self.cor = VERMELHO
        self.cinemons = []
        
    def desenhar(self, tela, camera):
        rect_tela = pygame.Rect(
            self.x - camera.x,
            self.y - camera.y,
            self.rect.width,
            self.rect.height
        )
        
        pygame.draw.rect(tela, self.cor, rect_tela)
        # Desenha cabeça do Pedro
        pygame.draw.circle(tela, (200, 150, 100), 
                         (self.x - camera.x + 20, self.y - camera.y + 15), 10)
        # Desenha óculos
        pygame.draw.rect(tela, PRETO, 
                         (self.x - camera.x + 10, self.y - camera.y + 10, 20, 5), 2)
        pygame.draw.rect(tela, PRETO, 
                         (self.x - camera.x + 5, self.y - camera.y + 10, 5, 5), 2)
        pygame.draw.rect(tela, PRETO, 
                         (self.x - camera.x + 25, self.y - camera.y + 10, 5, 5), 2)

class CInemon:
    def __init__(self, nome, tipo, nivel, hp, ataques):
        self.nome = nome
        self.tipo = tipo
        self.nivel = nivel
        self.hp = hp
        self.hp_max = hp
        self.ataques = ataques
        self.cor = {
            "FOGO": LARANJA,
            "AGUA": AZUL,
            "PLANTA": VERDE,
            "ELETRICO": AMARELO,
            "TERRA": MARROM,
            "ESPECIAL": ROXO
        }.get(tipo, CINZA)

class Jogo:
    def __init__(self):
        # Estados do jogo
        self.estado = "menu"
        self.estado_anterior = None
        
        # Carrega o mapa TMX
        
        # CORRIJA AQUI
        # COLOQUE O CAMINHO ATÉ O BASIC.TMX 
        self.tmx_data = load_pygame(r'C:\Users\PC\Desktop\projetoip\data\basic.tmx')

         # CORRIJA AQUI# CORRIJA AQUI# CORRIJA AQUI# CORRIJA AQUI# CORRIJA AQUI

        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight
       





        # Cria jogador e inimigo
        self.jogador = Jogador(
            x=self.map_width // 2,
            y=self.map_height // 2,
            map_width=self.map_width,
            map_height=self.map_height
        )
        
        # Posiciona o inimigo em um local específico no mapa
        self.pedro = Inimigo(500, 500)
        
        # Configuração da câmera
        self.camera = pygame.Rect(0, 0, LARGURA, ALTURA)
        
        # Sistema de batalha
        self.cinemons_disponiveis = self.criar_cinemons_disponiveis()
        self.cinemons_escolhidos = []
        self.pedro_cinemons = [
            CInemon("Paradoxium", "ESPECIAL", 15, 200, [("Paradoxo Lógico", 30), ("Indução Forte", 40)])
        ]
        self.em_batalha = False
        self.turno_jogador = True
        self.mensagem_atual = ""
        self.fase_batalha = 0  # 0: turno jogador, 1: resultado jogador, 2: turno inimigo, 3: resultado inimigo
        self.acao_selecionada = None
        self.cinemon_jogador_atual = None
        self.cinemon_inimigo_atual = None
        self.dano_calculado = 0
        self.rects_cinemon = []
        self.aguardando_espaco = False
        self.distancia_batalha = 100  # Distância para iniciar batalha
        self.mensagem_dialogo = []
        self.dialogo_atual = 0
        self.batalha_vencida = False  # Controla se o jogador já venceu a batalha
        
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
        # Calcula a distância entre o jogador e o Pedro
        distancia = math.sqrt((self.jogador.x - self.pedro.x)**2 + (self.jogador.y - self.pedro.y)**2)
        
        # Se a distância for menor que o limite, inicia a batalha
        if (distancia < self.distancia_batalha and not self.em_batalha 
                and len(self.jogador.cinemons) > 0 and not self.batalha_vencida):
            self.mensagem_dialogo = [
                "Pedro Manhães: Você ousa se opor à minha revolução?",
                "Pedro Manhães: Prepare-se para enfrentar as consequências!",
                "Pedro Manhães: Vamos resolver isso com uma batalha de CInemons!"
            ]
            self.dialogo_atual = 0
            self.estado_anterior = self.estado
            self.estado = "dialogo"
            self.aguardando_espaco = True

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
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botão esquerdo
                    for i, rect in enumerate(self.rects_cinemon):
                        if rect.collidepoint(evento.pos) and len(self.cinemons_escolhidos) < 3:
                            if i not in self.cinemons_escolhidos:
                                self.cinemons_escolhidos.append(i)
                            else:
                                self.cinemons_escolhidos.remove(i)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and len(self.cinemons_escolhidos) == 3:
                    self.jogador.cinemons = [self.cinemons_disponiveis[i] for i in self.cinemons_escolhidos]
                    self.jogador.cinemon_atual = self.jogador.cinemons[0]
                    self.estado = "mapa"

        tela.fill((240, 240, 240))
        titulo = fonte_grande.render("Escolha 3 CInemons", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))

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

    def iniciar_batalha(self):
        self.em_batalha = True
        self.turno_jogador = True
        self.fase_batalha = 0
        self.cinemon_jogador_atual = self.jogador.cinemon_atual
        self.cinemon_inimigo_atual = self.pedro_cinemons[0]
        self.mensagem_atual = f"Pedro Manhães enviou {self.cinemon_inimigo_atual.nome}!"
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
                    elif self.cinemon_jogador_atual.hp <= 0 and any(c.hp > 0 for c in self.jogador.cinemons):
                        self.estado = "trocar_cinemon"
                    elif self.fase_batalha == 1:  # Depois do ataque do jogador
                        self.fase_batalha = 2  # Vai para turno do inimigo
                        self.turno_jogador = False
                        self.mensagem_atual = f"{self.cinemon_inimigo_atual.nome} está atacando..."
                        pygame.time.delay(1000)  # Pequena pausa antes do inimigo atacar
                        self.executar_ataque_inimigo()
                    elif self.fase_batalha == 3:  # Depois do ataque do inimigo
                        self.fase_batalha = 0  # Volta para o turno do jogador
                        self.turno_jogador = True
                
                # Seleção de ataques apenas durante o turno do jogador
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
            dano, mensagem = self.calcular_dano(
                self.cinemon_jogador_atual,
                self.cinemon_inimigo_atual,
                self.acao_selecionada
            )
            self.cinemon_inimigo_atual.hp -= dano
            self.mensagem_atual = mensagem
            self.acao_selecionada = None
            self.aguardando_espaco = True
            self.fase_batalha = 1  # Mostrando resultado do ataque
            
            if self.cinemon_inimigo_atual.hp <= 0:
                self.mensagem_atual += f"\n{self.cinemon_inimigo_atual.nome} desmaiou!"

    def executar_ataque_inimigo(self):
        dano, mensagem = self.calcular_dano(
            self.cinemon_inimigo_atual,
            self.cinemon_jogador_atual,
            random.randint(0, 1)
        )
        self.cinemon_jogador_atual.hp -= dano
        self.mensagem_atual = mensagem
        self.aguardando_espaco = True
        self.fase_batalha = 3  # Mostrando resultado do ataque inimigo
        
        if self.cinemon_jogador_atual.hp <= 0:
            self.mensagem_atual += f"\n{self.cinemon_jogador_atual.nome} desmaiou!"
            if any(c.hp > 0 for c in self.jogador.cinemons):
                self.mensagem_atual += "\nEscolha outro CInemon!"
            else:
                self.mensagem_atual += "\nVocê perdeu a batalha!"

    def proximo_inimigo(self):
        for cinemon in self.pedro_cinemons:
            if cinemon.hp > 0:
                self.cinemon_inimigo_atual = cinemon
                self.mensagem_atual = f"Pedro enviou {cinemon.nome}!"
                self.fase_batalha = 0
                self.turno_jogador = True
                self.aguardando_espaco = True
                return
        
        self.em_batalha = False
        self.estado = self.estado_anterior or "mapa"
        self.batalha_vencida = True  # Marca que o jogador venceu
        self.mensagem_atual = "Você venceu a batalha!"
        self.aguardando_espaco = True

    def renderizar_batalha(self):
        tela.fill((200, 230, 255))
        
        # Renderizar CInemons
        pygame.draw.rect(tela, AZUL, (50, 50, 400, 200))  # Jogador
        pygame.draw.rect(tela, VERMELHO, (LARGURA - 450, 50, 400, 200))  # Inimigo
        
        # Info do CInemon do jogador
        jogador = self.cinemon_jogador_atual
        nome_jogador = fonte_grande.render(jogador.nome, True, BRANCO)
        hp_jogador = fonte.render(f"HP: {jogador.hp}/{jogador.hp_max}", True, BRANCO)
        tela.blit(nome_jogador, (70, 70))
        tela.blit(hp_jogador, (70, 110))
        
        # Info do CInemon inimigo
        inimigo = self.cinemon_inimigo_atual
        nome_inimigo = fonte_grande.render(inimigo.nome, True, BRANCO)
        hp_inimigo = fonte.render(f"HP: {inimigo.hp}/{inimigo.hp_max}", True, BRANCO)
        tela.blit(nome_inimigo, (LARGURA - 430, 70))
        tela.blit(hp_inimigo, (LARGURA - 430, 110))
        
        # Caixa de mensagem
        pygame.draw.rect(tela, BRANCO, (50, ALTURA - 200, LARGURA - 100, 150))
        pygame.draw.rect(tela, PRETO, (50, ALTURA - 200, LARGURA - 100, 150), 2)
        
        # Renderizar mensagem atual
        linhas = self.mensagem_atual.split('\n')
        for i, linha in enumerate(linhas):
            texto = fonte.render(linha, True, PRETO)
            tela.blit(texto, (70, ALTURA - 180 + i * 30))
        
        # Opções durante o turno do jogador
        if self.fase_batalha == 0 and self.turno_jogador and not self.aguardando_espaco:
            opcoes = fonte.render(f"1. {jogador.ataques[0][0]}  2. {jogador.ataques[1][0]}  3. Trocar", True, PRETO)
            tela.blit(opcoes, (LARGURA//2 - opcoes.get_width()//2, ALTURA - 50))
        
        # Instrução para continuar
        if self.aguardando_espaco:
            instrucao = fonte.render("Pressione ESPAÇO para continuar", True, PRETO)
            tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 50))
        
        # Se for turno do inimigo e não estiver esperando espaço, executa o ataque
        elif self.fase_batalha == 2 and not self.aguardando_espaco:
            self.executar_ataque_inimigo()

    def tela_trocar_cinemon(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1 and len(self.jogador.cinemons) >= 1 and self.jogador.cinemons[0].hp > 0:
                    antigo = self.cinemon_jogador_atual.nome
                    self.cinemon_jogador_atual = self.jogador.cinemons[0]
                    self.jogador.cinemon_atual = self.cinemon_jogador_atual
                    self.mensagem_atual = f"Você trocou {antigo} por {self.cinemon_jogador_atual.nome}!"
                    self.estado = "batalha"
                    self.fase_batalha = 0  # Volta para o turno do jogador (pode atacar)
                    self.turno_jogador = True
                    self.aguardando_espaco = False  # Não precisa pressionar espaço, pode atacar direto
                elif evento.key == pygame.K_2 and len(self.jogador.cinemons) >= 2 and self.jogador.cinemons[1].hp > 0:
                    antigo = self.cinemon_jogador_atual.nome
                    self.cinemon_jogador_atual = self.jogador.cinemons[1]
                    self.jogador.cinemon_atual = self.cinemon_jogador_atual
                    self.mensagem_atual = f"Você trocou {antigo} por {self.cinemon_jogador_atual.nome}!"
                    self.estado = "batalha"
                    self.fase_batalha = 0  # Volta para o turno do jogador
                    self.turno_jogador = True
                    self.aguardando_espaco = False
                elif evento.key == pygame.K_3 and len(self.jogador.cinemons) >= 3 and self.jogador.cinemons[2].hp > 0:
                    antigo = self.cinemon_jogador_atual.nome
                    self.cinemon_jogador_atual = self.jogador.cinemons[2]
                    self.jogador.cinemon_atual = self.cinemon_jogador_atual
                    self.mensagem_atual = f"Você trocou {antigo} por {self.cinemon_jogador_atual.nome}!"
                    self.estado = "batalha"
                    self.fase_batalha = 0  # Volta para o turno do jogador
                    self.turno_jogador = True
                    self.aguardando_espaco = False
                elif evento.key == pygame.K_ESCAPE:
                    self.estado = "batalha"

        tela.fill((200, 200, 255))
        titulo = fonte_grande.render("Escolha um CInemon", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))

        for i, cinemon in enumerate(self.jogador.cinemons):
            y = 150 + i * 120
            pygame.draw.rect(tela, BRANCO if cinemon.hp > 0 else CINZA, (LARGURA//2 - 150, y, 300, 100))
            pygame.draw.rect(tela, PRETO, (LARGURA//2 - 150, y, 300, 100), 2)
            
            nome = fonte.render(f"{i+1}. {cinemon.nome} ({cinemon.tipo})", True, PRETO)
            hp = fonte.render(f"HP: {cinemon.hp}/{cinemon.hp_max}", True, PRETO)
            status = fonte.render("ATIVO" if cinemon.hp > 0 else "DESMAIADO", True, VERMELHO if cinemon.hp <= 0 else VERDE)
            
            tela.blit(nome, (LARGURA//2 - nome.get_width()//2, y + 20))
            tela.blit(hp, (LARGURA//2 - hp.get_width()//2, y + 50))
            tela.blit(status, (LARGURA//2 - status.get_width()//2, y + 80))

        instrucao = fonte.render("Pressione 1-3 para escolher ou ESC para cancelar", True, PRETO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 50))

    def renderizar_dialogo(self):
        tela.fill(AZUL_ESCURO)  # Fundo azul escuro para diálogos
        
        # Caixa de diálogo
        pygame.draw.rect(tela, BRANCO, (50, ALTURA - 200, LARGURA - 100, 150))
        pygame.draw.rect(tela, PRETO, (50, ALTURA - 200, LARGURA - 100, 150), 2)
        
        # Texto do diálogo
        texto = fonte.render(self.mensagem_dialogo[self.dialogo_atual], True, PRETO)
        tela.blit(texto, (70, ALTURA - 180))
        
        # Instrução
        instrucao = fonte.render("Pressione ESPAÇO para continuar", True, PRETO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 50))
        
        # Processar eventos
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
        
        # Movimentação do jogador
        teclas = pygame.key.get_pressed()
        dx, dy = 0, 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy = -1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy = 1
            
        self.jogador.mover(dx, dy)
        self.verificar_colisao()  # Verifica colisão a cada frame
        self._atualizar_camera()
        
        # Desenhar o mapa
        tela.fill((50, 50, 50))  # Cor de fundo padrão
        
        # Desenha as camadas do mapa TMX
        for layer in self.tmx_data.layers:
            if hasattr(layer, 'tiles'):
                for x, y, surf in layer.tiles():
                    tela.blit(
                        surf, 
                        (x * self.tmx_data.tilewidth - self.camera.x, 
                         y * self.tmx_data.tileheight - self.camera.y)
                    )
        
        # Desenha o inimigo (Pedro)
        self.pedro.desenhar(tela, self.camera)
        
        # Desenha o jogador
        self.jogador.desenhar(tela, self.camera)
        
        # Instruções
        instrucao = fonte.render("Use WASD ou setas para mover. ESC para voltar ao menu", True, BRANCO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 30))
        
        # Mostrar CInemon atual
        if self.jogador.cinemon_atual:
            cinemon_info = fonte.render(
                f"CInemon atual: {self.jogador.cinemon_atual.nome} (HP: {self.jogador.cinemon_atual.hp}/{self.jogador.cinemon_atual.hp_max})", 
                True, BRANCO)
            tela.blit(cinemon_info, (10, 10))
        
        # Mostrar mensagem se já tiver vencido
        if self.batalha_vencida:
            mensagem = fonte.render("Você já derrotou Pedro Manhães!", True, VERMELHO)
            tela.blit(mensagem, (LARGURA//2 - mensagem.get_width()//2, 50))

    def _atualizar_camera(self):
        # Centraliza a câmera no jogador
        x = self.jogador.x - LARGURA // 2
        y = self.jogador.y - ALTURA // 2
        
        # Limita a câmera aos limites do mapa
        x = max(0, min(x, self.map_width - LARGURA))
        y = max(0, min(y, self.map_height - ALTURA))
        
        self.camera = pygame.Rect(x, y, LARGURA, ALTURA)

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

if __name__ == "__main__":
    jogo = Jogo()
    jogo.rodar()