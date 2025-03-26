import pygame

# Inicialização do game, apenas se ligar na resolução
pygame.init()
tela = pygame.display.set_mode((1080, 820))
pygame.display.set_caption("GABIGOL EU TE AMO")
relogio = pygame.time.Clock()

# Cores default
VERDE = (100, 200, 100)
PRETO = (0, 0, 0)

# Definição e parâmetros do jogador 
jogador = pygame.Rect(400, 300, 32, 48)  # x, y, largura, altura
velocidade = 5

# loop de executar o jogo
executando = True
while executando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
    
    # Movimento padrão WASD
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: jogador.x -= velocidade
    if teclas[pygame.K_RIGHT]: jogador.x += velocidade
    if teclas[pygame.K_UP]: jogador.y -= velocidade
    if teclas[pygame.K_DOWN]: jogador.y += velocidade
    
    # Limites da tela
    jogador.x = max(0, min(jogador.x, 800 - jogador.width))
    jogador.y = max(0, min(jogador.y, 600 - jogador.height))
    
    # Desenho
    tela.fill(VERDE)  # Grama fillado na tela inteira (mudar dps)
    pygame.draw.rect(tela, PRETO, jogador)  # Personagem (ponto preto)
    
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()