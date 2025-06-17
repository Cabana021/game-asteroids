import pygame
import random
from src import settings
from .bullet import EnemyBullet

class UFO(pygame.sprite.Sprite):
    """
    Representa a nave inimiga (UFO).
    Pode ter diferentes padrões de movimento e atira no jogador.
    """
    def __init__(self, assets, all_sprites_group, enemy_bullets_group, app, movement_pattern="horizontal"):
        super().__init__()
        
        # --- Referências Externas ---
        self.assets = assets
        self.all_sprites = all_sprites_group
        self.enemy_bullets = enemy_bullets_group
        self.app = app
        
        # --- Configuração de Movimento e Aparência ---
        self.movement_pattern = movement_pattern
        ufo_speed = self.app.difficulty_settings["ufo_speed"]

        # Define a imagem, posição inicial e velocidade com base no padrão de movimento.
        if self.movement_pattern == "horizontal":
            self.image = self.assets['ufo_image']
            spawn_side = random.choice([-1, 1])
            y = random.randint(50, settings.SCREEN_HEIGHT - 200)
            if spawn_side == -1: # Esquerda
                x = -self.image.get_width()
                self.velocity = pygame.math.Vector2(ufo_speed, 0)
            else: # Direita
                x = settings.SCREEN_WIDTH + self.image.get_width()
                self.velocity = pygame.math.Vector2(-ufo_speed, 0)
        
        elif self.movement_pattern == "vertical":
            self.image = self.assets['ufo_vertical_image']
            spawn_side = random.choice([-1, 1])
            x = random.randint(100, settings.SCREEN_WIDTH - 100)
            if spawn_side == -1: # Cima
                y = -self.image.get_height()
                self.velocity = pygame.math.Vector2(0, ufo_speed)
            else: # Baixo
                y = settings.SCREEN_HEIGHT + self.image.get_height()
                self.velocity = pygame.math.Vector2(0, -ufo_speed)
        
        # --- Configuração de Sprite e Posição ---
        self.mask = pygame.mask.from_surface(self.image)
        self.position = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.position)
        
        # --- Lógica de Tiro ---
        self.shot_cooldown = self.app.difficulty_settings["ufo_shot_cooldown"]
        self.shot_timer = random.uniform(0.5, 1.5) * self.shot_cooldown # Delay inicial variado para não atirar imediatamente

    def update(self, dt, player_ship):
        """Atualiza a posição do UFO, verifica se saiu da tela e tenta atirar."""
        # Movimento
        self.position += self.velocity * (dt / (1000.0 / settings.FPS))
        self.rect.center = self.position
        
        # Autodestruição se sair completamente da área de jogo.
        if (self.rect.right < -50 or self.rect.left > settings.SCREEN_WIDTH + 50 or
            self.rect.bottom < -50 or self.rect.top > settings.SCREEN_HEIGHT + 50):
            self.kill()
            
        # Lógica de tiro
        self._shoot_at_player(dt, player_ship)

    def _shoot_at_player(self, dt, player_ship):
        """Verifica o cooldown e atira na direção do jogador."""
        self.shot_timer -= dt
        if self.shot_timer <= 0:
            self.shot_timer = self.shot_cooldown # Reseta o timer
            
            if player_ship.alive():
                # Calcula a direção do UFO até a nave do jogador.
                direction = pygame.math.Vector2(player_ship.rect.center) - self.position
                if direction.length() > 0:
                    direction.normalize_ip() # Normaliza para obter um vetor de direção unitário
                
                # Cria e adiciona a bala aos grupos.
                bullet = EnemyBullet(self.rect.center, direction, self.assets['enemy_gunshot_image'])
                self.all_sprites.add(bullet)
                self.enemy_bullets.add(bullet)
                
                if self.app.sfx_on:
                    self.assets['enemy_gunshot_sound'].play()