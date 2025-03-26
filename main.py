import pygame

class Jogador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 48)
        self.velocidade = 5
        self.cor = (0, 0, 0)
    
    def mover(self, teclas):
        if teclas[pygame.K_LEFT]: self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT]: self.rect.x += self.velocidade
        if teclas[pygame.K_UP]: self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN]: self.rect.y += self.velocidade
        self._limitar_movimento()
    
    def _limitar_movimento(self):
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
    
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("GABIGOL LINDO")
        self.relogio = pygame.time.Clock()
        self.jogador = Jogador(400, 300)
        self.cor_fundo = (100, 200, 100)
        self.executando = True
    
    def rodar(self):
        while self.executando:
            self._processar_eventos()
            self._atualizar()
            self._desenhar()
            self.relogio.tick(60)
        pygame.quit()
    
    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.executando = False
    
    def _atualizar(self):
        teclas = pygame.key.get_pressed()
        self.jogador.mover(teclas)
    
    def _desenhar(self):
        self.tela.fill(self.cor_fundo)
        self.jogador.desenhar(self.tela)
        pygame.display.flip()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.rodar()
