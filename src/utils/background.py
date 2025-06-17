import pygame
import random
from src import settings

class Starfield:
    """
    Gerencia um fundo de estrelas com múltiplas camadas para criar um efeito de profundidade.
    Suporta dois modos de movimento:
    1. Rolagem vertical constante (para menus).
    2. Efeito de paralaxe 2D que reage a um vetor de velocidade (para o gameplay).
    """
    def __init__(self):
        # Cada lista interna representa uma camada de estrelas.
        self.star_layers = [[], [], []]
        
        # Fatores que determinam a velocidade de cada camada (camadas mais próximas se movem mais rápido).
        self.parallax_factors = [0.1, 0.3, 0.5]
        
        self._create_stars()

    def _create_stars(self):
        """Preenche as camadas com posições e quantidades de estrelas aleatórias."""
        self.star_layers = [[], [], []]
        # Camada de fundo (mais lenta, menos estrelas)
        for _ in range(50):
            self.star_layers[0].append([random.randrange(settings.SCREEN_WIDTH), random.randrange(settings.SCREEN_HEIGHT)])
        # Camada do meio
        for _ in range(100):
            self.star_layers[1].append([random.randrange(settings.SCREEN_WIDTH), random.randrange(settings.SCREEN_HEIGHT)])
        # Camada da frente (mais rápida, mais estrelas)
        for _ in range(150):
            self.star_layers[2].append([random.randrange(settings.SCREEN_WIDTH), random.randrange(settings.SCREEN_HEIGHT)])

    def update_menu_scroll(self):
        """Atualiza as estrelas com uma rolagem vertical simples, ideal para menus."""
        for i, layer in enumerate(self.star_layers):
            speed_factor = self.parallax_factors[i]
            for star in layer:
                # Move a estrela para baixo com base no fator de paralaxe.
                star[1] += speed_factor
                # Se a estrela sair da tela por baixo, reposiciona-a no topo com um novo x.
                if star[1] > settings.SCREEN_HEIGHT:
                    star[0] = random.randrange(settings.SCREEN_WIDTH)
                    star[1] = 0

    def update_game_parallax(self, velocity: pygame.math.Vector2):
        """Atualiza a posição das estrelas com base no vetor de velocidade do jogador."""
        for i, layer in enumerate(self.star_layers):
            # Calcula o movimento da camada, na direção oposta à da nave.
            movement = -velocity * self.parallax_factors[i]
            for star in layer:
                star[0] += movement.x
                star[1] += movement.y

                # Lógica de "wrapping": se uma estrela sai de um lado da tela, ela reaparece no oposto.
                if star[0] > settings.SCREEN_WIDTH: star[0] = 0
                if star[0] < 0: star[0] = settings.SCREEN_WIDTH
                if star[1] > settings.SCREEN_HEIGHT: star[1] = 0
                if star[1] < 0: star[1] = settings.SCREEN_HEIGHT
    
    def draw(self, screen):
        """Desenha todas as camadas de estrelas na tela, cada uma com sua cor e tamanho."""
        # Define a aparência de cada camada (cor e tamanho).
        colors = [(80, 80, 80), (150, 150, 150), (255, 255, 255)]
        sizes = [1, 1, 2]
        
        for i, layer in enumerate(self.star_layers):
            color = colors[i]
            size = sizes[i]
            for star in layer:
                pygame.draw.circle(screen, color, (int(star[0]), int(star[1])), size)