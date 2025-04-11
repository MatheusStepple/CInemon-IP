import pygame
import pytmx
import os
from pathlib import Path

class Labirinto:
    def __init__(self):
        # Configurações
        self.TAMANHO_TILE = 24
        self.LARGURA_TELA = 54 * self.TAMANHO_TILE
        self.ALTURA_TELA = 30 * self.TAMANHO_TILE
        
        # Cores
        self.BLACK = (0, 0, 0)
        self.COLISION_COLOR = (255, 0, 0, 128)
        
        # Caminhos
        self.assets_dir = Path(__file__).parent / "assets"
        self.map_filename = "mapa_final.tmx"
        self.map_path = str(self.assets_dir / self.map_filename)
        self.dados_tmx = None
    
    def load_tmx_map(self, filename):
        """Carrega o mapa TMX"""
        return pytmx.load_pygame(filename)
    
    def carregar_mapa(self):
        """Carrega o mapa TMX"""
        if not os.path.exists(self.map_path):
            raise FileNotFoundError(f"Arquivo de mapa não encontrado: {self.map_path}")
        self.dados_tmx = self.load_tmx_map(self.map_path)
    
    def desenhar(self, tela):
        """Desenha o labirinto na tela, exceto camadas com nomes específicos"""
        if self.dados_tmx is None:
            return
        
        CAMADA_INVISIVEL = "colisão"  # Ou o nome da sua camada que deve ser invisível
        
        for layer in self.dados_tmx.layers:
            if isinstance(layer, pytmx.TiledTileLayer) and CAMADA_INVISIVEL not in layer.name.lower():
                for x, y, gid in layer:
                    tile = self.dados_tmx.get_tile_image_by_gid(gid)
                    if tile:
                        tela.blit(tile, (x * self.TAMANHO_TILE, y * self.TAMANHO_TILE))
    
    def get_matriz_labirinto(self):
        """Retorna matriz onde 0 = vazio e 1 = parede"""
        matriz = []
        for y in range(self.dados_tmx.height):
            linha = []
            for x in range(self.dados_tmx.width):
                tem_parede = any(
                    layer.data[y][x] != 0
                    for layer in self.dados_tmx.layers
                    if isinstance(layer, pytmx.TiledTileLayer) and "colisão" in layer.name.lower()
                )
                linha.append(1 if tem_parede else 0)
            matriz.append(linha)
        return matriz

if __name__ == "__main__":
    pygame.init()
    labirinto = Labirinto()
    tela = pygame.display.set_mode((labirinto.LARGURA_TELA, labirinto.ALTURA_TELA))
    pygame.display.set_caption("Teste do Labirinto")
        
        # Carrega o mapa antes de desenhar
    labirinto.carregar_mapa()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        tela.fill(labirinto.BLACK)
        labirinto.desenhar(tela)
        pygame.display.flip()
        clock.tick(60)