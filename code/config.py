# config.py
import pygame

# Constants
LARGURA = 1080
ALTURA = 720
VERDE = (0, 128, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
ROXO = (128, 0, 128)
CINZA = (128, 128, 128)
AMARELO = (255, 255, 0)
AZUL_ESCURO = (0, 0, 128)
LARANJA = (255, 165, 0)  # Added if needed
MARROM = (165, 42, 42)   # Added if needed

# Type effectiveness (example, adjust as needed)
SISTEMA_DE_TIPOS = {
    "FOGO": {"AGUA": 0.5, "PLANTA": 2.0, "FOGO": 0.5},
    "AGUA": {"FOGO": 2.0, "TERRA": 0.5, "AGUA": 0.5},
    "PLANTA": {"TERRA": 2.0, "FOGO": 0.5, "PLANTA": 0.5},
    "TERRA": {"ELETRICO": 2.0, "AGUA": 2.0, "TERRA": 0.5},
    "ELETRICO": {"AGUA": 2.0, "TERRA": 0.5, "ELETRICO": 0.5},
    "ESPECIAL": {"ESPECIAL": 1.0}  # Default for now
}

# Pygame initialization
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("CINEMON IP - A Revolução")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 24)
fonte_grande = pygame.font.SysFont("Arial", 36)