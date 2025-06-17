import pygame
import random
from ..entities.particles import Particle 

class VFXSystem:
    """
    Sistema de Efeitos Visuais (Visual Effects).
    Gerencia a criação de partículas e o efeito de "screen shake".
    """
    def __init__(self, game_state, app):
        self.state = game_state
        self.app = app
        
        # Variáveis para controlar o "screen shake"
        self.shake_magnitude = 0  # Intensidade do tremor
        self.shake_duration = 0   # Duração do tremor em frames

    def trigger_shake(self, magnitude, duration=10):
        """
        Ativa o efeito de "screen shake".
        Se um shake já estiver ativo, mantém o de maior magnitude/duração.
        """
        # Ignora o efeito se estiver desativado nas configurações.
        if not self.app.screen_shake_on:
            return
            
        self.shake_magnitude = max(self.shake_magnitude, magnitude)
        self.shake_duration = max(self.shake_duration, duration)

    def update(self):
        """Atualiza o estado do "screen shake" a cada frame."""
        # Se o shake estiver desativado globalmente, reseta e sai.
        if not self.app.screen_shake_on:
            self.shake_magnitude = 0
            self.shake_duration = 0
            return

        # Reduz a duração do shake a cada frame.
        if self.shake_duration > 0:
            self.shake_duration -= 1
            # Quando a duração chega a zero, reseta a magnitude.
            if self.shake_duration == 0:
                self.shake_magnitude = 0

    def get_render_offset(self):
        """
        Calcula um deslocamento aleatório para a tela, criando o efeito de tremor.
        Este valor deve ser adicionado à posição de todos os objetos renderizados.
        """
        if self.shake_magnitude > 0:
            offset_x = random.randint(-self.shake_magnitude, self.shake_magnitude)
            offset_y = random.randint(-self.shake_magnitude, self.shake_magnitude)
            return (offset_x, offset_y)
            
        return (0, 0)

    def create_particles(self, position, count, p_type='explosion'):
        """Cria múltiplas partículas de um tipo específico em uma dada posição."""
        for _ in range(count):
            particle = Particle(position, p_type=p_type)
            self.state.all_sprites.add(particle)
            self.state.particles.add(particle)

    def create_thrust_particles(self):
        """Cria as partículas do rastro de propulsão da nave."""
        ship = self.state.ship
        
        # Calcula a direção oposta à frente da nave para o rastro.
        thrust_direction = pygame.math.Vector2(0, 1).rotate(-ship.angle)
        
        # Calcula a posição inicial das partículas, na "traseira" da nave.
        offset = thrust_direction * (ship.rect.height / 2)
        position = ship.position + offset
        
        # Cria um pequeno número de partículas a cada frame para um rastro contínuo.
        for _ in range(4):
            particle = Particle(
                position, 
                p_type='thrust', 
                initial_velocity_vector=ship.velocity,  # Passa a inércia da nave
                thrust_direction=thrust_direction       # Passa a direção do empurrão
            )
            self.state.all_sprites.add(particle)
            self.state.particles.add(particle)