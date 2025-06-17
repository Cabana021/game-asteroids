import pygame
import math 
from .. import settings 

class Ship(pygame.sprite.Sprite):
    """
    Representa a nave controlada pelo jogador.
    Gerencia seu movimento, rotação, tiros e estado de invulnerabilidade.
    """
    def __init__(self, image_surface):
        super().__init__()
        
        # --- Configuração de Sprite ---
        self.original_image = image_surface # Imagem base para rotações
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)
        
        # --- Física e Movimento ---
        self.position = pygame.math.Vector2(self.rect.center)
        self.velocity = pygame.math.Vector2(0, 0)
        self.angle = 0.0
        self.accelerating = False 

        # --- Estado da Nave ---
        self.invulnerable = False
        self.invulnerable_countdown = 0
        self.visible = True
        self.blink_countdown = 0

    def update(self, dt, *args, **kwargs):
        """O método principal de atualização, chamado a cada frame."""
        self._get_input()
        self._apply_friction()
        self._move(dt)
        self._wrap_around_screen()
        self._handle_invulnerability(dt)

    def _get_input(self):
        """Verifica as teclas pressionadas para controlar a nave."""
        self.accelerating = False
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]: 
            self._rotate(settings.SHIP_ROTATION_SPEED)
        if keys[pygame.K_RIGHT]: 
            self._rotate(-settings.SHIP_ROTATION_SPEED)
        if keys[pygame.K_UP]: 
            self._accelerate()
            self.accelerating = True

    def _rotate(self, speed):
        """Rotaciona a nave e atualiza sua imagem, rect e máscara."""
        self.angle = (self.angle + speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def _accelerate(self):
        """Aplica uma força de propulsão na direção em que a nave está apontando."""
        thrust = pygame.math.Vector2(0, -settings.SHIP_ACCELERATION).rotate(-self.angle)
        self.velocity += thrust

    def _apply_friction(self):
        """Aplica atrito para desacelerar a nave e limita sua velocidade máxima."""
        # Limita a velocidade máxima.
        if self.velocity.magnitude() > settings.SHIP_MAX_SPEED:
            self.velocity.scale_to_length(settings.SHIP_MAX_SPEED)
            
        # Aplica atrito se a nave estiver se movendo.
        if self.velocity.length() > 0.1:
            self.velocity *= (1 - settings.SHIP_FRICTION)
        else: # Para a nave completamente se a velocidade for muito baixa.
            self.velocity.x = 0; self.velocity.y = 0

    def _move(self, dt):
        """Atualiza a posição da nave com base em sua velocidade."""
        self.position += self.velocity * (dt / (1000.0 / settings.FPS))
        self.rect.center = self.position

    def _wrap_around_screen(self):
        """Faz a nave reaparecer no lado oposto da tela."""
        if self.position.x > settings.SCREEN_WIDTH: self.position.x = 0
        if self.position.x < 0: self.position.x = settings.SCREEN_WIDTH
        if self.position.y > settings.SCREEN_HEIGHT: self.position.y = 0
        if self.position.y < 0: self.position.y = settings.SCREEN_HEIGHT
    
    def _handle_invulnerability(self, dt):
        """Gerencia o estado de invulnerabilidade e o efeito de piscar."""
        if self.invulnerable:
            self.invulnerable_countdown -= dt
            if self.invulnerable_countdown <= 0:
                self.invulnerable = False
                self.visible = True
            else:
                # Efeito de piscar
                self.blink_countdown -= dt
                if self.blink_countdown <= 0:
                    self.blink_countdown = 100 # Intervalo do pisca-pisca
                    self.visible = not self.visible
        else:
            self.visible = True

    def shoot(self, bullet_image):
        """Cria os dados para um novo projétil."""
        direction = pygame.math.Vector2(0, -1).rotate(-self.angle)
        offset = direction * (self.rect.height / 2) # Posição na ponta da nave
        bullet_pos = self.position + offset
        
        return {"pos": bullet_pos, "dir": direction, "img": bullet_image}
    
    def respawn(self):
        """Reseta a nave para sua posição e estado iniciais após ser destruída."""
        self.position = pygame.math.Vector2(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2)
        self.velocity = pygame.math.Vector2(0, 0)
        self.angle = 0.0
        self._rotate(0) # Reseta a rotação da imagem
        
        # Ativa a invulnerabilidade por um curto período.
        self.invulnerable = True
        self.invulnerable_countdown = 2000 # 2 segundos