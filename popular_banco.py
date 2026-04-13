"""
popular_banco.py — Insere registros de teste no banco via API.
Execute com: python popular_banco.py
A API (main.py) precisa estar rodando antes.
"""

import requests

API = "http://127.0.0.1:8000/atendimento"

mensagens = [
    {"cliente_id": "cliente_01", "texto": "qual o preco do produto?"},
    {"cliente_id": "cliente_02", "texto": "quero comprar o plano premium"},
    {"cliente_id": "cliente_03", "texto": "o sistema nao funciona"},
    {"cliente_id": "cliente_04", "texto": "estou com um erro na tela de login"},
    {"cliente_id": "cliente_05", "texto": "tenho uma duvida sobre o contrato"},
    {"cliente_id": "cliente_01", "texto": "quanto custa o plano anual?"},
    {"cliente_id": "cliente_06", "texto": "o app travou depois da atualizacao"},
    {"cliente_id": "cliente_07", "texto": "gostaria de saber mais sobre os planos"},
    {"cliente_id": "cliente_02", "texto": "problema no pagamento, nao finalizou"},
    {"cliente_id": "cliente_08", "texto": "qual o valor para 10 usuarios?"},
    {"cliente_id": "cliente_09", "texto": "nao consigo acessar minha conta"},
    {"cliente_id": "cliente_10", "texto": "como funciona o periodo de teste?"},
]

print(f"Enviando {len(mensagens)} mensagens para a API...\n")

for msg in mensagens:
    try:
        r = requests.post(API, json=msg)
        dados = r.json()
        print(f"[{dados['prioridade']:8s}] {dados['intencao']:20s} <- {msg['texto'][:40]}")
    except Exception as e:
        print(f"[ERRO] {e} — a API esta rodando?")

print("\nPronto! Abra o dashboard: python dashboard.py")
