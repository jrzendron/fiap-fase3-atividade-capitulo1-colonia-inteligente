"""Regras que escolhem o modo de operação da colônia."""

LIMITE_ENERGIA_BAIXA = 50     # Abaixo de 50% da reserva, há alerta.
LIMITE_ENERGIA_CRITICA = 20   # Abaixo de 20%, o caso é emergência.
LIMITE_CONSUMO_ALTO = 60      # Consumo acima de 60 kWh é alto.
LIMITE_FRIO_EXTREMO = -80     # Temperatura abaixo de -80 °C é extrema.


def calcular_proposicoes(estado, geracao_prevista=None):
    """Avalia as seis condições usadas nas decisões."""
    energia = estado["energia_reserva"]  # Porcentagem disponível na bateria.
    consumo = estado["consumo"]  # Energia usada pela colônia em kWh.
    return {
        "A": energia < LIMITE_ENERGIA_BAIXA,  # Reserva baixa.
        "B": consumo > LIMITE_CONSUMO_ALTO,  # Consumo alto.
        "C": energia < LIMITE_ENERGIA_CRITICA,  # Reserva crítica.
        "D": estado.get("temperatura", 0) < LIMITE_FRIO_EXTREMO,  # Frio extremo.
        "E": geracao_prevista is not None and geracao_prevista < consumo,  # Déficit previsto.
        "F": estado.get("tempestade_poeira", False),  # Poeira no ambiente.
    }


def decidir(estado, geracao_prevista=None):
    """Devolve o modo, as ações e a prioridade que deve ser desligada."""
    proposicoes = calcular_proposicoes(estado, geracao_prevista)
    reserva_baixa = proposicoes["A"]  # Reserva menor que 50%.
    consumo_alto = proposicoes["B"]  # Consumo acima de 60 kWh.
    reserva_critica = proposicoes["C"]  # Reserva menor que 20%.
    frio_extremo = proposicoes["D"]  # Temperatura abaixo do limite.
    deficit_previsto = proposicoes["E"]  # Geração insuficiente.
    tempestade = proposicoes["F"]  # Poeira reduz a geração solar.

    modo = "NORMAL"  # Começa sem restrições.
    desligar_a_partir_de = None  # Nenhum equipamento será desligado por padrão.
    acoes = []  # Guarda as mensagens para a equipe.

    # Emergência tem prioridade sobre economia.
    if reserva_critica or (frio_extremo and reserva_baixa):
        modo = "EMERGENCIA"
        desligar_a_partir_de = 2  # Preserva somente prioridade 1.
        acoes.append("EMERGENCIA: manter apenas suporte a vida, desligar sistemas prio 2 e 3")
    elif reserva_baixa and consumo_alto:  # Duas condições levam à economia.
        modo = "ECONOMIA"
        desligar_a_partir_de = 3  # Desliga apenas os não essenciais.
        acoes.append("ATIVAR MODO ECONOMIA: desligar sistemas nao essenciais (prio 3)")

    if reserva_baixa:  # O alerta também aparece nos modos mais graves.
        acoes.append("ALERTA: reduzir consumo")

    if deficit_previsto and not reserva_baixa:  # Avisa antes de faltar energia.
        acoes.append("PREVENCAO: geracao prevista nao cobre o consumo; reduzir antes de faltar")
        if modo == "NORMAL":  # Um aviso preventivo não é emergência.
            modo = "ATENCAO"

    if tempestade:  # A poeira prejudica os painéis solares.
        acoes.append("CLIMA: tempestade de poeira; priorizar energia eolica e baterias")

    if len(acoes) == 0:  # Nenhuma regra encontrou um problema.
        acoes.append("OK: colonia operando normalmente")

    # O programa usa esses campos para mostrar e aplicar a decisão.
    return {"modo": modo, "acoes": acoes,
            "desligar_a_partir_de": desligar_a_partir_de, "proposicoes": proposicoes}
