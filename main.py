from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from func.qrcode import gerar_pagamento_pix
from func.token import alterar_token

# Inicializa a aplicação FastAPI
app = FastAPI()
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# Rota para gerar o PIX QR Code
@app.get("/gerarpix/{amount}/{description}/{email}")
async def gerar_pix(amount: float, description: str, email: str):
    # Chama a função para gerar o pagamento via PIX
    pagamento = gerar_pagamento_pix(amount, description, email)

    # Verifica se houve erro
    if "error" in pagamento:
        return {"status": "erro", "message": pagamento["message"]}

    # Verifica se a chave existe antes de acessá-la
    if "qr_code" not in pagamento:
        return {"status": "erro", "message": "Erro ao gerar QR Code"}

    # Retorna os dados do pagamento
    return {
        "qr_code": pagamento["qr_code"],
        "qr_code_base64": pagamento["qr_code_base64"],
        "ticket_url": pagamento["ticket_url"],
        "payment_id": pagamento["payment_id"],
        "extracted_payment_id": pagamento["extracted_payment_id"],
        "payment_status": pagamento["payment_status"]
    }

# Rota para trocar o token
@app.get("/trocartoken/{new_token}")
async def trocar_token(new_token: str):
    resultado = alterar_token(new_token)
    return resultado
