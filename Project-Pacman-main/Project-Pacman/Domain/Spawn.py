import pygame
import random
from Coletaveis import *

class SpawnManager:
    def __init__(self):
        self.locais_moedas = []
        self.locais_monitores = []
        self.tempo_ultimo_spawn = 0
        self.intervalo_spawn = 10000  # 5 segundos em ms

    def adicionar_local_moeda(self, x, y):
        self.locais_moedas.append((y, x))
        
    def adicionar_local_monitor(self, x, y):
        self.locais_monitores.append((y, x))

    def tentar_spawn_buff(self, moedas, monitores, buffs, buff_on_map, buff_aplicado):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_spawn > self.intervalo_spawn:
            # Cria lista de todas as posições ocupadas
            posicoes_ocupadas = []
            
            # Adiciona posições das moedas
            for moeda in moedas:
                posicoes_ocupadas.append((moeda.x, moeda.y))
            
            # Adiciona posições dos monitores
            for monitor in monitores:
                posicoes_ocupadas.append((monitor.x, monitor.y))
            
            # Adiciona posições dos buffs existentes
            for buff in buffs:
                posicoes_ocupadas.append((buff.x, buff.y))
            
            # Filtra locais disponíveis que não estão ocupados
            locais_disponiveis = [
                (x, y) for (y, x) in self.locais_moedas + self.locais_monitores 
                if (x, y) not in posicoes_ocupadas
            ]
            
            if locais_disponiveis and not buff_on_map:
                x, y = random.choice(locais_disponiveis)
                buffs.append(buff_aplicado(x, y))
                self.tempo_ultimo_spawn = tempo_atual