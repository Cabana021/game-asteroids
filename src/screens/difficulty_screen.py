import pygame
import math
from src import settings
from src.utils.enums import GameState
from src.utils.background import Starfield

class DifficultyScreen:
    """
    Gerencia a tela onde o jogador escolhe o nível de dificuldade antes de começar a partida.
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
        self.selected_index = 0  # Começa em "NIGHTMARE"
        self.pulse_angle = 0     # Para animação de pulso do item selecionado
        
        # Ordem das dificuldades na tela
        self.difficulties = ["NIGHTMARE", "MEDIUM", "EASY"]

    def handle_event(self, event):
        """Processa a entrada do jogador para navegar e selecionar a dificuldade."""
        if self.app.transition.is_active(): return

        if event.type == pygame.KEYDOWN:
            # Navegação para cima/baixo
            if event.key in [pygame.K_DOWN, pygame.K_UP]:
                if self.app.sfx_on: self.assets['ui_nav_sound'].play()
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.difficulties)
                else:
                    self.selected_index = (self.selected_index - 1 + len(self.difficulties)) % len(self.difficulties)
            
            # Confirmação da seleção
            elif event.key == pygame.K_RETURN:
                if self.app.sfx_on: self.assets['ui_confirm_sound'].play()
                
                selected_key = self.difficulties[self.selected_index]
                self.app.set_difficulty(selected_key)
                
                # Inicia a música de ação *antes* do fade para uma transição mais suave.
                self.app.handle_music(GameState.PLAYING)
                
                self.next_screen = GameState.PLAYING
                self.app.transition.start_fade_out()

            # Voltar para o menu
            elif event.key == pygame.K_ESCAPE:
                if self.app.sfx_on: self.assets['ui_nav_sound'].play()
                self.next_screen = GameState.MENU
                self.app.transition.start_fade_out()

    def update(self):
        """Atualiza o estado da tela, como animações e transições."""
        if not self.app.transition.is_active():
            self.pulse_angle += 0.05
        
        self.background.update_menu_scroll()
        self.app.transition.update()

        # Encerra o loop da tela quando a transição de fade-out terminar.
        if self.app.transition.is_faded_out():
            self.running = False

    def draw(self):
        """Desenha todos os elementos da tela de dificuldade."""
        self.screen.fill((10, 10, 25))
        self.background.draw(self.screen)
        
        # Título da tela
        self.text_renderer.draw(self.screen, "Escolha a Dificuldade", 55, (255, 255, 255), settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT * 0.15)
        
        # Loop para desenhar cada opção de dificuldade
        for i, key in enumerate(self.difficulties):
            difficulty_data = settings.DIFFICULTY_LEVELS[key]
            y_pos = settings.SCREEN_HEIGHT * 0.40 + i * 150 # Espaçamento vertical
            
            # Estilo para o item selecionado (maior, cor pulsante)
            if i == self.selected_index:
                pulse = (math.sin(self.pulse_angle) + 1) / 2
                brightness = 200 + int(pulse * 55)
                color = (brightness, brightness, 0)
                
                title_size, desc_size = 48, 22
                
                title_rect = self.text_renderer.draw(self.screen, difficulty_data["label"], title_size, color, settings.SCREEN_WIDTH/2, y_pos)
                self.text_renderer.draw(self.screen, difficulty_data["description"], desc_size, (220, 220, 220), settings.SCREEN_WIDTH/2, y_pos + 45)
                
                # Desenha o indicador ">"
                self.text_renderer.draw(self.screen, ">", title_size, color, title_rect.left - 40, y_pos)

            # Estilo para itens não selecionados (menor, cor estática)
            else:
                color = (180, 180, 180)
                title_size, desc_size = 40, 18
                
                self.text_renderer.draw(self.screen, difficulty_data["label"], title_size, color, settings.SCREEN_WIDTH/2, y_pos)
                self.text_renderer.draw(self.screen, difficulty_data["description"], desc_size, (150, 150, 150), settings.SCREEN_WIDTH/2, y_pos + 40)

        self.app.transition.draw()

    def run(self):
        """O loop principal que executa esta tela."""
        self.running = True
        self.next_screen = GameState.MENU # Estado padrão para retorno
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