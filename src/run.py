import pygame
from src import settings
from src.game import GameScreen
from src.screens.main_menu import MainMenuScreen
from src.screens.settings_screen import SettingsScreen
from src.screens.difficulty_screen import DifficultyScreen
from src.screens.game_over import GameOverScreen
from src.screens.tutorial_screen import TutorialScreen
from src.screens.pause_screen import PauseScreen
from src.utils.asset_loader import load_all_assets 
from src.utils.enums import GameState 
from src.utils.transition import FadeTransition
from src.utils.score_manager import load_highscore, save_highscore

class App:
    """
    Classe principal que gerencia a aplicação inteira.
    Atua como uma máquina de estados, controlando a transição entre as diferentes
    telas do jogo (Menu, Jogo, Configurações, etc.).
    """
    def __init__(self):
        # --- Inicialização do Pygame e da Janela ---
        pygame.init()
        pygame.mixer.init(channels=16)  # Permite múltiplos canais de áudio
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()

        # --- Carregamento de Recursos e Utilitários ---
        self.assets = load_all_assets()
        self.transition = FadeTransition(self.screen)
        self.highscore = load_highscore()

        # --- Configurações Globais da Aplicação ---
        self.music_on = True
        self.sfx_on = True
        self.screen_shake_on = True
        
        # --- Gerenciamento de Estado e Música ---
        self.music_channel = pygame.mixer.Channel(0)  # Canal dedicado para a música de fundo
        self.current_state = GameState.MENU  # O jogo começa no menu principal
        
        # --- Configurações de Dificuldade ---
        self.difficulty_settings = None
        self.set_difficulty("MEDIUM")  # Define a dificuldade padrão ao iniciar

    def set_difficulty(self, difficulty_key):
        """Atualiza as configurações de dificuldade com base na chave fornecida."""
        self.difficulty_settings = settings.DIFFICULTY_LEVELS[difficulty_key]

    def toggle_screen_shake(self): 
        """Ativa ou desativa o efeito de 'screen shake'."""
        self.screen_shake_on = not self.screen_shake_on
    
    def toggle_sfx(self):
        """Ativa ou desativa os efeitos sonoros."""
        self.sfx_on = not self.sfx_on
    
    def toggle_music(self):
        """Ativa ou desativa a música de fundo e atualiza imediatamente."""
        self.music_on = not self.music_on
        self.handle_music(self.current_state)

    def handle_music(self, new_state):
        """Gerencia qual faixa de música deve tocar com base no estado atual do jogo."""
        # Se a música estiver desativada, para qualquer som e sai da função.
        if not self.music_on:
            self.music_channel.stop()
            return
        
        # Determina a faixa de música correta para o novo estado.
        target_track = None
        if new_state in [GameState.MENU, GameState.TUTORIAL, GameState.SETTINGS, GameState.DIFFICULTY_SELECT]:
            target_track = 'menu_sound'
        elif new_state == GameState.PLAYING:
            target_track = 'action_soundtrack'
        
        # Verifica se a música alvo já está tocando para evitar reiniciá-la desnecessariamente.
        current_sound = self.music_channel.get_sound()
        target_sound = self.assets.get(target_track)

        # Se a música precisa ser trocada, para a atual e inicia a nova.
        if current_sound != target_sound:
            self.music_channel.stop()
            if target_sound:
                self.music_channel.play(target_sound, loops=-1)

    def run(self):
        """O loop principal da aplicação que gerencia as telas."""
        screen_data = None  # Dados passados entre as telas (ex: pontuação final)
        game_instance = None  # Armazena a instância da tela de jogo para poder pausar/retomar
        
        self.transition.start_fade_in()  # Inicia com um fade-in suave
        
        while self.current_state != GameState.QUIT:
            # --- LÓGICA DA MÁQUINA DE ESTADOS ---

            # 1. Resolve estados de transição que afetam a instância do jogo.
            # Se o jogo for reiniciado ou voltar ao menu, a instância anterior é descartada.
            if self.current_state == GameState.RESTART:
                game_instance = None
                self.current_state = GameState.PLAYING
            elif self.current_state == GameState.MENU:
                game_instance = None
            
            # Verifica se o jogo estava pausado para tratar a música corretamente.
            was_paused = self.current_state == GameState.RESUME
            if was_paused:
                self.current_state = GameState.PLAYING

            # 2. Cria a instância da tela a ser executada nesta iteração do loop.
            screen_instance = None 
            if self.current_state == GameState.PLAYING:
                # Se não houver uma instância de jogo ativa, cria uma nova.
                if game_instance is None:
                    game_instance = GameScreen(self.screen, self.clock, self.assets, self)
                screen_instance = game_instance

            elif self.current_state == GameState.GAME_OVER:
                game_instance = None  # Garante que o jogo não pode ser retomado
                final_score = screen_data if screen_data is not None else 0
                is_new_highscore = final_score > self.highscore
                if is_new_highscore:
                    self.highscore = final_score
                    save_highscore(self.highscore)
                screen_instance = GameOverScreen(self.screen, self.clock, self.assets, final_score, self.highscore, is_new_highscore, self)

            elif self.current_state == GameState.MENU:
                screen_instance = MainMenuScreen(self.screen, self.clock, self.assets, self)

            elif self.current_state == GameState.DIFFICULTY_SELECT:
                screen_instance = DifficultyScreen(self.screen, self.clock, self.assets, self)

            elif self.current_state == GameState.SETTINGS:
                screen_instance = SettingsScreen(self.screen, self.clock, self.assets, self)

            elif self.current_state == GameState.TUTORIAL:
                screen_instance = TutorialScreen(self.screen, self.clock, self.assets, self)

            elif self.current_state == GameState.PAUSE:
                screen_instance = PauseScreen(self.screen, self.clock, self.assets, screen_data, self)

            # Se por algum motivo o estado for inválido, encerra o loop para evitar erros.
            if screen_instance is None:
                print(f"ERRO: Estado desconhecido ou não gerenciado: {self.current_state}")
                break

            # 3. Gerencia a música com base no estado atual ou se acabou de sair da pausa.
            if self.current_state == GameState.PAUSE:
                self.music_channel.pause()
            elif was_paused: 
                if self.music_on:
                    self.music_channel.unpause()
            else:
                self.handle_music(self.current_state)
            
            # 4. Executa a tela atual, que rodará seu próprio loop interno.
            # Ela retorna o próximo estado e quaisquer dados necessários.
            next_state, screen_data = screen_instance.run()
            
            # 5. Se o estado mudou, inicia uma transição de fade-in para a nova tela.
            if self.current_state != next_state:
                self.transition.start_fade_in()
                
            self.current_state = next_state

        # Encerra o Pygame de forma limpa quando o loop principal termina.
        pygame.quit()