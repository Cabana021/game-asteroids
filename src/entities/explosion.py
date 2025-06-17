import pygame

class Explosion(pygame.sprite.Sprite):
    """
    Uma animação de explosão que toca uma vez e depois se autodestrói.
    """
    def __init__(self, center, frames):
        super().__init__()
        
        self.frames = frames                # Lista de imagens (frames da animação)
        self.image = self.frames[0]         # A imagem atual é o primeiro frame
        self.rect = self.image.get_rect(center=center)
        
        # --- Controle de Animação ---
        self.frame = 0                      # Índice do frame atual
        self.rate = 75                      # Duração de cada frame em milissegundos
        self.countdown = self.rate          # Contador regressivo para trocar de frame
        
    def update(self, dt, *args, **kwargs):
        """Atualiza a animação da explosão."""
        self.countdown -= dt
        
        # Se o tempo do frame atual acabou, avança para o próximo.
        if self.countdown <= 0:
            self.countdown = self.rate
            self.frame += 1
            
            # Se a animação terminou, o sprite se autodestrói.
            if self.frame == len(self.frames):
                self.kill()
            # Caso contrário, atualiza a imagem para o próximo frame.
            else:
                center = self.rect.center
                self.image = self.frames[self.frame]
                self.rect = self.image.get_rect(center=center)