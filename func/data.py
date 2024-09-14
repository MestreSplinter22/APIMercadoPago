from datetime import datetime

import pytz
from tinydb import Query, TinyDB

# Inicializa a TinyDB
db = TinyDB('db.json')

def salvar_dados_pix(amount, description, email, payment_status, payment_id, extracted_payment_id):
    # Obtém a hora atual no formato UTC brasileiro
    utc_brazilian_tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(utc_brazilian_tz).isoformat()

    # Adiciona um novo registro na tabela
    db.insert({
        'amount': amount,
        'description': description,
        'email': email,
        'payment_status': payment_status,
        'payment_id': payment_id,
        'extracted_payment_id': extracted_payment_id,
        'timestamp': now
    })
