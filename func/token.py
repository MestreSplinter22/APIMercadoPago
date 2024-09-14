import json
import os

# Caminho para o arquivo de token
TOKEN_FILE = "func/token.json"

# Função para obter o token atual
def obter_token():
    # Verifica se o arquivo de token existe
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            data = json.load(file)
            return data.get("access_token")
    else:
        return None

# Função para alterar e salvar o novo token
def alterar_token(novo_token: str):
    data = {"access_token": novo_token}
    with open(TOKEN_FILE, "w") as file:
        json.dump(data, file)
    return {"status": "Token atualizado com sucesso!"}
