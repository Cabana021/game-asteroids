import pygame
import math
from src import settings
from src.utils.enums import GameState

class PauseScreen:
    """
    Gerencia a tela de Pausa, que é exibida sobre um 'snapshot' congelado do jogo.
    Oferece opções para continuar, reiniciar ou sair para o menu.
    """
    def __init__(self, screen, clock, assets, snapshot, app):
        self.screen = screen
        self.clock = clock
        self.assets = assets
        self.app = app
        self.running = True
        
        # 'snapshot' é uma imagem congelada da tela de jogo no momento da pausa.
        self.snapshot = snapshot
        
        # Componentes e estado da tela
        self.text_renderer = self.assets['text_renderer']
        self.selected_button_index = 0
        self.pulse_angle = 0

    def handle_event(self, event):
        """Processa a entrada do jogador no menu de pausa."""
        if self.app.transition.is_active(): return
        
        if event.type == pygame.KEYDOWN:
            # Atalho ESC para continuar o jogo.
            if event.key == pygame.K_ESCAPE:
                if self.app.sfx_on: self.assets['ui_nav_sound'].play()
                self.next_screen = GameState.RESUME
                self.app.transition.start_fade_out()
                
            # Navegação pelos botões.
            elif event.key in [pygame.K_DOWN, pygame.K_UP]:
                if event.key == pygame.K_DOWN: self.selected_button_index = (self.selected_button_index + 1) % 3
                else: self.selected_button_index = (self.selected_button_index - 1 + 3) % 3
                if self.app.sfx_on: self.assets['ui_nav_sound'].play()
                
            # Seleção de uma opção.
            elif event.key == pygame.K_RETURN:
                if self.app.sfx_on: self.assets['ui_confirm_sound'].play()
                if self.selected_button_index == 0: self.next_screen = GameState.RESUME
                elif self.selected_button_index == 1: self.next_screen = GameState.RESTART
                elif self.selected_button_index == 2: self.next_screen = GameState.MENU
                self.app.transition.start_fade_out()

    def update(self):
        """Atualiza as animações e transições da tela."""
        if not self.app.transition.is_active():
            self.pulse_angle += 0.05

        self.app.transition.update()
        if self.app.transition.is_faded_out():
            self.running = False

    def draw(self):
        """Desenha a tela de pausa sobre o snapshot do jogo."""
        # 1. Desenha a imagem congelada do jogo como fundo.
        self.screen.blit(self.snapshot, (0, 0))
        
        # 2. Desenha um overlay semi-transparente para escurecer o fundo.
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 10, 180)); self.screen.blit(overlay, (0, 0))
        
        # 3. Desenha o título "PAUSADO".
        pulse = (math.sin(self.pulse_angle * 1.5) + 1) / 2
        brightness = 220 + int(pulse * 35)
        self.text_renderer.draw(self.screen, "PAUSADO", 65, (brightness, brightness, brightness), settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT * 0.25)
        
        # 4. Desenha os botões de opção.
        button_texts = ["Continuar", "Reiniciar", "Sair para o Menu"]
        for i, text in enumerate(button_texts):
            y_pos = settings.SCREEN_HEIGHT * 0.45 + i * 90
            if i == self.selected_button_index:
                pulse_highlight = (math.sin(self.pulse_angle * 0.8 + 1) + 1) / 2
                highlight_brightness = 200 + int(pulse_highlight * 55)
                color = (highlight_brightness, highlight_brightness, 0)
                text_rect = self.text_renderer.draw(self.screen, text, 32, color, settings.SCREEN_WIDTH/2, y_pos)
                self.text_renderer.draw(self.screen, ">", 32, color, text_rect.left - 30, y_pos)
            else:
                self.text_renderer.draw(self.screen, text, 32, (255, 255, 255), settings.SCREEN_WIDTH/2, y_pos)
        
        # 5. Desenha a transição de fade por cima de tudo.
        self.app.transition.draw()

    def run(self):
        """O loop principal que executa esta tela."""
        self.running = True
        self.next_screen = GameState.RESUME # Padrão é continuar o jogo
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