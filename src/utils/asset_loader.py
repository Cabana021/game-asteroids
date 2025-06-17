import pygame
import os
from src.utils.text_renderer import TextRenderer

def load_all_assets():
    """
    Carrega todos os assets do jogo (imagens, sons, fontes) de uma só vez
    e os retorna em um dicionário para fácil acesso em todo o projeto.
    Isso centraliza o carregamento de recursos e evita carregá-los repetidamente.
    """
    assets = {}
    
    # --- Configuração de Caminhos ---
    # Constrói o caminho absoluto para a pasta raiz do projeto, subindo dois níveis 
    # a partir do diretório atual (__file__, que está em 'src/utils').
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    assets_path = os.path.join(project_root, 'assets')

    # --- Carregamento de Fontes ---
    font_path = os.path.join(assets_path, 'fonts', 'PressStart2P-Regular.ttf')
    assets['text_renderer'] = TextRenderer(font_path)

    # --- Carregamento de Imagens ---
    img_path = os.path.join(assets_path, 'images')
    
    # Subpastas de imagens
    asteroids_folder = os.path.join(img_path, 'asteroids')
    player_folder = os.path.join(img_path, 'player')
    enemy_folder = os.path.join(img_path, 'enemy')
    keyboard_folder = os.path.join(img_path, 'keyboard')
    powerups_folder = os.path.join(img_path, 'powerups')
    
    # Assets de Asteroides
    assets['asteroid_image'] = pygame.image.load(os.path.join(asteroids_folder, 'asteroid.png')).convert_alpha()
    
    # Assets de Power-ups e Efeitos
    assets['pet_ship_image'] = pygame.image.load(os.path.join(powerups_folder, 'pet.png')).convert_alpha()
    powerup = pygame.image.load(os.path.join(powerups_folder, 'powerup.png')).convert_alpha()
    assets['powerup_image'] = pygame.transform.scale(powerup, (32, 32))  # Redimensiona para um tamanho padrão
    
    # Assets do Jogador
    assets['ship_image'] = pygame.image.load(os.path.join(player_folder, 'ship.png')).convert_alpha()
    assets['player_gunshot_image'] = pygame.image.load(os.path.join(player_folder, 'player_gunshot.png')).convert_alpha()
    assets['heart_image'] = pygame.image.load(os.path.join(player_folder, 'heart.png')).convert_alpha()
    
    # Assets do Inimigo (UFO)
    assets['ufo_vertical_image'] = pygame.image.load(os.path.join(enemy_folder, 'enemy_vertical.png')).convert_alpha()
    assets['ufo_image'] = pygame.image.load(os.path.join(enemy_folder, 'enemy.png')).convert_alpha()
    assets['enemy_gunshot_image'] = pygame.image.load(os.path.join(enemy_folder, 'enemy_gunshot.png')).convert_alpha()
    
    # Assets de Teclas do Teclado (para o Tutorial)
    assets['arrowup'] = pygame.image.load(os.path.join(keyboard_folder, 'arrowup.png')).convert_alpha()
    assets['arrowleft'] = pygame.image.load(os.path.join(keyboard_folder, 'arrowleft.png')).convert_alpha()
    assets['arrowright'] = pygame.image.load(os.path.join(keyboard_folder, 'arrowright.png')).convert_alpha()
    assets['space_bar'] = pygame.image.load(os.path.join(keyboard_folder, 'space_bar.png')).convert_alpha()
    
    # Carregamento de Animação (Spritesheet de Explosão)
    assets['explosion_anim'] = []
    try:
        spritesheet = pygame.image.load(os.path.join(asteroids_folder, 'explosion.png')).convert_alpha()
        # Itera sobre a spritesheet, fatiando cada frame da animação.
        for i in range(6):
            frame = spritesheet.subsurface(pygame.Rect(i * 20, 0, 20, 20))
            assets['explosion_anim'].append(pygame.transform.scale(frame, (60, 60))) # Redimensiona para o jogo
    except pygame.error:
        print("ERRO: Não foi possível carregar a spritesheet de explosão.")

    # --- Carregamento de Sons e Músicas ---
    snd_path = os.path.join(assets_path, 'sounds')
    
    # Subpastas de sons
    music_folder = os.path.join(snd_path, 'music')
    ui_folder = os.path.join(snd_path, 'sfx/ui')
    player_sfx = os.path.join(snd_path, 'sfx/player')
    enemy_sfx = os.path.join(snd_path, 'sfx/enemy')
    world_sfx = os.path.join(snd_path, 'sfx/world')

    # Músicas (Soundtrack)
    assets['menu_sound'] = pygame.mixer.Sound(os.path.join(music_folder, 'main_menu_soundtrack.wav'))
    assets['action_soundtrack'] = pygame.mixer.Sound(os.path.join(music_folder, 'action_soundtrack.wav'))
    
    # Efeitos Sonoros (SFX) - Interface de Usuário
    assets['game_over_sound'] = pygame.mixer.Sound(os.path.join(ui_folder, 'game_over.wav'))
    assets['ui_nav_sound'] = pygame.mixer.Sound(os.path.join(ui_folder, 'hover_button.wav'))
    assets['ui_nav_sound'].set_volume(0.5)  # Ajusta o volume para não ser irritante
    assets['ui_confirm_sound'] = pygame.mixer.Sound(os.path.join(ui_folder, 'confirm_button.wav'))
    assets['ui_confirm_sound'].set_volume(0.5)
    
    # Efeitos Sonoros (SFX) - Gameplay
    assets['powerup_sound'] = pygame.mixer.Sound(os.path.join(world_sfx, 'powerup_collect.wav'))
    assets['powerup_sound'].set_volume(0.7)
    assets['player_gunshot_sound'] = pygame.mixer.Sound(os.path.join(player_sfx, 'player_laser_gunshot.wav'))
    assets['pet_gunshot_sound'] = pygame.mixer.Sound(os.path.join(player_sfx, 'pet_gunshot.wav'))
    assets['enemy_gunshot_sound'] = pygame.mixer.Sound(os.path.join(enemy_sfx, 'enemy_gunshot_sound.wav'))
    assets['explosion_sound'] = pygame.mixer.Sound(os.path.join(world_sfx, 'explosion.wav'))
    assets['scream_sound'] = pygame.mixer.Sound(os.path.join(world_sfx, 'explosion_and_scream.wav'))
    
    return assets