import pygame
import sys
import random
import math

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

class Personagem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 5
        self.rect = pygame.Rect(x, y, 40, 60)
        self.cor = AZUL
        self.direcao = "baixo"
        
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
            
        # Mantém dentro da tela
        self.x = max(0, min(LARGURA - 40, self.x))
        self.y = max(0, min(ALTURA - 60, self.y))
        
        self.rect = pygame.Rect(self.x, self.y, 40, 60)
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)
        # Desenha cabeça
        pygame.draw.circle(tela, (255, 200, 150), (self.x + 20, self.y + 15), 10)
        
        # Desenha olhos baseado na direção
        if self.direcao == "direita":
            pygame.draw.circle(tela, PRETO, (self.x + 25, self.y + 13), 3)
        elif self.direcao == "esquerda":
            pygame.draw.circle(tela, PRETO, (self.x + 15, self.y + 13), 3)
        else:
            pygame.draw.circle(tela, PRETO, (self.x + 17, self.y + 13), 3)
            pygame.draw.circle(tela, PRETO, (self.x + 23, self.y + 13), 3)

class Inimigo:
    def __init__(self, x, y,nome):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 40, 60)
        self.cor = VERMELHO if nome == 'Pedro' else LARANJA
        
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)
        # Desenha cabeça do Pedro
        pygame.draw.circle(tela, (200, 150, 100), (self.x + 20, self.y + 15), 10)
        # Desenha óculos
        pygame.draw.rect(tela, PRETO, (self.x + 10, self.y + 10, 20, 5), 2)
        pygame.draw.rect(tela, PRETO, (self.x + 5, self.y + 10, 5, 5), 2)
        pygame.draw.rect(tela, PRETO, (self.x + 25, self.y + 10, 5, 5), 2)

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
        self.estado = "menu"
        self.jogador = Personagem(LARGURA//2, ALTURA//2)
        self.pedro = Inimigo(LARGURA//4, ALTURA//4, 'Pedro')
        self.gusto = Inimigo(LARGURA//2 + 100 , ALTURA//4, 'Gusto')
        self.inimigo_atual = None
        self.jogador_cinemons = []
        self.cinemons_disponiveis = self.criar_cinemons_disponiveis()
        self.cinemons_escolhidos = []
        self.pedro_cinemons = [
            CInemon("Paradoxium", "ESPECIAL", 15, 200, [("Paradoxo Lógico", 30), ("Indução Forte", 40)])
        ]
        self.gusto_cinemons = [
            CInemon("discretex", "ESPECIAL", 15, 200, [("dano imoral", 30), ("chama", 40)])]
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
        self.fundo_mapa = pygame.Surface((LARGURA, ALTURA))
        self.fundo_mapa.fill((100, 200, 100))  # Cor verde para o mapa
        self.distancia_batalha = 100  # Distância para iniciar batalha
        self.mensagem_dialogo = []
        self.dialogo_atual = 0
        self.batalha_vencida = False  # Controla se o jogador já venceu a batalha
        self.batalha_vencida_gusto = False
        self.batalha_vencida_pedro = False
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
        distancia_pedro = math.sqrt((self.jogador.x - self.pedro.x)**2 + (self.jogador.y - self.pedro.y)**2)
        distancia_gusto = math.sqrt((self.jogador.x - self.gusto.x)**2 + (self.jogador.y - self.gusto.y)**2)
        # Se a distância for menor que 100 pixels, não estiver já em batalha e não tiver vencido ainda
        if (distancia_pedro < self.distancia_batalha and not self.em_batalha 
                and len(self.jogador_cinemons) > 0 and not self.batalha_vencida_pedro):
            self.inimigo_atual = 'Pedro' # define pedro como inimigo
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
            self.inimigo_atual = 'Gusto' # define gusto como inimigo
            self.mensagem_dialogo = [
                "gusto: Como você ousa falar mal de front end",
                "gusto : Prepare-se para enfrentar as consequências!",
                "gusto : Vamos resolver isso com uma batalha de CInemons!"
            ]
            self.dialogo_atual = 0
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
                    self.jogador_cinemons = [self.cinemons_disponiveis[i] for i in self.cinemons_escolhidos]
                    self.estado = "mapa"
                    self.cinemon_jogador_atual = self.jogador_cinemons[0]

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
        if self.inimigo_atual == 'Pedro':
            self.cinemon_inimigo_atual = self.pedro_cinemons[0]
        elif self.inimigo_atual == 'Gusto':
            self.cinemon_inimigo_atual = self.gusto_cinemons[0]
        self.cinemon_jogador_atual = self.jogador_cinemons[0]
        
    
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
            if any(c.hp > 0 for c in self.jogador_cinemons):
                self.mensagem_atual += "\nEscolha outro CInemon!"
            else:
                self.mensagem_atual += "\nVocê perdeu a batalha!"

    def proximo_inimigo(self):
        if self.inimigo_atual == 'Pedro':
            inimigos = self.pedro_cinemons
        elif self.inimigo_atual == 'Gusto':
            inimigos = self.gusto_cinemons

        
        for cinemon in inimigos:
            if cinemon.hp > 0:
                self.cinemon_inimigo_atual = cinemon
                self.mensagem_atual = f"Pedro enviou {cinemon.nome}!"
                self.fase_batalha = 0
                self.turno_jogador = True
                self.aguardando_espaco = True
                return
        
        self.em_batalha = False
        self.estado = "mapa"
        if self.inimigo_atual == 'Pedro':
            self.batalha_vencida_pedro = True  # Marca que o jogador venceu pedro
            
        if self.inimigo_atual == 'Gusto':
            self.batalha_vencida_gusto = True  # Marca que o jogador venceu gusto
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
                if evento.key == pygame.K_1 and len(self.jogador_cinemons) >= 1 and self.jogador_cinemons[0].hp > 0:
                    antigo = self.cinemon_jogador_atual.nome
                    self.cinemon_jogador_atual = self.jogador_cinemons[0]
                    self.mensagem_atual = f"Você trocou {antigo} por {self.cinemon_jogador_atual.nome}!"
                    self.estado = "batalha"
                    self.fase_batalha = 0  # Volta para o turno do jogador (pode atacar)
                    self.turno_jogador = True
                    self.aguardando_espaco = False  # Não precisa pressionar espaço, pode atacar direto
                elif evento.key == pygame.K_2 and len(self.jogador_cinemons) >= 2 and self.jogador_cinemons[1].hp > 0:
                    antigo = self.cinemon_jogador_atual.nome
                    self.cinemon_jogador_atual = self.jogador_cinemons[1]
                    self.mensagem_atual = f"Você trocou {antigo} por {self.cinemon_jogador_atual.nome}!"
                    self.estado = "batalha"
                    self.fase_batalha = 0  # Volta para o turno do jogador
                    self.turno_jogador = True
                    self.aguardando_espaco = False
                elif evento.key == pygame.K_3 and len(self.jogador_cinemons) >= 3 and self.jogador_cinemons[2].hp > 0:
                    antigo = self.cinemon_jogador_atual.nome
                    self.cinemon_jogador_atual = self.jogador_cinemons[2]
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

        for i, cinemon in enumerate(self.jogador_cinemons):
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
        self.verificar_colisao()  # Verifica colisão a cada frame
        
        # Desenhar o mapa
        tela.blit(self.fundo_mapa, (0, 0))
        
        # Desenhar personagens
        self.pedro.desenhar(tela)
        self.jogador.desenhar(tela)
        self.gusto.desenhar(tela)
        # Instruções
        instrucao = fonte.render("Use WASD ou setas para mover. ESC para voltar ao menu", True, PRETO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 30))
        
        # Mostrar CInemon atual
        if self.cinemon_jogador_atual:
            cinemon_info = fonte.render(f"CInemon atual: {self.cinemon_jogador_atual.nome} (HP: {self.cinemon_jogador_atual.hp}/{self.cinemon_jogador_atual.hp_max})", True, PRETO)
            tela.blit(cinemon_info, (10, 10))
        
        # Mostrar mensagem se já tiver vencido
        if self.batalha_vencida_pedro:
            mensagem = fonte.render("Você já derrotou Pedro Manhães!", True, VERMELHO)
            tela.blit(mensagem, (LARGURA//2 - mensagem.get_width()//2, 50))
        if self.batalha_vencida_gusto:
            mensagem = fonte.render("Você já derrotou gusto!", True, VERMELHO)
            tela.blit(mensagem, (LARGURA//2 - mensagem.get_width()//2, 50))


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