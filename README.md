# Asteroids

Uma interpretação moderna e com uso de funcionalidades do clássico jogo de arcade Asteroids, construído do zero em Python com a biblioteca Pygame. Pilote a sua nave por um campo de asteroides, enfrente OVNIs hostis e lute pela maior pontuação em uma experiência arcade dinâmica e polida.

![Gameplay GIF](https://github.com/user-attachments/assets/728ed4f0-ac92-44ee-b61a-e9959bf5bff9)

---

## ✨ Funcionalidades

- **Jogabilidade Clássica com Toque Moderno:** Física de inércia, rotação e aceleração com a clássica tela "wrap-around".
- **Inimigos Variados:**
  - **Asteroides** de 3 tamanhos diferentes, que se dividem ao serem destruídos.
  - **UFOs** com múltiplos padrões de movimento (horizontal e vertical) e mira inteligente.
- **Sistema de Dificuldade:** Escolha entre os modos **Fácil, Médio e Pesadelo**, que alteram vidas iniciais, velocidade dos inimigos, frequência de tiros e pontuação.
- **Efeitos Visuais Avançados:**
  - **Sistema de Partículas:** Explosões, brilhos e um rastro de propulsor dinâmico que reage à aceleração da nave.
  - **Screen Shake:** Efeito de tremor de tela que adiciona impacto às explosões e colisões.
  - **Fundo Parallax:** Um campo estelar com múltiplas camadas que reage ao movimento da nave, criando uma sensação de profundidade.
- **Interface Completa e Animada:**
  - Menus totalmente navegáveis (Principal, Pausa, Configurações, Tutorial, Dificuldade).
  - Tela de **Game Over** com contagem de pontos animada e destaque para novos recordes.
  - HUD com alerta de UFOs pulsante.
  - Transições de tela suaves com efeito de _fade_.
- **Áudio Imersivo:**
  - Trilha sonora dinâmica que muda entre o menu e a ação do jogo.
  - Efeitos sonoros para tiros, explosões, navegação de UI e mais.
  - Opções para ativar/desativar música e SFX de forma independente.
- **Persistência de Dados:** O seu **Highscore** é salvo localmente em um arquivo `data/highscore.json`.

---

## 🎮 Controles

| Ação            | Tecla                |
| --------------- | -------------------- |
| Rotacionar      | `←` / `→` (Setas)    |
| Acelerar        | `↑` (Seta para Cima) |
| Atirar          | `Barra de Espaço`    |
| Pausar / Voltar | `ESC`                |
| Confirmar       | `ENTER`              |

---

## 🚀 Como Executar

### Pré-requisitos

- **Python 3.8** ou superior.
- **Pygame**

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/Cabana021/game-asteroids.git
    cd seu-repositorio
    ```

2.  **(Opcional, mas recomendado) Crie e ative um ambiente virtual:**

    ```bash
    # Para Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o jogo:**
    ```bash
    python main.py
    ```

---

## 📂 Estrutura e Arquitetura

O projeto foi desenvolvido com uma arquitetura modular e orientada a sistemas para garantir um código limpo, organizado e de fácil manutenção.

├── assets/ # Contém todas as imagens, sons e fontes.

├── data/ # Armazena dados persistentes, como o highscore.

├── src/ # Pasta principal com o código-fonte.

│ ├── entities/ # Classes para objetos do jogo (Nave, Asteroide, UFO, Bala).

│ ├── screens/ # Lógica para cada tela individual (Menu, Jogo, Game Over).

│ ├── systems/ # Sistemas que gerenciam a lógica global (Colisão, Spawn, VFX).

│ ├── utils/ # Ferramentas e classes auxiliares (HUD, Assets, Scores).

│ ├── game.py # Lógica principal da tela de jogo.

│ ├── game_state.py # Contêiner de dados para a sessão de jogo.

│ └── settings.py # Constantes e configurações globais.

└── run.py # Ponto de entrada da aplicação, gerencia a máquina de estados.

└── requirements.txt # Dependências do projeto.

### Detalhes Técnicos

- **Máquina de Estados:** A classe `App` em `run.py` funciona como uma máquina de estados finitos, gerenciando a transição entre as diferentes telas (`GameState.MENU`, `GameState.PLAYING`, etc.), o que mantém a lógica de cada tela isolada e organizada.
- **Arquitetura Orientada a Sistemas:** A lógica do gameplay em `game.py` é desacoplada e delegada a sistemas especializados:
  - **`CollisionSystem`**: Processa todas as interações e colisões entre as entidades do jogo.
  - **`SpawnSystem`**: Controla quando e como os inimigos aparecem, ajustando-se à dificuldade.
  - **`VFXSystem`**: Gerencia todos os efeitos visuais, como a criação de partículas e o _screen shake_.
- **Estado de Jogo Desacoplado:** A classe `GameSessionState` armazena todos os dados de uma partida (pontuação, vidas, grupos de sprites). Isso permite que o jogo seja facilmente reiniciado e que diferentes sistemas acessem os dados do jogo de forma segura e centralizada.

---

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Sinta-se à vontade para usar, modificar e distribuir o código.
