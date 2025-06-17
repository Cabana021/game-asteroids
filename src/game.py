import pygame
from . import settings
from .entities.ship import Ship
from .entities.bullet import PlayerBullet
from .systems.collision_system import CollisionSystem
from .systems.spawn_system import SpawnSystem
from .systems.vfx_system import VFXSystem
from .utils.hud import HUD
from .utils.background import Starfield
from .game_state import GameSessionState
from .utils.enums import GameState

class GameScreen:
    """
    Gerencia toda a lógica, atualização e renderização da tela de jogo principal.
    Esta classe é um "mini-aplicativo" que roda quando o estado do jogo é 'PLAYING'.
    """
    def __init__(self, screen, clock, assets, app):
        self.screen = screen
        self.clock = clock
        self.assets = assets
        self.app = app  # Referência à classe principal para acessar configurações globais
        self._start_game()

    def _start_game(self):
        """Inicializa ou reinicializa todos os componentes para uma nova partida."""
        # Cria um contêiner para todos os dados da sessão de jogo atual.
        self.state = GameSessionState(self.assets, self.app.difficulty_settings)
        
        # Inicializa os sistemas que gerenciam a lógica do jogo.
        self.vfx = VFXSystem(self.state, self.app)
        self.collision = CollisionSystem(self.state, self.vfx, self.assets, self.app)
        self.spawn = SpawnSystem(self.state, self.assets, self.app)
        
        # Inicializa os componentes de interface e visuais.
        self.hud = HUD(self.assets)
        self.background = Starfield()
        
        # Variáveis de controle do jogo.
        self.player_shot_countdown = 0
        self.running = True
        
        # Define o estado padrão para o qual a tela de jogo transitará ao terminar.
        self.next_screen = GameState.GAME_OVER
        self.screen_data = None

    def run(self):
        """O loop principal da tela de jogo. Continua até que 'self.running' se torne False."""
        self.running = True
        while self.running:
            # Garante que o jogo rode a uma taxa de quadros constante e obtém o delta time.
            dt = self.clock.tick(settings.FPS)
            
            # Estrutura clássica de um game loop.
            self._handle_events()
            self._update(dt)
            self._draw()

            # Se a transição de fade-out terminou, encerra o loop desta tela.
            if self.app.transition.is_faded_out():
                self.running = False

            # Atualiza o conteúdo da tela inteira.
            pygame.display.flip()
        
        # Retorna o próximo estado e os dados para a classe App.
        return self.next_screen, self.screen_data

    def _handle_events(self):
        """Processa todas as entradas do usuário (teclado, fechar janela)."""
        # Não processa eventos se uma transição de tela estiver ativa.
        if self.app.transition.is_active():
            return

        for event in pygame.event.get():
            # Evento para fechar a janela.
            if event.type == pygame.QUIT:
                self.next_screen = GameState.QUIT
                self.app.transition.start_fade_out()
            
            # Eventos de teclas pressionadas.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._handle_player_shooting()
                elif event.key == pygame.K_ESCAPE:
                    self.next_screen = GameState.PAUSE
                    self.screen_data = self.screen.copy()  # Salva um screenshot para o fundo da pausa
                    self.app.transition.start_fade_out()

    def _update(self, dt):
        """Atualiza a lógica de todos os objetos e sistemas do jogo."""
        # Se uma transição estiver ativa, apenas atualiza a transição.
        if self.app.transition.is_active():
            self.app.transition.update()
            return
            
        # Atualiza o cooldown de tiro do jogador.
        if self.player_shot_countdown > 0:
            self.player_shot_countdown -= dt
            
        # Cria partículas de rastro se a nave estiver acelerando.
        if self.state.ship.accelerating:
            self.vfx.create_thrust_particles()
        
        # Delega a atualização para os sistemas especializados.
        self.spawn.update(dt)
        self.vfx.update()
        self.collision.process()
        
        # Atualiza todos os sprites do jogo.
        self.state.all_sprites.update(dt, self.state.ship)
        
        # Atualiza o fundo para criar um efeito de parallax com base na velocidade da nave.
        self.background.update_game_parallax(self.state.ship.velocity)
        
        self.app.transition.update()

        # Verifica a condição de fim de jogo.
        if self.state.lives <= 0:
            self.next_screen = GameState.GAME_OVER
            self.screen_data = self.state.score  # Passa a pontuação final para a tela de Game Over
            self.app.transition.start_fade_out()

    def _draw(self):
        """Desenha todos os elementos visuais na tela."""
        # Obtém o deslocamento da câmera para o efeito de "screen shake".
        render_offset = self.vfx.get_render_offset()
        
        # Limpa a tela e desenha o fundo.
        self.screen.fill((10, 10, 25))
        self.background.draw(self.screen)
        
        # Desenha todos os sprites, exceto a nave, para que o rastro fique atrás dela.
        for sprite in self.state.all_sprites:
            if sprite is not self.state.ship:
                self.screen.blit(sprite.image, (sprite.rect.x + render_offset[0], sprite.rect.y + render_offset[1]))
        
        # Desenha a nave por último para que ela fique por cima de tudo.
        if self.state.ship.visible:
            self.screen.blit(self.state.ship.image, (self.state.ship.rect.x + render_offset[0], self.state.ship.rect.y + render_offset[1]))

        # Desenha a interface (HUD) e a camada de transição por cima de todos os elementos do jogo.
        self.hud.draw(self.screen, self.state.score, self.state.lives, bool(self.state.ufos))
        self.app.transition.draw()
        
    def _handle_player_shooting(self):
        """Lida com a lógica de criação de um projétil quando o jogador atira."""
        # Verifica se a nave está viva e se o cooldown de tiro já terminou.
        if self.state.ship.alive() and self.player_shot_countdown <= 0:
            self.player_shot_countdown = settings.PLAYER_BULLET_COOLDOWN
            
            # Toca o som de tiro, se estiver ativado.
            if self.app.sfx_on:
                self.assets['player_gunshot_sound'].play()
                
            # Cria e adiciona a nova bala aos grupos de sprites apropriados.
            bullet_data = self.state.ship.shoot(self.assets['player_gunshot_image'])
            new_bullet = PlayerBullet(bullet_data["pos"], bullet_data["dir"], bullet_data["img"])
            self.state.all_sprites.add(new_bullet)
            self.state.bullets.add(new_bullet)
