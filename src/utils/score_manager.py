import json
import os

# Constantes para o diretório e nome do arquivo de score.
DATA_DIR = "data"
SCORE_FILE = "highscore.json"

def get_highscore_path():
    """
    Constrói o caminho completo para o arquivo de highscore, garantindo que
    o diretório 'data' exista.
    """
    # Navega para o diretório raiz do projeto (onde estão 'src', 'assets', etc.).
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    # Constrói o caminho para a pasta 'data' dentro da raiz do projeto.
    data_path = os.path.join(project_root, DATA_DIR)
    
    # Cria a pasta 'data' se ela ainda não existir, sem gerar erro caso já exista.
    os.makedirs(data_path, exist_ok=True)
    
    # Retorna o caminho completo para o arquivo de score.
    return os.path.join(data_path, SCORE_FILE)

def load_highscore():
    """
    Carrega o high score do arquivo JSON.
    Retorna 0 se o arquivo não for encontrado ou se houver um erro de leitura.
    """
    filepath = get_highscore_path()
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data.get("highscore", 0)  # Retorna o score ou 0 se a chave não existir
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existe ou está corrompido/vazio, considera o highscore como 0.
        return 0

def save_highscore(new_score):
    """
    Salva o novo high score no arquivo JSON.
    """
    filepath = get_highscore_path()
    data = {"highscore": new_score}
    
    try:
        with open(filepath, 'w') as f:
            # Salva os dados no formato JSON com indentação para fácil leitura.
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Erro ao salvar o highscore: {e}")