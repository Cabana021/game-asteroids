from enum import Enum, auto

class GameState(Enum):
    """
    Define todos os possíveis estados da máquina de estados do jogo.
    Usar um Enum torna o código mais legível e seguro contra erros de digitação.
    `auto()` atribui automaticamente um valor inteiro único para cada membro.
    """
    # Telas principais
    MENU = auto()
    DIFFICULTY_SELECT = auto()
    SETTINGS = auto()
    PLAYING = auto()
    PAUSE = auto()
    TUTORIAL = auto()
    GAME_OVER = auto()
    
    # Ações/Transições
    QUIT = auto()       # Sinaliza para encerrar a aplicação
    RESUME = auto()     # Sinaliza para voltar ao jogo a partir da pausa
    RESTART = auto()    # Sinaliza para começar um novo jogo

# Enum para futuros tipos de power-ups.
class PowerUpType(Enum):
    IMMORTALITY = auto()      # 1. Imortalidade por alguns segundos
    EXTRA_LIFE = auto()       # 2. Adiciona +1 vida
    RAPID_FIRE = auto()       # 3. Cooldown de tiro reduzido por alguns segundos
    PET_SHIP = auto()         # 4. Adiciona uma nave de apoio que atira
    NUKE = auto()             # 5. Destrói todos os asteroides na tela
    SCORE_MULTIPLIER = auto() # 6. Multiplicador de pontos por um tempo