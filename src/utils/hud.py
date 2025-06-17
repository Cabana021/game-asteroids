import pygame
import math
from src import settings

class HUD:
    """
    Head-Up Display: Gerencia a renderização de todas as informações
    na tela durante o gameplay, como pontuação, vidas e alertas.
    """
    def __init__(self, assets):
        # Armazena referências para os assets necessários.
        self.text_renderer = assets['text_renderer']
        
        # Configura a imagem de coração para representar as vidas.
        self.heart_image = pygame.transform.scale(assets['heart_image'], (28, 28))
        self.heart_width = self.heart_image.get_width()
        self.padding = 8  # Espaçamento entre os corações

        # Variável para animar o alerta de UFO.
        self.pulse_angle = 0

    def draw(self, screen, score, lives, ufo_warning):
        """
        Desenha todos os elementos do HUD na tela.
        
        Args:
            screen: A superfície principal para desenhar.
            score (int): A pontuação atual do jogador.
            lives (int): O número de vidas restantes.
            ufo_warning (bool): True se um alerta de UFO deve ser exibido.
        """
        
        # --- Desenha a Pontuação ---
        score_text = f"SCORE: {score}"
        self.text_renderer.draw(screen, score_text, 24, (255, 255, 255), 20, 15, align="topleft")

        # --- Desenha os Ícones de Vida ---
        # Itera sobre o número de vidas e desenha um coração para cada uma.
        for i in range(lives):
            x_pos = 20 + (i * (self.heart_width + self.padding))
            y_pos = 45 
            screen.blit(self.heart_image, (x_pos, y_pos))
        
        # --- Desenha o Alerta de UFO (se necessário) ---
        if ufo_warning:
            # Animação de pulso para o texto de alerta.
            self.pulse_angle += 0.1
            # Usa uma função seno para criar uma oscilação suave entre 0 e 1.
            pulse = (math.sin(self.pulse_angle) + 1) / 2 
            # Mapeia o pulso para uma variação na cor vermelha do texto.
            red_value = 150 + int(pulse * 105) 
            warning_color = (red_value, 50, 50)
            
            # Desenha o texto de alerta centralizado no topo da tela.
            self.text_renderer.draw(
                screen, 
                "WARNING: UFO DETECTED", 
                24, 
                warning_color,
                settings.SCREEN_WIDTH / 2, 
                20
            )