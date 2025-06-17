import pygame
import random
from .. import settings
from ..entities.asteroid import Asteroid
from ..entities.ufo import UFO

class SpawnSystem:
    """
    Gerencia o aparecimento de inimigos (asteroides e UFOs) no jogo.
    Controla o ritmo, a quantidade e a posição dos spawns.
    """
    def __init__(self, game_state, assets, app):
        self.state = game_state
        self.assets = assets
        self.app = app
        
        # --- Configurações de Spawn de Asteroides ---
        self.asteroid_spawn_timer = 0
        self.max_asteroids = self.app.difficulty_settings["max_asteroids"]
        
        # --- Configurações de Spawn de UFOs ---
        self.ufo_spawn_countdown = self.app.difficulty_settings["ufo_spawn_rate"]
        self.num_ufos_to_spawn = self.app.difficulty_settings["num_ufos"]
        
        # Inicia o jogo com uma quantidade inicial de asteroides.
        self.spawn_initial_asteroids(self.app.difficulty_settings["initial_asteroids"])

    def update(self, dt):
        """Atualiza os timers de spawn a cada frame e cria inimigos quando necessário."""
        # --- Lógica de Spawn de Asteroides ---
        self.asteroid_spawn_timer -= dt
        if self.asteroid_spawn_timer <= 0:
            # Reseta o timer com um valor aleatório para um spawn menos previsível.
            self.asteroid_spawn_timer = random.uniform(2000, 4000)
            if len(self.state.asteroids) < self.max_asteroids:
                self._spawn_asteroid_at_edge()

        # Aumenta gradualmente o número máximo de asteroides a cada 30 segundos.
        if pygame.time.get_ticks() % 30000 < dt:
             self.max_asteroids = min(self.max_asteroids + 1, 20)  # Limite máximo de 20

        # --- Lógica de Spawn de UFOs ---
        # Só conta o tempo para spawnar UFOs se não houver nenhum na tela.
        if not self.state.ufos:
            self.ufo_spawn_countdown -= dt
            if self.ufo_spawn_countdown <= 0:
                self._spawn_ufos()
                # Reseta o countdown para a próxima onda de UFOs.
                self.ufo_spawn_countdown = self.app.difficulty_settings["ufo_spawn_rate"]

    def spawn_initial_asteroids(self, number):
        """Cria a leva inicial de asteroides no começo do jogo."""
        for _ in range(number):
            # Procura uma posição segura para o spawn, longe da nave do jogador.
            while True:
                pos = pygame.math.Vector2(random.randrange(settings.SCREEN_WIDTH), random.randrange(settings.SCREEN_HEIGHT))
                if not self.state.ship.alive() or pos.distance_to(self.state.ship.position) > settings.SAFE_SPAWN_DISTANCE:
                    break
            self._spawn_asteroid(3, pos) # Spawn de um asteroide grande

    def _spawn_asteroid_at_edge(self):
        """Cria um único asteroide em uma das bordas da tela."""
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        
        if edge == 'top':
            pos = pygame.math.Vector2(random.randrange(settings.SCREEN_WIDTH), -50)
        elif edge == 'bottom':
            pos = pygame.math.Vector2(random.randrange(settings.SCREEN_WIDTH), settings.SCREEN_HEIGHT + 50)
        elif edge == 'left':
            pos = pygame.math.Vector2(-50, random.randrange(settings.SCREEN_HEIGHT))
        else: # 'right'
            pos = pygame.math.Vector2(settings.SCREEN_WIDTH + 50, random.randrange(settings.SCREEN_HEIGHT))
            
        self._spawn_asteroid(3, pos) # Spawn de um asteroide grande

    def _spawn_asteroid(self, size, position):
        """Cria uma instância de Asteroide e a adiciona aos grupos de sprites."""
        asteroid = Asteroid(size, position, self.assets['asteroid_image'])
        self.state.all_sprites.add(asteroid)
        self.state.asteroids.add(asteroid)

    def _spawn_ufos(self):
        """Cria a quantidade de UFOs definida pela dificuldade, com padrões de movimento variados."""
        if self.num_ufos_to_spawn == 1:
            patterns = ["horizontal"]
        elif self.num_ufos_to_spawn >= 2:
            patterns = ["horizontal", "vertical"]
        else:
            patterns = []

        # Garante que não spawne mais UFOs do que o planejado.
        patterns_to_spawn = patterns[:self.num_ufos_to_spawn]

        for pattern in patterns_to_spawn:
            ufo = UFO(self.assets, self.state.all_sprites, self.state.enemy_bullets, self.app, movement_pattern=pattern)
            self.state.all_sprites.add(ufo)
            self.state.ufos.add(ufo)