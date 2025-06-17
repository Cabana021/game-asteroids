import pygame
import random
from .. import settings
from ..entities.explosion import Explosion
from ..entities.asteroid import Asteroid

class CollisionSystem:
    """
    Gerencia toda a lógica de detecção e resposta a colisões no jogo.
    Desacopla a lógica de colisão das próprias entidades.
    """
    def __init__(self, game_state, vfx_system, assets, app):
        self.state = game_state
        self.vfx = vfx_system
        self.assets = assets
        self.app = app
        self.points_multiplier = self.app.difficulty_settings["points_multiplier"]

    def process(self):
        """Método principal chamado a cada frame para verificar todas as colisões."""
        self._check_bullet_hits()
        self._check_player_collisions()

    def _check_bullet_hits(self):
        """Verifica colisões entre balas do jogador e inimigos (asteroides e UFOs)."""
        # Balas vs. Asteroides
        # 'groupcollide' retorna um dicionário de asteroides que colidiram.
        # Os dois 'True' removem tanto o asteroide quanto a bala dos seus grupos.
        collided_asteroids = pygame.sprite.groupcollide(self.state.asteroids, self.state.bullets, True, True, pygame.sprite.collide_mask)
        for asteroid in collided_asteroids:
            self._destroy_asteroid(asteroid)
        
        # Balas vs. UFOs
        collided_ufos = pygame.sprite.groupcollide(self.state.ufos, self.state.bullets, True, True, pygame.sprite.collide_mask)
        for ufo in collided_ufos:
            self._destroy_ufo(ufo)

    def _check_player_collisions(self):
        """Verifica colisões envolvendo a nave do jogador."""
        ship = self.state.ship
        # Só verifica colisões se a nave estiver viva e não invulnerável.
        if ship.alive() and not ship.invulnerable:
            # Nave vs. Asteroides
            hit_asteroid = pygame.sprite.spritecollideany(ship, self.state.asteroids, pygame.sprite.collide_mask)
            if hit_asteroid: self._player_hit(hit_asteroid); return
            
            # Nave vs. UFOs
            hit_ufo = pygame.sprite.spritecollideany(ship, self.state.ufos, pygame.sprite.collide_mask)
            if hit_ufo: self._player_hit(hit_ufo); return

            # Nave vs. Balas Inimigas
            hit_enemy_bullet = pygame.sprite.spritecollideany(ship, self.state.enemy_bullets, pygame.sprite.collide_mask)
            if hit_enemy_bullet: self._player_hit(hit_enemy_bullet)

    def _destroy_asteroid(self, asteroid, killed_by_player=True):
        """Lida com a destruição de um asteroide."""
        # Efeitos sonoros e visuais
        if self.app.sfx_on:
            if random.random() < 0.05: self.assets['scream_sound'].play() # Easter egg
            else: self.assets['explosion_sound'].play()
        
        self.vfx.create_particles(asteroid.rect.center, 15)
        self.vfx.trigger_shake(8)
        
        # Animação de explosão
        if self.assets['explosion_anim']:
            explosion = Explosion(asteroid.rect.center, self.assets['explosion_anim'])
            self.state.all_sprites.add(explosion)
        
        # Pontuação
        if killed_by_player:
            if asteroid.size == 3: base_points = settings.BASE_POINTS["ASTEROID_LARGE"]
            elif asteroid.size == 2: base_points = settings.BASE_POINTS["ASTEROID_MEDIUM"]
            else: base_points = settings.BASE_POINTS["ASTEROID_SMALL"]
            self.state.score += int(base_points * self.points_multiplier)
        
        # Se o asteroide for grande ou médio, cria dois menores em seu lugar.
        if asteroid.size > 1:
            for _ in range(2):
                new_asteroid = Asteroid(asteroid.size - 1, asteroid.position, self.assets['asteroid_image'])
                self.state.all_sprites.add(new_asteroid)
                self.state.asteroids.add(new_asteroid)
        
        asteroid.kill()

    def _destroy_ufo(self, ufo):
        """Lida com a destruição de um UFO."""
        # Pontuação
        base_points = settings.BASE_POINTS["UFO"]
        self.state.score += int(base_points * self.points_multiplier)
        
        # Efeitos visuais e sonoros (mais intensos para o UFO)
        self.vfx.create_particles(ufo.rect.center, 25, p_type='ufo_explosion')
        self.vfx.trigger_shake(15)
        if self.app.sfx_on: self.assets['explosion_sound'].play()
        
        # Animação de explosão
        if self.assets['explosion_anim']:
            explosion = Explosion(ufo.rect.center, self.assets['explosion_anim'])
            self.state.all_sprites.add(explosion)
            
        ufo.kill()
            
    def _player_hit(self, collided_sprite):
        """Lida com a nave do jogador sendo atingida."""
        self.state.lives -= 1
        
        # Efeitos visuais e sonoros (muito intensos para a morte do jogador)
        self.vfx.trigger_shake(25)
        if self.app.sfx_on: self.assets['explosion_sound'].play()
        self.vfx.create_particles(self.state.ship.rect.center, 30)
        
        # Animação de explosão
        if self.assets['explosion_anim']:
            explosion = Explosion(self.state.ship.rect.center, self.assets['explosion_anim'])
            self.state.all_sprites.add(explosion)
        
        # Remove o sprite que colidiu com o jogador (asteroide, ufo ou bala)
        collided_sprite.kill()

        # Se o jogador ainda tiver vidas, faz o respawn.
        if self.state.lives > 0:
            self.state.ship.respawn()