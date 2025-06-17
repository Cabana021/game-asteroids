import pygame
import math
from src import settings
from src.utils.enums import GameState
from src.utils.background import Starfield

class TutorialScreen:
    """
    Gerencia a tela de Tutorial, que exibe os controles básicos do jogo
    de forma visualmente agradável.
    """
    def __init__(self, screen, clock, assets, app):
        self.screen = screen
        self.clock = clock
        self.assets = assets
        self.app = app
        self.running = True
        
        # Componentes e estado da tela
        self.text_renderer = self.assets['text_renderer']
        self.background = Starfield()
        self.pulse_angle = 0

    def handle_event(self, event):
        """Processa a entrada para voltar ao menu."""
        if self.app.transition.is_active(): return

        # Qualquer tecla de confirmação/escape retorna ao menu.
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
            if self.app.sfx_on: self.assets['ui_confirm_sound'].play()
            self.next_screen = GameState.MENU
            self.app.transition.start_fade_out()

    def update(self):
        """Atualiza as animações e transições da tela."""
        if not self.app.transition.is_active():
            self.pulse_angle += 0.05
        
        self.background.update_menu_scroll()
        self.app.transition.update()

        if self.app.transition.is_faded_out():
            self.running = False

    def draw(self):
        """Desenha todos os elementos da tela de tutorial."""
        self.screen.fill((10, 10, 25))
        self.background.draw(self.screen)
        
        # Título
        pulse = (math.sin(self.pulse_angle * 1.5) + 1) / 2
        brightness = 220 + int(pulse * 35)
        self.text_renderer.draw(self.screen, "Como Jogar", 65, (brightness, brightness, brightness), settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT*0.15)
        
        # Blocos de instrução
        self._draw_instruction_block(settings.SCREEN_HEIGHT*0.35, ['left', 'right'], "Girar a nave")
        self._draw_instruction_block(settings.SCREEN_HEIGHT*0.55, ['up'], "Acelerar")
        self._draw_instruction_block(settings.SCREEN_HEIGHT*0.75, ['space'], "Atirar")
        
        # Texto de ajuda para voltar
        pulse_return = (math.sin(self.pulse_angle) + 1) / 2
        brightness_return = 200 + int(pulse_return * 55)
        self.text_renderer.draw(self.screen, "Pressione ENTER ou ESC para voltar", 20, (brightness_return, brightness_return, brightness_return), settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT*0.92)

        # Camada de transição
        self.app.transition.draw()

    def _draw_instruction_block(self, y_pos, keys, text):
        """Desenha um painel contendo imagens de teclas e um texto de instrução."""
        # Mapeia nomes de teclas para as imagens carregadas.
        images = {'up': self.assets['arrowup'], 'left': self.assets['arrowleft'], 'right': self.assets['arrowright'], 'space': self.assets['space_bar']}
        
        # --- Cálculos para centralizar o painel ---
        key_gap, text_gap = 10, 40
        total_keys_width = sum(images[key].get_width() for key in keys) + key_gap * (len(keys) - 1)
        key_height = images[keys[0]].get_height()
        font = self.text_renderer._get_font(32)
        text_width = font.size(text)[0]
        total_content_width = total_keys_width + text_gap + text_width
        panel_padding = 40
        
        # --- Desenho do Painel ---
        panel_width = total_content_width + panel_padding * 2
        panel_height = key_height + panel_padding
        panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        panel_rect.center = (settings.SCREEN_WIDTH/2, y_pos)
        self._draw_tech_panel(panel_rect)
        
        # --- Desenho do Conteúdo (Teclas e Texto) ---
        start_x = panel_rect.left + panel_padding
        current_x = start_x
        for key_name in keys:
            image = images[key_name]
            self.screen.blit(image, (current_x, y_pos - key_height/2))
            current_x += image.get_width() + key_gap
        self.text_renderer.draw(self.screen, text, 32, (255, 255, 100), current_x - key_gap + text_gap, y_pos, align="left")

    def _draw_tech_panel(self, rect):
        """Desenha um painel com estilo futurista e cantos chanfrados."""
        panel_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        panel_surface.fill((15, 25, 40, 180)) # Cor de fundo semi-transparente
        # Pontos para desenhar um polígono como borda, criando cantos chanfrados.
        points = [(15, 0), (rect.width - 15, 0), (rect.width, 15), (rect.width, rect.height - 15), (rect.width-15, rect.height), (15, rect.height), (0, rect.height - 15), (0, 15)]
        pygame.draw.polygon(panel_surface, (100, 150, 255, 200), points, 3)
        self.screen.blit(panel_surface, rect.topleft)

    def run(self):
        """O loop principal que executa esta tela."""
        self.running = True
        self.next_screen = GameState.MENU
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.next_screen = GameState.QUIT
                    self.app.transition.start_fade_out()
                self.handle_event(event)
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        return self.next_screen, None