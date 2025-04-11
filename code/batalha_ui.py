import pygame
import sys
import os
from jogo_base import JogoBase
from config import (tela, fonte, fonte_grande, relogio, CINZA, BRANCO, PRETO, VERMELHO, AZUL, VERDE, LARGURA, ALTURA)

class BatalhaUI(JogoBase):
    def __init__(self):
        super().__init__()
        self.tempo_tremor_jogador = 0
        self.tempo_tremor_inimigo = 0
        self.tremor_offset_jogador = [0, 0]
        self.tremor_offset_inimigo = [0, 0]
        self.hp_jogador_anterior = None
        self.hp_inimigo_anterior = None
        self.sprites_cache = {}

    def carregar_sprite_cinemon(self, nome, tamanho):
        """Carrega o sprite do CInemon com o tamanho especificado."""
        chave_cache = f"{nome}_{tamanho[0]}x{tamanho[1]}"
        if chave_cache in self.sprites_cache:
            return self.sprites_cache[chave_cache]
        
        sprite_path = os.path.join(r"cinemons", f"{nome}.png")
        try:
            sprite = pygame.image.load(sprite_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, tamanho)
            self.sprites_cache[chave_cache] = sprite
            return sprite
        except Exception as e:
            print(f"Erro ao carregar sprite do CInemon {nome}: {e}")
            return None

    def desenhar_barra_vida(self, tela, x, y, hp_atual, hp_max, tempo_tremor, tremor_offset):
        largura_barra = 200
        altura_barra = 20
        hp_atual = max(0, hp_atual)
        proporcao = hp_atual / hp_max
        largura_verde = int(largura_barra * proporcao)

        offset_x = tremor_offset[0] if tempo_tremor > 0 else 0
        offset_y = tremor_offset[1] if tempo_tremor > 0 else 0

        pygame.draw.rect(tela, VERMELHO, (x + offset_x, y + offset_y, largura_barra, altura_barra))
        pygame.draw.rect(tela, VERDE, (x + offset_x, y + offset_y, largura_verde, altura_barra))
        pygame.draw.rect(tela, PRETO, (x + offset_x, y + offset_y, largura_barra, altura_barra), 2)

    def renderizar_batalha(self, jogo):
        tela.fill((200, 230, 255))
        
        # Atualizar offsets de tremor
        if self.tempo_tremor_jogador > 0:
            self.tremor_offset_jogador = [pygame.time.get_ticks() % 2 * 4 - 2, pygame.time.get_ticks() % 2 * 4 - 2]
            self.tempo_tremor_jogador -= 1
        if self.tempo_tremor_inimigo > 0:
            self.tremor_offset_inimigo = [pygame.time.get_ticks() % 2 * 4 - 2, pygame.time.get_ticks() % 2 * 4 - 2]
            self.tempo_tremor_inimigo -= 1

        pygame.draw.rect(tela, AZUL, (50, 50, 400, 200))
        pygame.draw.rect(tela, VERMELHO, (LARGURA - 450, 50, 400, 200))
        
        jogador = jogo.cinemon_jogador_atual
        nome_jogador = fonte_grande.render(jogador.nome, True, BRANCO)
        hp_jogador = fonte.render(f"HP: {max(0, jogador.hp)}/{jogador.hp_max}", True, BRANCO)
        tela.blit(nome_jogador, (70, 70))
        tela.blit(hp_jogador, (70, 110))
        self.desenhar_barra_vida(tela, 70, 150, jogador.hp, jogador.hp_max, 
                                self.tempo_tremor_jogador, self.tremor_offset_jogador)
        sprite_jogador = self.carregar_sprite_cinemon(jogador.nome, (300, 300))
        sprite_jogador_x = 70 + (self.tremor_offset_jogador[0] if self.tempo_tremor_jogador > 0 else 0)
        sprite_jogador_y = 220 + (self.tremor_offset_jogador[1] if self.tempo_tremor_jogador > 0 else 0)
        if sprite_jogador:
            tela.blit(sprite_jogador, (sprite_jogador_x, sprite_jogador_y))
        else:
            pygame.draw.rect(tela, jogador.cor, (sprite_jogador_x, sprite_jogador_y, 300, 300))
        
        inimigo = jogo.cinemon_inimigo_atual
        nome_inimigo = fonte_grande.render(inimigo.nome, True, BRANCO)
        hp_inimigo = fonte.render(f"HP: {max(0, inimigo.hp)}/{inimigo.hp_max}", True, BRANCO)
        tela.blit(nome_inimigo, (LARGURA - 430, 70))
        tela.blit(hp_inimigo, (LARGURA - 430, 110))
        self.desenhar_barra_vida(tela, LARGURA - 430, 150, inimigo.hp, inimigo.hp_max, 
                                self.tempo_tremor_inimigo, self.tremor_offset_inimigo)
        sprite_inimigo = self.carregar_sprite_cinemon(inimigo.nome, (300, 300))
        sprite_inimigo_x = (LARGURA - 430) + (self.tremor_offset_inimigo[0] if self.tempo_tremor_inimigo > 0 else 0)
        sprite_inimigo_y = 220 + (self.tremor_offset_inimigo[1] if self.tempo_tremor_inimigo > 0 else 0)
        if sprite_inimigo:
            tela.blit(sprite_inimigo, (sprite_inimigo_x, sprite_inimigo_y))
        else:
            pygame.draw.rect(tela, inimigo.cor, (sprite_inimigo_x, sprite_inimigo_y, 300, 300))
        
        pygame.draw.rect(tela, BRANCO, (50, ALTURA - 200, LARGURA - 100, 150))
        pygame.draw.rect(tela, PRETO, (50, ALTURA - 200, LARGURA - 100, 150), 2)
        
        linhas = jogo.mensagem_atual.split('\n')
        for i, linha in enumerate(linhas):
            texto = fonte.render(linha, True, PRETO)
            tela.blit(texto, (70, ALTURA - 180 + i * 30))
        
        if jogo.fase_batalha == 0 and jogo.turno_jogador and not jogo.aguardando_espaco:
            opcoes = fonte.render(f"1. {jogador.ataques[0][0]}  2. {jogador.ataques[1][0]}  3. Trocar", True, PRETO)
            tela.blit(opcoes, (LARGURA//2 - opcoes.get_width()//2, ALTURA - 50))
        
        if jogo.aguardando_espaco:
            instrucao = fonte.render("Pressione ESPAÇO para continuar", True, PRETO)
            tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 50))

        self.hp_jogador_anterior = jogador.hp
        self.hp_inimigo_anterior = inimigo.hp

    def tela_trocar_cinemon(self, jogo):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1 and len(jogo.jogador_cinemons) >= 1 and jogo.jogador_cinemons[0].hp > 0:
                    antigo = jogo.cinemon_jogador_atual.nome
                    jogo.cinemon_jogador_atual = jogo.jogador_cinemons[0]
                    jogo.mensagem_atual = f"Você trocou {antigo} por {jogo.cinemon_jogador_atual.nome}!"
                    jogo.estado = "batalha"
                    jogo.fase_batalha = 0
                    jogo.turno_jogador = True
                    jogo.aguardando_espaco = False
                elif evento.key == pygame.K_2 and len(jogo.jogador_cinemons) >= 2 and jogo.jogador_cinemons[1].hp > 0:
                    antigo = jogo.cinemon_jogador_atual.nome
                    jogo.cinemon_jogador_atual = jogo.jogador_cinemons[1]
                    jogo.mensagem_atual = f"Você trocou {antigo} por {jogo.cinemon_jogador_atual.nome}!"
                    jogo.estado = "batalha"
                    jogo.fase_batalha = 0
                    jogo.turno_jogador = True
                    jogo.aguardando_espaco = False
                elif evento.key == pygame.K_3 and len(jogo.jogador_cinemons) >= 3 and jogo.jogador_cinemons[2].hp > 0:
                    antigo = jogo.cinemon_jogador_atual.nome
                    jogo.cinemon_jogador_atual = jogo.jogador_cinemons[2]
                    jogo.mensagem_atual = f"Você trocou {antigo} por {jogo.cinemon_jogador_atual.nome}!"
                    jogo.estado = "batalha"
                    jogo.fase_batalha = 0
                    jogo.turno_jogador = True
                    jogo.aguardando_espaco = False
                elif evento.key == pygame.K_ESCAPE:
                    jogo.estado = "batalha"

        tela.fill((200, 200, 255))
        titulo = fonte_grande.render("Escolha um CInemon", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))

        for i, cinemon in enumerate(jogo.jogador_cinemons):
            y = 150 + i * 150
            retangulo_x = LARGURA//2 - 250
            retangulo_largura = 500
            retangulo_altura = 120
            
            pygame.draw.rect(tela, BRANCO if cinemon.hp > 0 else CINZA, 
                            (retangulo_x, y, retangulo_largura, retangulo_altura))
            pygame.draw.rect(tela, PRETO, 
                            (retangulo_x, y, retangulo_largura, retangulo_altura), 2)
            
            sprite = self.carregar_sprite_cinemon(cinemon.nome, (100, 100))
            sprite_x = retangulo_x + 20
            sprite_y = y + (retangulo_altura - 100) // 2
            if sprite:
                tela.blit(sprite, (sprite_x, sprite_y))
            else:
                pygame.draw.rect(tela, cinemon.cor, (sprite_x, sprite_y, 100, 100))
            
            texto_x = retangulo_x + 140
            nome = fonte.render(f"{i+1}. {cinemon.nome} ({cinemon.tipo})", True, PRETO)
            hp = fonte.render(f"HP: {max(0, cinemon.hp)}/{cinemon.hp_max}", True, PRETO)
            status = fonte.render("ATIVO" if cinemon.hp > 0 else "DESMAIADO", 
                                True, VERMELHO if cinemon.hp <= 0 else VERDE)
            
            tela.blit(nome, (texto_x, y + 20))
            tela.blit(hp, (texto_x, y + 50))
            tela.blit(status, (texto_x, y + 80))

        instrucao = fonte.render("Pressione 1-3 para escolher ou ESC para cancelar", True, PRETO)
        tela.blit(instrucao, (LARGURA//2 - instrucao.get_width()//2, ALTURA - 50))

    def processar_batalha(self, jogo):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and jogo.aguardando_espaco:
                    jogo.aguardando_espaco = False
                    if jogo.cinemon_inimigo_atual.hp <= 0:
                        jogo.proximo_inimigo()
                    elif jogo.cinemon_jogador_atual.hp <= 0 and any(c.hp > 0 for c in jogo.jogador_cinemons):
                        jogo.estado = "trocar_cinemon"
                    elif jogo.cinemon_jogador_atual.hp <= 0 and not any(c.hp > 0 for c in jogo.jogador_cinemons):
                        
                        
                        
                        #aqui
                        jogo.estado = 'game_over'
                        
                        
                    elif jogo.fase_batalha == 1:
                        jogo.fase_batalha = 2
                        jogo.turno_jogador = False
                        jogo.mensagem_atual = f"{jogo.cinemon_inimigo_atual.nome} está atacando..."
                        pygame.time.delay(1000)
                        hp_inimigo_antes = jogo.cinemon_inimigo_atual.hp
                        jogo.executar_ataque_inimigo()
                        if self.hp_jogador_anterior is not None and jogo.cinemon_jogador_atual.hp < self.hp_jogador_anterior:
                            self.tempo_tremor_jogador = 15
                    elif jogo.fase_batalha == 3:
                        jogo.fase_batalha = 0
                        jogo.turno_jogador = True
                if jogo.fase_batalha == 0 and jogo.turno_jogador and not jogo.aguardando_espaco:
                    if evento.key == pygame.K_1:
                        jogo.acao_selecionada = 0
                        hp_inimigo_antes = jogo.cinemon_inimigo_atual.hp
                        jogo.executar_ataque_jogador()
                        if hp_inimigo_antes is not None and jogo.cinemon_inimigo_atual.hp < hp_inimigo_antes:
                            self.tempo_tremor_inimigo = 15
                    elif evento.key == pygame.K_2:
                        jogo.acao_selecionada = 1
                        hp_inimigo_antes = jogo.cinemon_inimigo_atual.hp
                        jogo.executar_ataque_jogador()
                        if hp_inimigo_antes is not None and jogo.cinemon_inimigo_atual.hp < hp_inimigo_antes:
                            self.tempo_tremor_inimigo = 15
                    elif evento.key == pygame.K_3:
                        jogo.estado = "trocar_cinemon"