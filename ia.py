"""
ia.py — Lógica de triagem e classificação de mensagens.
Sem dependências de banco ou HTTP: só recebe texto, devolve resultado.
Fácil de testar unitariamente e de trocar por um modelo real no futuro.
"""


REGRAS = [
    (
        ["preço", "comprar", "quanto", "valor", "custo", "orçamento"],
        "COMPRA",
        "ALTA",
    ),
    (
        ["erro", "problema", "não funciona", "bug", "falha", "travou", "quebrou"],
        "PROBLEMA_TECNICO",
        "CRITICA",
    ),
]

DEFAULT_INTENCAO  = "DUVIDA_GERAL"
DEFAULT_PRIORIDADE = "MEDIA"


def classificar(texto: str) -> dict:
    """
    Recebe o texto do cliente e devolve:
        intencao, prioridade, resposta_sugerida
    """
    t = texto.lower()

    for palavras_chave, intencao, prioridade in REGRAS:
        if any(p in t for p in palavras_chave):
            break
    else:
        intencao  = DEFAULT_INTENCAO
        prioridade = DEFAULT_PRIORIDADE

    return {
        "intencao":   intencao,
        "prioridade": prioridade,
        "resposta_sugerida": (
            f"Recebemos sua mensagem sobre {intencao}. "
            "Um atendente já vai falar com você!"
        ),
    }