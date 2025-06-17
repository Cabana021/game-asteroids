import pygame

class TextRenderer:
    """
    Uma classe utilitária para renderizar texto de forma consistente.
    - Gerencia e armazena em cache objetos de fonte para otimização.
    - Desenha texto com uma sombra simples para melhor legibilidade.
    - Suporta múltiplos alinhamentos.
    """
    def __init__(self, font_path):
        self.fonts = {}  # Dicionário para armazenar fontes já carregadas (cache).
        self.font_path = font_path

    def _get_font(self, size):
        """
        Obtém um objeto de fonte do tamanho especificado.
        Se a fonte já foi carregada, a retorna do cache. Caso contrário,
        carrega-a do arquivo, armazena no cache e a retorna.
        """
        if size not in self.fonts:
            self.fonts[size] = pygame.font.Font(self.font_path, size)
        return self.fonts[size]

    def draw(self, screen, text, size, color, x, y, align="center"):
        """
        Desenha texto na tela com uma sombra e alinhamento customizável.
        
        Retorna:
            pygame.Rect: O retângulo do texto principal, útil para detecção de cliques.
        """
        # 1. Obter a fonte e renderizar as superfícies de texto e sombra.
        font = self._get_font(size)
        text_surface = font.render(text, True, color)
        shadow_surface = font.render(text, True, (20, 20, 20))  # Cor escura para a sombra
        
        # 2. Obter os retângulos para posicionamento.
        text_rect = text_surface.get_rect()
        shadow_rect = shadow_surface.get_rect()
        
        # 3. Ajustar a posição do retângulo do texto principal com base no alinhamento.
        if align == "center":
            text_rect.center = (x, y)
        elif align == "topleft":
            text_rect.topleft = (x, y)
        elif align == "topright":
            text_rect.topright = (x, y)
        elif align == "left":
            text_rect.midleft = (x, y)  # Alinha o centro vertical com o 'y' fornecido.
        
        # 4. Posicionar a sombra com um pequeno deslocamento em relação ao texto principal.
        shadow_rect.topleft = (text_rect.left + 3, text_rect.top + 3)

        # 5. Desenhar a sombra primeiro, depois o texto por cima.
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)
        
        return text_rect