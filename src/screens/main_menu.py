import pygame
import math
from src import settings
from src.utils.enums import GameState
from src.utils.background import Starfield

class MainMenuScreen:
    """
    Gerencia o Menu Principal do jogo, oferecendo opções para iniciar o jogo,
    ver o tutorial, acessar configurações ou sair.
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
        
        # Variáveis de estado do menu
        self.selected_button_index = 0
        self.show_exit_confirmation = False
        self.selected_exit_button_index = 1 # 0=Sim, 1=Não

    def handle_event(self, event):
        """Processa a entrada do jogador, delegando para o menu apropriado (principal ou confirmação de saída)."""
        if self.app.transition.is_active(): return

        if event.type == pygame.KEYDOWN:
            if self.show_exit_confirmation:
                self._handle_exit_confirmation_input(event)
            else:
                self._handle_main_menu_input(event)

    def _handle_main_menu_input(self, event):
        """Lida com a entrada do jogador no menu principal."""
        if event.key in [pygame.K_DOWN, pygame.K_UP]:
            if self.app.sfx_on: self.assets['ui_nav_sound'].play()
            if event.key == pygame.K_DOWN: self.selected_button_index = (self.selected_button_index + 1) % 4
            else: self.selected_button_index = (self.selected_button_index - 1 + 4) % 4
        elif event.key == pygame.K_RETURN:
            if self.app.sfx_on: self.assets['ui_confirm_sound'].play()
            
            # Executa a ação correspondente ao botão selecionado.
            if self.selected_button_index == 0: # Jogar
                self.next_screen = GameState.DIFFICULTY_SELECT
                self.app.transition.start_fade_out()
            elif self.selected_button_index == 1: # Tutorial
                self.next_screen = GameState.TUTORIAL
                self.app.transition.start_fade_out()
            elif self.selected_button_index == 2: # Configuração
                self.next_screen = GameState.SETTINGS
                self.app.transition.start_fade_out()
            elif self.selected_button_index == 3: # Sair
                self.show_exit_confirmation = True
    
    def _handle_exit_confirmation_input(self, event):
        """Lida com a entrada do jogador na caixa de diálogo de confirmação de saída."""
        if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            if self.app.sfx_on: self.assets['ui_nav_sound'].play()
            self.selected_exit_button_index = 1 - self.selected_exit_button_index
        elif event.key == pygame.K_RETURN:
            if self.app.sfx_on: self.assets['ui_confirm_sound'].play()
            if self.selected_exit_button_index == 0: # Sim
                self.next_screen = GameState.QUIT
                self.app.transition.start_fade_out()
            else: # Não
                self.show_exit_confirmation = False
        elif event.key == pygame.K_ESCAPE:
            self.show_exit_confirmation = False # Cancelar com ESC

    def update(self):
        """Atualiza o estado da tela, como animações e transições."""
        if not self.app.transition.is_active():
            self.pulse_angle += 0.05
        
        self.background.update_menu_scroll()
        self.app.transition.update()

        if self.app.transition.is_faded_out():
            self.running = False

    def draw(self):
        """Desenha a tela, mostrando o menu principal ou a confirmação de saída."""
        self.screen.fill((10, 10, 25))
        self.background.draw(self.screen)
        
        if self.show_exit_confirmation:
            self._draw_exit_confirmation()
        else:
            self._draw_main_menu()
        
        self.app.transition.draw()
    
    def _draw_main_menu(self):
        """Desenha os elementos do menu principal."""
        # Título do jogo com efeito de pulso.
        pulse = (math.sin(self.pulse_angle) + 1) / 2 
        brightness = 200 + int(pulse * 55)
        title_color = (brightness, brightness, brightness)
        self.text_renderer.draw(self.screen, settings.TITLE, 65, title_color, settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT * 0.20)
        
        # Botões do menu
        button_texts = ["Jogar", "Tutorial", "Configuração", "Sair"]
        for i, text in enumerate(button_texts):
            y_pos = settings.SCREEN_HEIGHT * 0.45 + i * 70
            if i == self.selected_button_index:
                pulse_highlight = (math.sin(self.pulse_angle * 0.8 + 1) + 1) / 2
                highlight_brightness = 200 + int(pulse_highlight * 55)
                color = (highlight_brightness, highlight_brightness, 0)
                text_rect = self.text_renderer.draw(self.screen, text, 32, color, settings.SCREEN_WIDTH/2, y_pos)
                self.text_renderer.draw(self.screen, ">", 32, color, text_rect.left - 30, y_pos)
            else:
                self.text_renderer.draw(self.screen, text, 32, (255, 255, 255), settings.SCREEN_WIDTH/2, y_pos)

    def _draw_exit_confirmation(self):
        """Desenha a caixa de diálogo para confirmar a saída do jogo."""
        # Overlay semi-transparente para escurecer o fundo.
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)); self.screen.blit(overlay, (0, 0))
        
        # Caixa de diálogo
        dialog_rect = pygame.Rect(0, 0, 600, 220); dialog_rect.center = (settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2)
        pygame.draw.rect(self.screen, (10, 10, 25), dialog_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), dialog_rect, 2)
        
        # Texto da pergunta
        question_lines = ["Tem certeza que", "quer sair?"]; line_y = dialog_rect.centery - 60
        for line in question_lines: self.text_renderer.draw(self.screen, line, 28, (255,255,255), dialog_rect.centerx, line_y); line_y += 40
        
        # Botões "Sim" e "Não"
        sim_color = (255, 215, 0) if self.selected_exit_button_index == 0 else (255, 255, 255)
        nao_color = (255, 215, 0) if self.selected_exit_button_index == 1 else (255, 255, 255)
        self.text_renderer.draw(self.screen, "Sim", 24, sim_color, dialog_rect.centerx - 80, dialog_rect.centery + 50)
        self.text_renderer.draw(self.screen, "Não", 24, nao_color, dialog_rect.centerx + 80, dialog_rect.centery + 50)

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