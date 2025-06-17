import pygame
import random
from .. import settings

class Particle(pygame.sprite.Sprite):
    """
    Partícula genérica para criar diversos efeitos visuais, como explosões,
    rastros de propulsor, brilhos, etc.
    """
    def __init__(self, position, p_type='explosion', initial_velocity_vector=None, thrust_direction=None):
        super().__init__()
        
        self.p_type = p_type
        
        # --- Configuração baseada no tipo de partícula ---
        
        # Partícula de brilho para Power-ups
        if self.p_type == 'powerup_glow':
            self.start_radius = random.randint(8, 12)
            self.radius = self.start_radius
            self.color = random.choice([(255, 255, 0), (255, 220, 50), (255, 255, 100)])
            self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * 0.5
            self.start_lifetime = random.randint(300, 500)
            self.lifetime_countdown = self.start_lifetime
        
        # Partícula para o rastro do propulsor da nave
        elif self.p_type == 'thrust':
            self.start_radius = random.randint(3, 6) 
            self.radius = self.start_radius
            self.start_color = random.choice([(255, 255, 220), (255, 250, 200), (255, 200, 150)])
            self.end_color = random.choice([(255, 60, 0), (200, 20, 0), (240, 90, 40)])
            self.color = self.start_color

            ship_momentum = initial_velocity_vector if initial_velocity_vector is not None else pygame.math.Vector2()
            push_speed = random.uniform(1.5, 4.0) 
            cone_angle = random.uniform(-10, 10) 
            self.start_lifetime = random.randint(400, 700)
            self.lifetime_countdown = self.start_lifetime
            
            push_vector = thrust_direction.rotate(cone_angle) * push_speed
            self.velocity = ship_momentum + push_vector
        
        # Partícula para a explosão do UFO (verde)
        elif self.p_type == 'ufo_explosion':
            self.radius = random.randint(2, 5)
            self.color = random.choice([(0, 255, 0), (100, 255, 100), (150, 255, 150)])
            self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(1, 5)
            self.lifetime_countdown = random.randint(400, 900)
            self.start_lifetime = self.lifetime_countdown
            
        # Partícula de explosão padrão (cinza/branco)
        else: # 'explosion'
            self.radius = random.randint(2, 5)
            self.color = random.choice([(180, 180, 180), (255, 255, 255), (200, 200, 200)])
            self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(1, 4)
            self.lifetime_countdown = random.randint(300, 800)
            self.start_lifetime = self.lifetime_countdown

        # --- Criação da imagem da partícula (um círculo) ---
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=position)
        self.position = pygame.math.Vector2(position)

    def update(self, dt, *args, **kwargs):
        """Atualiza a posição, aparência e tempo de vida da partícula."""
        life_percent = max(0, self.lifetime_countdown / self.start_lifetime)

        # Efeitos específicos para cada tipo de partícula
        if self.p_type == 'powerup_glow':
            # Apenas desaparece (fade out)
            self.image.set_alpha(int(255 * life_percent))
        
        elif self.p_type == 'thrust':
            # Diminui de tamanho e muda de cor (de amarelo para vermelho)
            current_radius = int(self.start_radius * life_percent)
            if current_radius < 1: self.kill(); return
            
            # Interpolação linear de cor
            r = self.start_color[0] + (self.end_color[0] - self.start_color[0]) * (1 - life_percent)
            g = self.start_color[1] + (self.end_color[1] - self.start_color[1]) * (1 - life_percent)
            b = self.start_color[2] + (self.end_color[2] - self.start_color[2]) * (1 - life_percent)
            
            # Recria a imagem com o novo raio e cor
            center = self.rect.center
            self.image = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (r, g, b), (current_radius, current_radius), current_radius)
            self.rect = self.image.get_rect(center=center)

        # Atualiza a posição da partícula
        self.position += self.velocity * (dt / (1000.0 / settings.FPS))
        self.rect.center = self.position
        
        # Decrementa o tempo de vida e se destrói se acabar
        self.lifetime_countdown -= dt
        if self.lifetime_countdown <= 0:
            self.kill()