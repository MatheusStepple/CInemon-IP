import pygame
import pytmx
import sys
import random
import os
from Protagonista import Protagonista
from Perseguidor import Perseguidor
from Botao import Botao
from Coletaveis import Coletaveis
from Buff_velocidade import Buff_velocidade
from Monitor import Monitor
from Spawn import SpawnManager
from Matriz import maze
from Labirinto import Labirinto

# Constantes
LARGURA = 1296
ALTURA = 720
TAMANHO_CELULA = 24
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pacman")

# Carregar o fundo do menu com caminho relativo para 'imagens'

FUNDO_MENU = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "..", "imagens", "fundo_menu.jpg"))
FUNDO_MENU = pygame.transform.scale(FUNDO_MENU, (LARGURA, ALTURA))

# Função para carregar a fonte personalizada
def carregar_fonte(tamanho):
    fonte_path = os.path.join(os.path.dirname(__file__), "..", "..", "imagens", "PressStart2P-Regular.ttf")

    return pygame.font.Font(fonte_path, tamanho)
   

# Carregar o mapa
labirinto = Labirinto()
labirinto.carregar_mapa()

# Função para encontrar posição inicial
def encontrar_posicao_inicial():
    return LARGURA // 2, ALTURA // 2  # (648, 360)

# Função para desenhar contador de moedas
def desenhar_contador_moedas(tela, pontuacao):
    fonte = carregar_fonte(24)  # Usa a fonte personalizada
    texto = fonte.render(f"Moedas: {pontuacao}", True, BRANCO)
    tela.blit(texto, (10, 10))

# Loop principal do jogo
def jogo_principal():
    pos_x, pos_y = encontrar_posicao_inicial()
    jogador = Protagonista(pos_x, pos_y)
    vidas = 3

    matriz = maze
    moedas = Coletaveis.criar_moedas_na_matriz(matriz, TAMANHO_CELULA)
    monitores = Monitor.criar_monitores_na_matriz(matriz, TAMANHO_CELULA)
    total_moedas = len(moedas)

    inimigo = Perseguidor(170, 200)

    # Construção das paredes
    paredes = []
    for camada in labirinto.dados_tmx.layers:
        if isinstance(camada, pytmx.TiledTileLayer):
            if "colisão" in camada.name.lower():
                for y in range(camada.height):
                    for x in range(camada.width):
                        if camada.data[y][x] != 0:
                            paredes.append(pygame.Rect(
                                x * TAMANHO_CELULA,
                                y * TAMANHO_CELULA,
                                TAMANHO_CELULA,
                                TAMANHO_CELULA
                            ))
    print(f"Total de paredes carregadas: {len(paredes)}")

    pontuacao = 0
    relogio = pygame.time.Clock()

    itens_especiais = []
    powerups = []
    powerup_ativo = False
    spawner = SpawnManager()

    rodando = True
    while rodando:
        if pontuacao >= total_moedas:
            rodando = False
            print("Você coletou todas as moedas!")
            continue

        if inimigo.verificar_colisao(jogador):
            vidas -= 1
            if vidas <= 0:
                rodando = False
                print("Game Over!")
            else:
                jogador.x, jogador.y = encontrar_posicao_inicial()
                jogador.anim_frame = 0
                jogador.direction = "baixo"
                inimigo.x, inimigo.y = 170, 200
                inimigo.anim_frame = 0
                inimigo.direction = "baixo"

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        jogador.mover(teclas, paredes)
        jogador.limitar_bordas(LARGURA, ALTURA)
        inimigo.perseguir(jogador.x, jogador.y, paredes, LARGURA, ALTURA)

        for moeda in moedas[:]:
            if moeda.verificar_colisao(jogador):
                pontuacao += 1
                moedas.remove(moeda)

        for item in itens_especiais[:]:
            if item.verificar_colisao(jogador):
                itens_especiais.remove(item)

        for monitor in monitores[:]:
            if monitor.verificar_colisao(jogador):
                monitores.remove(monitor)

        if random.random() < 0.3 and not powerup_ativo:
            spawner.tentar_spawn_buff(moedas, itens_especiais, powerups, powerup_ativo, buff_aplicado=Buff_velocidade)

        # Desenho na tela
        tela.fill(PRETO)  # Limpa a tela primeiro
        labirinto.desenhar(tela)

        for moeda in moedas:
            moeda.desenhar(tela)
        for item in itens_especiais:
            item.desenhar(tela)
        for monitor in monitores:
            monitor.desenhar(tela)
        for powerup in powerups[:]:
            powerup.desenhar(tela)
            if powerup.verificar_colisao(jogador):
                powerups.remove(powerup)
                powerup_ativo = True

        jogador.modelo_personagem(tela)
        inimigo.desenhar(tela)

        # Desenha o contador por último para garantir visibilidade
        desenhar_contador_moedas(tela, pontuacao)
        pygame.display.flip()
        relogio.tick(60)

# Menu principal
def menu_principal():
    ativo = True
    while ativo:
        tela.blit(FUNDO_MENU, (0, 0))
        pos_mouse = pygame.mouse.get_pos()

        # Títulos do menu com fonte personalizada
        fonte_titulo = carregar_fonte(50)
        fonte_subtitulo = carregar_fonte(20)
        fonte_botao = carregar_fonte(16)

        titulo = fonte_titulo.render("Emanoel", True, (182, 143, 64))
        subtitulo = fonte_subtitulo.render("E o Labirinto Misterioso", True, (182, 143, 64))
        
        botao_jogar = Botao(
            pos=(LARGURA // 2, 250),
            text_input="JOGAR",
            font=fonte_botao,
            base_color=BRANCO,
            hovering_color=AZUL
        )
        
        botao_sair = Botao(
            pos=(LARGURA // 2, 325),
            text_input="SAIR",
            font=fonte_botao,
            base_color=BRANCO,
            hovering_color=AZUL
        )

        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2 + 4, 110)))
        tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA // 2 + 4, 160)))

        for botao in [botao_jogar, botao_sair]:
            botao.mudar_cor(pos_mouse)
            botao.update_tela(tela)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ativo = False
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.checar_clique(pos_mouse):
                    ativo = False
                    jogo_principal()
                elif botao_sair.checar_clique(pos_mouse):
                    ativo = False
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    menu_principal()
    pygame.quit()
    sys.exit()