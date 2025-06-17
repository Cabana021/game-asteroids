import pygame
import math
from src import settings
from src.utils.enums import GameState
from src.utils.background import Starfield

class GameOverScreen:
    """
    Gerencia a tela de Fim de Jogo. Anima a contagem da pontuação,
    exibe o recorde e oferece opções para jogar novamente ou voltar ao menu.
    """
    def __init__(self, screen, clock, assets, final_score, highscore, is_new_highscore, app):
        self.screen = screen
        self.clock = clock
        self.assets = assets
        self.app = app
        self.running = True
        
        # Dados da partida encerrada
        self.text_renderer = self.assets['text_renderer']
        self.final_score = final_score if final_score is not None else 0
        self.highscore = highscore
        self.is_new_highscore = is_new_highscore
        
        # Variáveis de estado e animação da tela
        self.displayed_score = 0
        self.score_ticking_done = False
        self.pulse_angle = 0
        self.selected_button_index = 0
        self.background = Starfield()
        
        # Toca o som de Game Over
        if self.app.sfx_on:
            self.assets['game_over_sound'].play()

    def handle_event(self, event):
        """Processa a entrada do jogador, mas apenas após a animação da pontuação."""
        if self.app.transition.is_active(): return
        
        if self.score_ticking_done and event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_DOWN, pygame.K_UP]:
                if self.app.sfx_on: self.assets['ui_nav_sound'].play()
                self.selected_button_index = 1 - self.selected_button_index
            elif event.key == pygame.K_RETURN:
                if self.app.sfx_on: self.assets['ui_confirm_sound'].play()
                
                if self.selected_button_index == 0: # Jogar Novamente
                    self.next_screen = GameState.RESTART
                else: # Voltar ao Menu
                    self.next_screen = GameState.MENU
                
                self.app.transition.start_fade_out()

    def update(self):
        """Atualiza as animações da tela, incluindo o 'ticker' da pontuação."""
        if not self.app.transition.is_active():
            self.pulse_angle += 0.08
            
            # Lógica da animação de contagem de pontos
            if not self.score_ticking_done:
                # O incremento é proporcional à pontuação para que a contagem não demore demais.
                increment = max(1, int(self.final_score / 150)) if self.final_score > 0 else 1
                if self.displayed_score < self.final_score:
                    self.displayed_score = min(self.final_score, self.displayed_score + increment)
                    # Toca um som de "tick" periodicamente durante a contagem.
                    if self.displayed_score % (increment * 5) < increment and not pygame.mixer.Channel(2).get_busy():
                        if self.app.sfx_on: pygame.mixer.Channel(2).play(self.assets['player_gunshot_sound'])
                else:
                    # Finaliza a contagem
                    self.displayed_score = self.final_score
                    self.score_ticking_done = True
                    if self.app.sfx_on: self.assets['explosion_sound'].play() # Som de "conclusão"
                    
        self.background.update_menu_scroll()
        self.app.transition.update()
        if self.app.transition.is_faded_out(): self.running = False

    def draw(self):
        """Desenha todos os elementos da tela de Game Over."""
        self.screen.fill((10, 10, 25))
        self.background.draw(self.screen)
        
        # Título "GAME OVER" com efeito de pulso vermelho.
        pulse = (math.sin(self.pulse_angle) + 1) / 2
        red_brightness = 180 + int(pulse * 75)
        self.text_renderer.draw(self.screen, "GAME OVER", 65, (red_brightness, 20, 20), settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT * 0.25)
        
        # Desenha a pontuação final (que estará sendo animada).
        self.text_renderer.draw(self.screen, f"SCORE FINAL: {self.displayed_score}", 42, (255, 255, 255), settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT * 0.45)
        
        # O resto das informações (recorde, botões) só aparece após a contagem.
        if self.score_ticking_done:
            y_pos_record = settings.SCREEN_HEIGHT * 0.58
            self.text_renderer.draw(self.screen, f"RECORDE: {self.highscore}", 28, (255, 215, 0), settings.SCREEN_WIDTH / 2, y_pos_record)

            # Exibe uma mensagem especial se um novo recorde foi alcançado.
            if self.is_new_highscore:
                y_pos_new_record_text = settings.SCREEN_HEIGHT * 0.50
                highlight_brightness = 200 + int(pulse * 55)
                color = (highlight_brightness, highlight_brightness, 0)
                self.text_renderer.draw(self.screen, "NOVO RECORDE!", 24, color, settings.SCREEN_WIDTH / 2, y_pos_new_record_text)

            # Desenho dos botões de opção.
            button_texts = ["Jogar Novamente", "Voltar ao Menu"]
            for i, text in enumerate(button_texts):
                y_pos_button = settings.SCREEN_HEIGHT * 0.75 + i * 70
                if i == self.selected_button_index:
                    color = (255, 255, 0)
                    text_rect = self.text_renderer.draw(self.screen, text, 28, color, settings.SCREEN_WIDTH/2, y_pos_button)
                    self.text_renderer.draw(self.screen, ">", 28, color, text_rect.left - 25, y_pos_button)
                else:
                    self.text_renderer.draw(self.screen, text, 28, (220, 220, 220), settings.SCREEN_WIDTH/2, y_pos_button)
        else:
            # Exibe uma mensagem enquanto a pontuação está sendo contada.
            self.text_renderer.draw(self.screen, "Calculando pontuação...", 20, (200, 200, 200), settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT * 0.75)

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
        return self.next_screen, self.final_score