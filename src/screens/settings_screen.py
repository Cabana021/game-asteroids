import pygame
import math
from src import settings
from src.utils.enums import GameState
from src.utils.background import Starfield

class SettingsScreen:
    """
    Gerencia a tela de Configurações, onde o jogador pode ativar ou desativar
    a música, os efeitos sonoros e outros recursos.
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
        self.selected_button_index = 0
        self.pulse_angle = 0
        
        # A lista de textos dos botões é dinâmica e será atualizada no método update().
        self.button_texts = []

    def handle_event(self, event):
        """Processa a entrada do jogador para navegar e alterar as configurações."""
        if self.app.transition.is_active(): return

        if event.type == pygame.KEYDOWN:
            # Navegação
            if event.key in [pygame.K_DOWN, pygame.K_UP]:
                if self.app.sfx_on: self.assets['ui_nav_sound'].play()
                num_buttons = len(self.button_texts)
                if event.key == pygame.K_DOWN:
                    self.selected_button_index = (self.selected_button_index + 1) % num_buttons
                else:
                    self.selected_button_index = (self.selected_button_index - 1 + num_buttons) % num_buttons
            
            # Alterar configuração ou voltar
            elif event.key == pygame.K_RETURN:
                if self.app.sfx_on: self.assets['ui_confirm_sound'].play()
                
                if self.selected_button_index == 0:
                    self.app.toggle_music()
                elif self.selected_button_index == 1:
                    self.app.toggle_sfx()
                elif self.selected_button_index == 2:
                    self.app.toggle_screen_shake()
                elif self.selected_button_index == 3: # Voltar
                    self.next_screen = GameState.MENU
                    self.app.transition.start_fade_out()
            
            # Voltar com ESC
            elif event.key == pygame.K_ESCAPE:
                if self.app.sfx_on: self.assets['ui_nav_sound'].play()
                self.next_screen = GameState.MENU
                self.app.transition.start_fade_out()

    def update(self):
        """Atualiza animações, transições e o texto dinâmico dos botões."""
        if not self.app.transition.is_active():
            self.pulse_angle += 0.05
        
        self.background.update_menu_scroll()
        self.app.transition.update()

        # Atualiza os textos dos botões para refletir o estado atual das configurações.
        self.button_texts = [
            f"Música: {'ON' if self.app.music_on else 'OFF'}",
            f"Efeitos Sonoros: {'ON' if self.app.sfx_on else 'OFF'}",
            f"Screen Shake: {'ON' if self.app.screen_shake_on else 'OFF'}",
            "Voltar"
        ]

        if self.app.transition.is_faded_out():
            self.running = False

    def draw(self):
        """Desenha todos os elementos da tela de configurações."""
        self.screen.fill((10, 10, 25))
        self.background.draw(self.screen)
        
        # Título
        self.text_renderer.draw(self.screen, "Configuração", 65, (255, 255, 255), settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT * 0.15)
        
        # Botões
        for i, text in enumerate(self.button_texts):
            y_pos = settings.SCREEN_HEIGHT * 0.35 + i * 80 # Espaçamento ajustado
            if i == self.selected_button_index:
                pulse_highlight = (math.sin(self.pulse_angle * 0.8 + i) + 1) / 2
                highlight_brightness = 200 + int(pulse_highlight * 55)
                color = (highlight_brightness, highlight_brightness, 0)
                text_rect = self.text_renderer.draw(self.screen, text, 32, color, settings.SCREEN_WIDTH/2, y_pos)
                self.text_renderer.draw(self.screen, ">", 32, color, text_rect.left - 30, y_pos)
            else:
                self.text_renderer.draw(self.screen, text, 32, (220, 220, 220), settings.SCREEN_WIDTH/2, y_pos)
        
        self.app.transition.draw()

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