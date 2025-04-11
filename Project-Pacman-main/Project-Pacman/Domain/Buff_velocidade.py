from Coletaveis import Coletaveis

class Buff_velocidade(Coletaveis):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.raio = 8
        self.cor = (0, 0, 255)
