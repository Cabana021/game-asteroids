import pygame
import random
from .. import settings

class Asteroid(pygame.sprite.Sprite):
    """
    Representa um asteroide no jogo. Pode ter diferentes tamanhos,
    velocidades e rotações.
    """
    def __init__(self, size, position, image):
        super().__init__()
        
        # --- Atributos ---
        self.size = size
        self.original_image = image  # Armazena a imagem base para rotações
        self.radius = settings.ASTEROID_SIZES.get(self.size, 15) # Obtém o raio do asteroide com base no seu tamanho
        
        # --- Configuração de Sprite ---
        # Redimensiona a imagem para o tamanho correto e a salva como 'original_image' para otimizar.
        self.image = pygame.transform.scale(self.original_image, (self.radius * 2, self.radius * 2))
        self.original_image = self.image 
        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image) # A máscara inicial
        
        # --- Física e Movimento ---
        self.position = pygame.math.Vector2(position) # Posição precisa usando vetores
        speed = random.uniform(settings.ASTEROID_MIN_SPEED, settings.ASTEROID_MAX_SPEED)
        self.velocity = pygame.math.Vector2(speed, 0).rotate(random.uniform(0, 360)) # Direção e velocidade aleatórias
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2) # Velocidade de rotação aleatória
        
    def update(self, dt, *args, **kwargs):
        """Atualiza a posição e rotação do asteroide a cada frame."""
        # Move o asteroide com base na sua velocidade e delta time.
        self.position += self.velocity * (dt / (1000.0 / settings.FPS))
        
        # Atualiza a rotação.
        self.rotation = (self.rotation + self.rotation_speed) % 360
        
        # Rotaciona a imagem e atualiza o rect e a mask a cada frame para colisões precisas.
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)
        
        # Garante que o asteroide reapareça do outro lado da tela se sair.
        self._wrap_around_screen()

    def _wrap_around_screen(self):
        """Implementa a lógica de "wrap-around" para o asteroide."""
        # Usa a posição do vetor para precisão, em vez do rect.
        if self.position.x > settings.SCREEN_WIDTH + self.radius: self.position.x = -self.radius
        if self.position.x < -self.radius: self.position.x = settings.SCREEN_WIDTH + self.radius
        if self.position.y > settings.SCREEN_HEIGHT + self.radius: self.position.y = -self.radius
        if self.position.y < -self.radius: self.position.y = settings.SCREEN_HEIGHT + self.radius