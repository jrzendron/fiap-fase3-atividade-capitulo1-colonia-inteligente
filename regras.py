"""
regras.py - REGRAS DE DECISAO (logica do sistema)

Cada condicao vira uma proposicao logica (Verdadeiro/Falso), como na
algebra de Boole:

    A = energia < 50           (energia baixa)
    B = consumo > 60           (consumo alto)
    C = energia < 20           (energia critica)
    D = temperatura < -80      (frio extremo)
    E = geracao_prevista < consumo   (deficit previsto)
    F = tempestade de poeira

Regras (avaliadas da MAIS para a MENOS importante):
    R1  C  OR (D AND A)   -> EMERGENCIA: so suporte a vida (desliga prio 2 e 3)
    R2  A  AND B          -> MODO ECONOMIA (desliga prio 3)
    R3  A                 -> ALERTA: reduzir consumo
    R4  E  AND NOT A      -> PREVENCAO: deficit previsto, reduzir antes
    R5  F                 -> priorizar energia eolica (solar prejudicado)
    R6  NOT A AND NOT E   -> situacao normal
"""

LIMITE_ENERGIA_BAIXA = 50
LIMITE_ENERGIA_CRITICA = 20
LIMITE_CONSUMO_ALTO = 60
LIMITE_FRIO_EXTREMO = -80


def calcular_proposicoes(estado, geracao_prevista=None):
    """Transforma os dados em valores logicos (True/False)."""
    energia = estado["energia_reserva"]
    consumo = estado["consumo"]
    return {
        "A": energia < LIMITE_ENERGIA_BAIXA,
        "B": consumo > LIMITE_CONSUMO_ALTO,
        "C": energia < LIMITE_ENERGIA_CRITICA,
        "D": estado.get("temperatura", 0) < LIMITE_FRIO_EXTREMO,
        "E": geracao_prevista is not None and geracao_prevista < consumo,
        "F": estado.get("tempestade_poeira", False),
    }


def decidir(estado, geracao_prevista=None):
    """
    Entrada: dicionario de estado (+ geracao prevista, opcional)
    Saida:   dicionario com o MODO, a lista de ACOES (mensagens claras)
             e qual prioridade deve ser desligada (ou None).
    """
    p = calcular_proposicoes(estado, geracao_prevista)
    A, B, C, D, E, F = p["A"], p["B"], p["C"], p["D"], p["E"], p["F"]

    modo = "NORMAL"
    desligar_a_partir_de = None
    acoes = []

    # R1 - prioridade maxima: proteger vidas
    if C or (D and A):
        modo = "EMERGENCIA"
        desligar_a_partir_de = 2
        acoes.append("EMERGENCIA: manter apenas suporte a vida, desligar sistemas prio 2 e 3")
    # R2 - condicao combinada
    elif A and B:
        modo = "ECONOMIA"
        desligar_a_partir_de = 3
        acoes.append("ATIVAR MODO ECONOMIA: desligar sistemas nao essenciais (prio 3)")

    # R3 - regra basica
    if A:
        acoes.append("ALERTA: reduzir consumo")

    # R4 - regra PREDITIVA (usa a previsao da regressao)
    if E and not A:
        acoes.append("PREVENCAO: geracao prevista nao cobre o consumo - reduzir antes de faltar")
        if modo == "NORMAL":
            modo = "ATENCAO"

    # R5 - clima
    if F:
        acoes.append("CLIMA: tempestade de poeira - priorizar energia eolica e baterias")

    # R6 - nada de errado
    if len(acoes) == 0:
        acoes.append("OK: colonia operando normalmente")

    return {"modo": modo, "acoes": acoes,
            "desligar_a_partir_de": desligar_a_partir_de, "proposicoes": p}
