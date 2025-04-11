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
        self.npc_atual = None  # Adicionado para rastrear o NPC atual em interação
        self.estado = "menu"  # Define o estado inicial como diálogo inicial
        self.dialogo_atual = 0
        self.sprites_cache = {}  # Cache para sprites

        # Carregar joy.png
        caminho_joy = os.path.join("Desktop", "CInemon-IP", "graphics", "fotos", "joy.png")
        try:
            self.joy_image = pygame.image.load(caminho_joy)
            self.joy_image = pygame.transform.smoothscale(self.joy_image, (LARGURA, ALTURA))
        except pygame.error as e:
            print(f"Erro ao carregar joy.png: {e}")
            self.joy_image = pygame.Surface((LARGURA, ALTURA))

    def renderizar_dialogo_inicial(self):
        self.mensagem_dialogo = [
            ['Olá, treinador! Eu sou Filipe Milk, estudante do CIn e líder da resistência contra Pedro Noites.'],
            ['Ele quer impor sua grade curricular maligna, mas nós temos um plano: os CInemons!'],
            ['Criados a partir de amostras roubadas do laboratório secreto de Pedro, essas criaturas digitais são nossa', 'única esperança.'],
            ['Sua missão? Reunir os fragmentos do Crachá Perdido do CIn, derrotando os capangas de Pedro que estão', 'espalhados pelo campus.'],
            ['Cuidado: após cada batalha, visite o Centro de Cura para recuperar seus CInemons.'],
            ['Quando o Crachá estiver completo, vá até a Balsa do CIn e enfrente Pedro Noites em uma batalha épica!'],
            ['O futuro do curso está em suas mãos. Você está preparado?'],
            ['Uma dica: há gemas espalhadas pelo mapa... dizem que juntando todas seus CInemons ficam mais fortes!']
        ]

        caminho_imagem_fundo = os.path.join("Desktop", "CInemon-IP", "graphics", 'fotos', "fundo.png")
        self.imagem_fundo = pygame.image.load(caminho_imagem_fundo)
        imagem_fundo_scaled = pygame.transform.smoothscale(self.imagem_fundo, (LARGURA, ALTURA))

        caminho_imagem = os.path.join("Desktop", "CInemon-IP", "graphics", 'fotos', "milk.png")
        self.imagem = pygame.image.load(caminho_imagem)
        imagem_scaled = pygame.transform.smoothscale(self.imagem, (400, 300))

        tela.blit(imagem_fundo_scaled, (0, 0))
        pygame.draw.rect(tela, BRANCO, (50, ALTURA - 200, LARGURA - 100, 150))
        pygame.draw.rect(tela, PRETO, (50, ALTURA - 200, LARGURA - 100, 150), 2)
        tela.blit(imagem_scaled, (750, 220))

        if len(self.mensagem_dialogo[self.dialogo_atual]) > 1:
            texto = fonte.render(self.mensagem_dialogo[self.dialogo_atual][0], True, PRETO)
            texto2 = fonte.render(self.mensagem_dialogo[self.dialogo_atual][1], True, PRETO)
            tela.blit(texto, (70, ALTURA - 180))
            tela.blit(texto2, (70, ALTURA - 150))
            self.estado = 'dialogo_inicial'
            instrucao = fonte.render("Pressione ESPAÇO para continuar", True, PRETO)
            tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 100))
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        if self.dialogo_atual < len(self.mensagem_dialogo) - 1:
                            self.dialogo_atual += 1
                        else:
                            self.estado = "escolher_cinemon"  
                            self.dialogo_atual = 0  
        else:    
            texto = fonte.render(self.mensagem_dialogo[self.dialogo_atual][0], True, PRETO)
            tela.blit(texto, (70, ALTURA - 180))
            self.estado = 'dialogo_inicial'
            instrucao = fonte.render("Pressione ESPAÇO para continuar", True, PRETO)
            tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 100))
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        if self.dialogo_atual < len(self.mensagem_dialogo) - 1:
                            self.dialogo_atual += 1
                        else:
                            self.estado = "escolher_cinemon"  
                            self.dialogo_atual = 0  

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
                    self.estado = "dialogo_inicial"
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
        tela.fill((240, 240, 240))  # Fundo cinza claro
        titulo = fonte_grande.render("Escolha 3 CInemons", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))

        # Dicionário de cores por tipo (usando tipos em maiúsculas, sem acentos)
        cores_tipos = {
            "FOGO": VERMELHO,
            "AGUA": AZUL,
            "PLANTA": VERDE,
            "ELETRICO": AMARELO,
            "TERRA": (139, 69, 19),  # Marrom para Terra
        }

        def carregar_sprite_cinemon(nome):
            """Carrega o sprite do CInemon em 80x80 pixels."""
            if nome in self.sprites_cache:
                return self.sprites_cache[nome]
            
            # Caminho absoluto a partir do diretório do script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            sprite_path = os.path.join(r"Desktop\CInemon-IP\cinemons", f"{nome}.png")
            
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (80, 80))
            self.sprites_cache[nome] = sprite
            return sprite
            

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
            x = 150 + (i % 5) * 180  # 5 colunas
            y = 150 + (i // 5) * 180  # 2 linhas
            rect = pygame.Rect(x, y, 150, 150)
            self.rects_cinemon.append(rect)

            # Cor do card baseada no tipo
            cor_card = cores_tipos[cinemon.tipo]  # Usa o tipo em maiúsculas, sem acentos
            pygame.draw.rect(tela, cor_card if i not in self.cinemons_escolhidos else ROXO, rect)
            pygame.draw.rect(tela, PRETO, rect, 2)

            # Sprite
            sprite = carregar_sprite_cinemon(cinemon.nome)
            if sprite:
                tela.blit(sprite, (x + 35, y + 40))  # Centralizado no topo
            else:
                pygame.draw.rect(tela, cinemon.cor, (x + 35, y + 40, 80, 80))

            # Nome
            nome = fonte.render(cinemon.nome, True, PRETO)
            tela.blit(nome, (x + 75 - nome.get_width()//2, y + 5))

        instrucao = fonte.render(f"Selecionados: {len(self.cinemons_escolhidos)}/3 - ENTER para confirmar", True, PRETO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 50))

    def renderizar_dialogo(self):
        tela.fill(AZUL_ESCURO)
        pygame.draw.rect(tela, BRANCO, (50, ALTURA - 200, LARGURA - 100, 150))
        pygame.draw.rect(tela, PRETO, (50, ALTURA - 200, LARGURA - 100, 150), 2)
        #teste

        



        caminho_imagem = os.path.join("Desktop", "CInemon-IP", "graphics", 'fotos', f'{self.inimigo_atual}.png')
        self.imagem = pygame.image.load(caminho_imagem)
        imagem_scaled = pygame.transform.smoothscale(self.imagem, (400, 300))
        tela.blit(imagem_scaled, (750, 220))



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
        # Enquanto o diálogo estiver ativo, verifica se é com a Enfermeira Joy para exibir joy.png
        if self.em_dialogo_npc and self.npc_atual and self.npc_atual.nome == 'Enfermeira Joy':
            tela.blit(self.joy_image, (0, 0))
        else:
            tela.fill(AZUL_ESCURO)

        pygame.draw.rect(tela, BRANCO, (50, ALTURA - 200, LARGURA - 100, 150))
        pygame.draw.rect(tela, PRETO, (50, ALTURA - 200, LARGURA - 100, 150), 2)
        
        texto = fonte.render(self.mensagem_dialogo[self.dialogo_atual], True, PRETO)
        tela.blit(texto, (70, ALTURA - 180))
        
        if self.dialogo_atual == 1 and self.jogador.dinheiro >= 50 and self.resposta_npc is None:
            instrucao = fonte.render("S para Sim | N para Não", True, PRETO)
        else:
            instrucao = fonte.render("Pressione ESPAÇO para continuar", True, PRETO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 100)) 

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
                        self.npc_atual = None  # Limpa o NPC atual apenas ao final do diálogo
                        self.dialogo_atual = 0
                elif self.dialogo_atual == 1 and self.jogador.dinheiro >= 50 and self.resposta_npc is None:
                    if evento.key == pygame.K_s:
                        self.responder_dialogo_npc('sim')
                    elif evento.key == pygame.K_n:
                        self.responder_dialogo_npc('nao')

    def responder_dialogo_npc(self, resposta):
        if resposta == 'sim' and self.jogador.dinheiro >= 50:
            self.jogador.dinheiro -= 50
            for cinemon in self.jogador_cinemons:
                cinemon.hp = cinemon.hp_max  # Cura total
            self.mensagem_dialogo = ["Enfermeira Joy: Seus CInemons estão como novos!"]
            self.dialogo_atual = 0
        elif resposta == 'nao':
            self.mensagem_dialogo = ["Enfermeira Joy: Tudo bem, volte quando precisar!"]
            self.dialogo_atual = 0
        self.resposta_npc = None  # Mantém o estado do diálogo ativo para continuar exibindo a imagem

        
    def mostrar_status_cinemons(self):
        tela.fill(AZUL_ESCURO)
        pygame.draw.rect(tela, BRANCO, (50, 50, LARGURA - 100, ALTURA - 100))
        pygame.draw.rect(tela, PRETO, (50, 50, LARGURA - 100, ALTURA - 100), 2)

        titulo = fonte_grande.render("CInemons", True, PRETO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 70))

        for i, cinemon in enumerate(self.jogador_cinemons):
            y_pos = 150 + i * 180
            nome_str = str(cinemon.nome)

            tipo_str = getattr(cinemon, 'tipo', 'DESCONHECIDO').strip().upper()

            # Painel de fundo azul escuro para melhor contraste
            pygame.draw.rect(tela, (10, 30, 80), (80, y_pos - 40, LARGURA - 160, 160), border_radius=10)

            nome = fonte.render(f"Nome: {nome_str}", True, BRANCO)
            tipo_label = fonte.render("Tipo:", True, (255, 165, 0))

            if tipo_str == "ELETRICO":
                tipo_valor = fonte.render("ELETRICO", True, (255, 255, 0))
            elif tipo_str == "FOGO":
                tipo_valor = fonte.render("FOGO", True, (255, 0, 0))
            elif tipo_str == "AGUA":
                tipo_valor = fonte.render("AGUA", True, (0, 0, 255))
            elif tipo_str == "PLANTA":
                tipo_valor = fonte.render("PLANTA", True, (0, 255, 0))
            else:
                tipo_valor = fonte.render("TERRA", True, (80, 50, 20))

            hp = fonte.render(f"HP: {cinemon.hp}/{cinemon.hp_max}", True, BRANCO if cinemon.hp > 0 else VERMELHO)
            status = fonte.render("Vivo" if cinemon.hp > 0 else "Morto", True, VERDE if cinemon.hp > 0 else VERMELHO)

            try:
                
                image_path = os.path.join("Desktop", "CInemon-IP", "cinemons", f"{nome_str}.png")

                cinemon_image = pygame.image.load(image_path)
                cinemon_image = pygame.transform.scale(cinemon_image, (150, 150))
                tela.blit(cinemon_image, (100, y_pos - 30))
                text_x_offset = 270
            except pygame.error:
                placeholder = fonte.render("(Imagem não encontrada)", True, BRANCO)
                tela.blit(placeholder, (100, y_pos - 30))
                text_x_offset = 270

            tela.blit(nome, (text_x_offset, y_pos))
            tela.blit(tipo_label, (text_x_offset, y_pos + 30))
            tela.blit(tipo_valor, (text_x_offset + 80, y_pos + 30))
            tela.blit(hp, (text_x_offset, y_pos + 60))
            tela.blit(status, (text_x_offset, y_pos + 90))

        instrucao = fonte.render("Pressione ESC para voltar ao mapa", True, PRETO)
        tela.blit(instrucao, (LARGURA // 2 - instrucao.get_width() // 2, ALTURA - 80))

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

    def verificar_interacao_npc(self):
        for npc in self.npcs:
            distancia = math.sqrt((self.jogador.x - npc.x)**2 + (self.jogador.y - npc.y)**2)
            if self.mapa_atual == 'basic.tmx' and distancia < 50:  # Distância de interação
                self.npc_atual = npc  # Armazena o NPC atual interagido
                return True
        return False

    def processar_dialogo_npc(self):
        if not hasattr(self, 'npc_atual') or self.npc_atual is None:
            return
        if self.jogador.dinheiro >= 50:
            self.mensagem_dialogo = [
                f"{self.npc_atual.nome}: Quer gastar 50 créditos para reanimar e curar seus CInemons?",
                "Pressione S para Sim ou N para Não"
            ]
        else:
            self.mensagem_dialogo = [
                f"{self.npc_atual.nome}: Você não tem créditos suficientes!",
                "Volte quando tiver pelo menos 50 créditos."
            ]
        self.em_dialogo_npc = True
        self.dialogo_atual = 0
        self.resposta_npc = None

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
        self.verificar_colisao_porta()  # Verifica portas de ida
        
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

        if self.mapa_atual == 'cin.tmx':
            self.pedro.desenhar(tela, self.camera, self.zoom)
        elif self.mapa_atual == 'basic.tmx':
            self.Sergio.desenhar(tela, self.camera, self.zoom)
            self.Fernanda.desenhar(tela, self.camera, self.zoom)
            self.Ricardo.desenhar(tela, self.camera, self.zoom)
            for npc in self.npcs:  # Desenha todos os NPCs
                npc.desenhar(tela, self.camera, self.zoom)

        for gema in self.gemas:
            if self.mapa_atual == 'basic.tmx':
                gema.desenhar(tela, self.camera, self.zoom)

        instrucao = fonte.render("WASD/Setas: Mover | ESC: Status | ESPAÇO: Falar com NPC", True, BRANCO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 30))
        
        if self.cinemon_jogador_atual:
            cinemon_info = fonte.render(
                f"CInemon atual: {self.cinemon_jogador_atual.nome} (HP: {self.cinemon_jogador_atual.hp}/{self.cinemon_jogador_atual.hp_max})", 
                True, BRANCO)
            tela.blit(cinemon_info, (10, 10))
        
        if self.batalha_vencida_Sergio:
            mensagem = fonte.render("Você derrotou Sergio!", True, VERDE)
            tela.blit(mensagem, (LARGURA//2 - mensagem.get_width()//2, 90))
            
        if self.batalha_vencida_Fernanda: 
            mensagem = fonte.render("Você derrotou Fernanda!", True, VERMELHO)
            tela.blit(mensagem, (LARGURA//2 - mensagem.get_width()//2, 110))
        if self.batalha_vencida_Ricardo: 
            mensagem = fonte.render("Você derrotou Ricardo!", True, VERMELHO)
            tela.blit(mensagem, (LARGURA//2 - mensagem.get_width()//2, 130))
            
        texto_dinheiro = fonte.render(f'Você tem {self.jogador.dinheiro} créditos', True, AMARELO)
        tela.blit(texto_dinheiro, (10, 40))
        
        texto_gemas = fonte.render(f"Gemas: {self.gemas_coletadas}", True, AMARELO)
        tela.blit(texto_gemas, (10, 70))
        
        # Novo: Exibir pedaços de crachá apenas se o crachá não estiver completo
        if self.cracha_completo == 0:
            texto_pedacos_cracha = fonte.render(f"Pedaços de Crachá: {self.pedacos_cracha}/3", True, AMARELO)
            tela.blit(texto_pedacos_cracha, (10, 100))
        else:
            texto_cracha_completo = fonte.render("Crachá Completo", True, AMARELO)
            tela.blit(texto_cracha_completo, (10, 100))

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
            elif self.estado == 'dialogo_inicial':
                self.renderizar_dialogo_inicial()
            elif self.estado == "dialogo":
                self.renderizar_dialogo()
            elif self.estado == "dialogo_npc":
                self.renderizar_dialogo_npc()
            elif self.estado == "creditos":
                self.creditos()
            #aqui
            elif self.estado == 'game_over':
                self.game_over()
            pygame.display.flip()
            relogio.tick(60)


    #tela de final de jogo, caso o jogagor vença
    def creditos(self):
        self.estado = 'creditos'
        tela.fill(AZUL)
        titulo_1 = fonte_grande.render("CINEMON IP", True, BRANCO)
        subtitulo_1 = fonte.render("Felipe Berardo, Gabriel Machado, Guilherme Máximo, Matheus Henrique, Matheus Stepple, Vinícius Pena", True, BRANCO)
        instrucao_1 = fonte.render("Muito Obrigado", True, BRANCO)
        instrucao_2 = fonte.render("Pressione ESPAÇO para sair", True, BRANCO)

        tela.blit(titulo_1, (LARGURA//2 - titulo_1.get_width()//2, 200))
        tela.blit(subtitulo_1, (LARGURA//2 - subtitulo_1.get_width()//2, 300))
        tela.blit(instrucao_1, (LARGURA//2 - instrucao_1.get_width()//2, 400))
        tela.blit(instrucao_2, (LARGURA//2 - instrucao_2.get_width()//2, 450))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pygame.quit()
                    sys.exit()

    #aqui
    # tela de final de jogo, caso o jogador perca               
    def game_over(self):
        self.estado = 'game_over'
        tela.fill(VERMELHO)
        titulo_1 = fonte_grande.render("VOCÊ PERDEU", True, BRANCO)
        subtitulo_1 = fonte.render("Pressione ENTER para tentar novamente", True, BRANCO)
        
        instrucao_2 = fonte.render("Pressione ESPAÇO para sair", True, BRANCO)

        tela.blit(titulo_1, (LARGURA//2 - titulo_1.get_width()//2, 200))
        tela.blit(subtitulo_1, (LARGURA//2 - subtitulo_1.get_width()//2, 300))
        
        tela.blit(instrucao_2, (LARGURA//2 - instrucao_2.get_width()//2, 450))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                print(f"Tecla pressionada: {evento.key}")
                if evento.key == pygame.K_SPACE:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_RETURN:
                    self.__init__()  
                    self.estado = "menu"  




def main():
    jogo = JogoUI()
    jogo.rodar()

if __name__ == "__main__":
    main()