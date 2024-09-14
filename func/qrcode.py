import mercadopago
from func.token import obter_token
from urllib.parse import urlparse
from func.data import salvar_dados_pix  # Importa a nova função

# Função que gera o pagamento via PIX QR Code
def gerar_pagamento_pix(transaction_amount: float, description: str, email: str):
    try:
        # Obtem o token do arquivo token.json
        access_token = obter_token()
        print("Token obtido:", access_token)

        # Inicializa o SDK do Mercado Pago com o token obtido
        sdk = mercadopago.SDK(access_token)
        print("SDK inicializado")

        # Cria os dados do pagamento
        payment_data = {
            "transaction_amount": transaction_amount,  # Valor da transação
            "description": description,  # Descrição da cobrança
            "payment_method_id": "pix",  # Forma de pagamento: PIX
            "payer": {
                "email": email,  # Email do comprador
            }
        }
        print("Dados do pagamento criados")

        # Realiza a chamada para criar o pagamento
        payment_response = sdk.payment().create(payment_data)
        print("Requisição enviada")

        # Verifica a resposta da API
        if payment_response["status"] == 201:
            # Extrai os dados do QR Code
            qr_code = payment_response["response"]["point_of_interaction"]["transaction_data"]["qr_code"]
            qr_code_base64 = payment_response["response"]["point_of_interaction"]["transaction_data"]["qr_code_base64"]
            ticket_url = payment_response["response"]["point_of_interaction"]["transaction_data"]["ticket_url"]
            payment_status = payment_response["response"]["status"]  # Status do pagamento
            payment_id = payment_response["response"]["id"]  # ID do pagamento gerado

            # Extrai o ID do pagamento da URL
            parsed_url = urlparse(ticket_url)
            path_parts = parsed_url.path.split('/')
            payment_id_from_url = path_parts[3]  # ID do pagamento está na posição 3

            # Salva os dados do pagamento na TinyDB
            salvar_dados_pix(transaction_amount, description, email, payment_status, payment_id, payment_id_from_url)

            # Retorna os dados do QR Code, status do pagamento e ID do pagamento
            return {
                "qr_code": qr_code,
                "qr_code_base64": qr_code_base64,
                "ticket_url": ticket_url,
                "payment_status": payment_status,
                "payment_id": payment_id,
                "extracted_payment_id": payment_id_from_url
            }
        else:
            print("Erro ao criar pagamento:", payment_response["status"])
            print("Detalhes do erro:", payment_response)
            return {"status": "erro", "message": "internal_error"}
    except Exception as e:
        print("Erro inesperado:", e)
        return {"status": "erro", "message": "internal_error"}