# === CONFIGURAÇÕES GERAIS E DE TELA ===
# Parâmetros que não mudam, independentemente da dificuldade.
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Asteroids"
SAFE_SPAWN_DISTANCE = 150  # Distância mínima da nave para spawn seguro de asteroides

# === CONFIGURAÇÕES FÍSICAS DA NAVE ===
# Como a nave se comporta.
SHIP_RADIUS = 8
SHIP_ACCELERATION = 0.2
SHIP_FRICTION = 0.02
SHIP_ROTATION_SPEED = 4
SHIP_MAX_SPEED = 7

# === CONFIGURAÇÕES FÍSICAS DOS TIROS ===
# Como os tiros se comportam.
BULLET_SPEED = 10
BULLET_RADIUS = 2
BULLET_LIFETIME = 1200  # Em milissegundos
PLAYER_BULLET_COOLDOWN = 250 # Cooldown para o tiro do jogador
ENEMY_BULLET_SPEED = 8

# === CONFIGURAÇÕES FÍSICAS DOS ASTEROIDES ===
# Tamanhos base dos asteroides.
ASTEROID_MIN_SPEED = 1
ASTEROID_MAX_SPEED = 3
ASTEROID_SIZES = {
    3: 45, # size: radius (Large)
    2: 25, # size: radius (Medium)
    1: 15  # size: radius (Small)
}

# === PONTUAÇÃO BASE ===
# Pontos concedidos antes de aplicar o multiplicador de dificuldade.
BASE_POINTS = {
    "ASTEROID_LARGE": 250,
    "ASTEROID_MEDIUM": 150,
    "ASTEROID_SMALL": 50,
    "UFO": 1000
}

# === NÍVEIS DE DIFICULDADE ===
DIFFICULTY_LEVELS = {
    "EASY": {
        "label": "Fácil",
        "description": "Sério, cara?",
        
        # Jogo
        "start_lives": 5,
        "points_multiplier": 0.5,

        # Spawns
        "initial_asteroids": 4,
        "max_asteroids": 8,
        "ufo_spawn_rate": 17000, # ms
        "ufo_shot_cooldown": 2500, # ms
        "ufo_speed": 4,
        "num_ufos": 1 
    },
    "MEDIUM": {
        "label": "Médio",
        "description": "Gameplay casual.",

        # Jogo
        "start_lives": 3,
        "points_multiplier": 1.0,

        # Spawns
        "initial_asteroids": 6,
        "max_asteroids": 12,
        "ufo_spawn_rate": 12000, # ms
        "ufo_shot_cooldown": 1800, # ms
        "ufo_speed": 6,
        "num_ufos": 1
    },
    "NIGHTMARE": {
        "label": "Pesadelo",
        "description": "Você não sobreviverá!",

        # Jogo
        "start_lives": 1,
        "points_multiplier": 2.0,

        # Spawns
        "initial_asteroids": 10,
        "max_asteroids": 20,
        "ufo_spawn_rate": 3000, # ms
        "ufo_shot_cooldown": 1000, # ms
        "ufo_speed": 8,
        "num_ufos": 2
    }
}
