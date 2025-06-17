import pygame
from . import settings
from .entities.ship import Ship

class GameSessionState:
    """
    Uma classe contêiner para armazenar todos os dados de uma única sessão de jogo.
    Isso desacopla os dados da lógica principal do jogo, facilitando o reinício
    de uma partida e o acesso a esses dados por diferentes sistemas.
    """
    def __init__(self, assets, difficulty_settings):
        # --- Grupos de Sprites ---
        # Esses grupos gerenciam a atualização e o desenho de todos os objetos do jogo.
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()  # Garante que haja apenas uma nave
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        
        # --- Variáveis de Estado da Partida ---
        self.score = 0
        self.lives = difficulty_settings["start_lives"]
        self.wave_count = 1
        
        # --- Inicialização do Jogador ---
        # Cria a instância da nave e a adiciona aos grupos relevantes.
        self.ship = Ship(assets['ship_image'])
        self.all_sprites.add(self.ship)
        self.player_group.add(self.ship)
