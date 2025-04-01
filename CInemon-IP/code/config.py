import pygame

LARGURA, ALTURA = 1024, 768

tela = pygame.display.set_mode((LARGURA, ALTURA))
display_do_jogo = "CInemon IP - A Revolução"


SISTEMA_DE_TIPOS = {
    "FOGO": {"AGUA": 0.5, "PLANTA": 2.0},
    "AGUA": {"FOGO": 2.0, "ELETRICO": 0.5},
    "PLANTA": {"TERRA": 2.0, "FOGO": 0.5},
    "ELETRICO": {"AGUA": 2.0, "TERRA": 0.5},
    "TERRA": {"ELETRICO": 2.0, "PLANTA": 0.5},
    "ESPECIAL": {"FOGO": 1.5, "ELETRICO": 1.5}
}


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