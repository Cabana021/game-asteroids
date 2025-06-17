import pygame
import math
from .. import settings

class BaseBullet(pygame.sprite.Sprite):
    """
    Classe base para todos os projéteis no jogo.
    Contém a lógica de movimento comum e autodestruição fora da tela.
    """
    def __init__(self, position, velocity, image):
        super().__init__()
        
        self.image = image
        self.position = pygame.math.Vector2(position)
        self.velocity = velocity
        
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, dt, *args, **kwargs):
        """Atualiza a posição do projétil e verifica se ele saiu da tela."""
        # Movimento consistente baseado em Delta Time.
        self.position += self.velocity * (dt / (1000.0 / settings.FPS))
        self.rect.center = self.position
        
        # Remove o projétil se ele sair completamente da tela (com uma margem).
        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.inflate(50, 50).colliderect(self.rect):
            self.kill()

class PlayerBullet(BaseBullet):
    """
    Projétil disparado pelo jogador. Herda de BaseBullet e adiciona
    um tempo de vida limitado.
    """
    def __init__(self, position, direction, image):
        # Calcula a velocidade com base na direção e velocidade padrão.
        velocity = direction * settings.BULLET_SPEED
        
        # Rotaciona a imagem do projétil para alinhar com a sua direção.
        angle = math.degrees(math.atan2(-direction.y, direction.x))
        rotated_image = pygame.transform.rotate(image, angle)
        
        # Chama o construtor da classe base.
        super().__init__(position, velocity, rotated_image)
        
        # Define o tempo de vida do projétil.
        self.lifetime_countdown = settings.BULLET_LIFETIME

    def update(self, dt, *args, **kwargs):
        """Atualiza o movimento e o tempo de vida do projétil."""
        super().update(dt) # Chama o update da classe base (movimento e verificação de tela).
        
        # Reduz o tempo de vida e se destrói se o tempo acabar.
        self.lifetime_countdown -= dt
        if self.lifetime_countdown <= 0:
            self.kill()

class EnemyBullet(BaseBullet):
    """
    Projétil disparado pelos inimigos (UFOs).
    Herda de BaseBullet e tem sua própria velocidade.
    """
    def __init__(self, position, direction, image):
        velocity = direction * settings.ENEMY_BULLET_SPEED
        
        angle = math.degrees(math.atan2(-direction.y, direction.x))
        rotated_image = pygame.transform.rotate(image, angle)

        super().__init__(position, velocity, rotated_image)