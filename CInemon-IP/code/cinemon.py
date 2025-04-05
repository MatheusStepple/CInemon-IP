from config import *

class CInemon:
    def __init__(self, nome, tipo, hp_max, velocidade, ataques):
        self.nome = nome
        self.tipo = tipo
        self.hp = hp_max
        self.hp_max = hp_max
        self.velocidade = velocidade
        self.ataques = ataques
        self.cor = self._definir_cor_tipo()
    
    def _definir_cor_tipo(self):
        cores = {
            "FOGO": VERMELHO,
            "AGUA": AZUL,
            "PLANTA": VERDE,
            "ELETRICO": AMARELO,
            "TERRA": MARROM,
            "ESPECIAL": ROXO
        }
        return cores.get(self.tipo, BRANCO)