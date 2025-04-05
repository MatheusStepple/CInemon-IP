import pygame
import sys
from jogo_base import JogoBase
from config import (tela, fonte, fonte_grande, relogio,CINZA, BRANCO, PRETO, VERMELHO, AZUL, VERDE, LARGURA, ALTURA)

class BatalhaUI(JogoBase):
    def renderizar_batalha(self, jogo):
        tela.fill((200, 230, 255))
        pygame.draw.rect(tela, AZUL, (50, 50, 400, 200))
        pygame.draw.rect(tela, VERMELHO, (LARGURA - 450, 50, 400, 200))
        
        jogador = jogo.cinemon_jogador_atual
        nome_jogador = fonte_grande.render(jogador.nome, True, BRANCO)
        hp_jogador = fonte.render(f"HP: {jogador.hp}/{jogador.hp_max}", True, BRANCO)
        tela.blit(nome_jogador, (70, 70))
        tela.blit(hp_jogador, (70, 110))
        
        inimigo = jogo.cinemon_inimigo_atual
        nome_inimigo = fonte_grande.render(inimigo.nome, True, BRANCO)
        hp_inimigo = fonte.render(f"HP: {inimigo.hp}/{inimigo.hp_max}", True, BRANCO)
        tela.blit(nome_inimigo, (LARGURA - 430, 70))
        tela.blit(hp_inimigo, (LARGURA - 430, 110))
        
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
                    elif jogo.fase_batalha == 1:
                        jogo.fase_batalha = 2
                        jogo.turno_jogador = False
                        jogo.mensagem_atual = f"{jogo.cinemon_inimigo_atual.nome} está atacando..."
                        pygame.time.delay(1000)
                        jogo.executar_ataque_inimigo()
                    elif jogo.fase_batalha == 3:
                        jogo.fase_batalha = 0
                        jogo.turno_jogador = True
                if jogo.fase_batalha == 0 and jogo.turno_jogador and not jogo.aguardando_espaco:
                    if evento.key == pygame.K_1:
                        jogo.acao_selecionada = 0
                        jogo.executar_ataque_jogador()
                    elif evento.key == pygame.K_2:
                        jogo.acao_selecionada = 1
                        jogo.executar_ataque_jogador()
                    elif evento.key == pygame.K_3:
                        jogo.estado = "trocar_cinemon"