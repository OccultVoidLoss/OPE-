import os

#Diretórios para arquivo JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "models", "data", "dados.json")
FOTOS_FILE = os.path.join(BASE_DIR, "models", "data", "fotos.json")