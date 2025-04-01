# main.py
import sys
from jogo_ui import JogoUI
from config import (tela, fonte, fonte_grande, relogio, BRANCO, PRETO, VERMELHO, AZUL, VERDE, AMARELO, 
                    CINZA, ROXO, LARANJA, MARROM, AZUL_ESCURO, LARGURA, ALTURA, SISTEMA_DE_TIPOS)

def main():
    jogo = JogoUI()
    jogo.rodar()

if __name__ == "__main__":
    main()