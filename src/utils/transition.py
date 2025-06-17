import pygame
from src import settings

class FadeTransition:
    """
    Gerencia um efeito de transição de fade (escurecer/clarear) entre telas.
    """
    def __init__(self, screen):
        self.screen = screen
        
        # Cria uma superfície do tamanho da tela para desenhar o fade.
        self.fade_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.fade_surface.fill((0, 0, 0))  # Cor do fade (preto)
        
        # Variáveis de estado da transição
        self.alpha = 0          # Nível de transparência (0=transparente, 255=opaco)
        self.speed = 10         # Velocidade com que o alpha muda
        self.fading_out = False # True se a tela está escurecendo
        self.fading_in = False  # True se a tela está clareando

    def start_fade_out(self):
        """Inicia o processo de fade-out (tela escurece)."""
        # Só inicia uma nova transição se nenhuma outra estiver ativa.
        if not self.fading_out and not self.fading_in:
            self.fading_out = True
            self.alpha = 0  # Começa totalmente transparente

    def start_fade_in(self):
        """Inicia o processo de fade-in (tela clareia)."""
        if not self.fading_out and not self.fading_in:
            self.fading_in = True
            self.alpha = 255 # Começa totalmente opaco

    def update(self):
        """Atualiza o valor alpha para animar o efeito de fade."""
        if self.fading_out:
            self.alpha += self.speed
            if self.alpha >= 255:
                self.alpha = 255
                self.fading_out = False # Terminou o fade-out
        elif self.fading_in:
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.alpha = 0
                self.fading_in = False # Terminou o fade-in

    def draw(self):
        """Desenha a superfície de fade na tela, se a transição não for totalmente transparente."""
        if self.alpha > 0:
            self.fade_surface.set_alpha(self.alpha)
            self.screen.blit(self.fade_surface, (0, 0))

    def is_faded_out(self):
        """Verifica se a tela está completamente escura (fade-out concluído)."""
        return self.alpha == 255 and not self.fading_out

    def is_active(self):
        """Verifica se alguma transição (fade-in ou fade-out) está em andamento."""
        return self.fading_in or self.fading_out