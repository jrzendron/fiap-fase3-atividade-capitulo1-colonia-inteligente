"""
analise_energia.py - ANALISE DO USO DE ENERGIA
Compara geracao x consumo (e a reserva) e devolve um diagnostico.
"""

MARGEM_EQUILIBRIO = 5  # diferenca (kWh) considerada "equilibrada"


def analisar_energia(geracao, consumo, reserva=None):
    """
    Retorna um dicionario com saldo, situacao e mensagem.
      consumo > geracao  -> RISCO (deficit)
      geracao > consumo  -> possivel DESPERDICIO (sobra)
      diferenca pequena  -> EQUILIBRIO
    """
    saldo = geracao - consumo

    if abs(saldo) <= MARGEM_EQUILIBRIO:
        situacao = "EQUILIBRIO"
        mensagem = "OK: geracao e consumo equilibrados"
    elif consumo > geracao:
        situacao = "DEFICIT"
        mensagem = "ALERTA: consumo maior que geracao"
    else:
        situacao = "EXCEDENTE"
        mensagem = "SUGESTAO: armazenar energia excedente"

    # Reserva entra como informacao extra
    if reserva is not None and situacao == "DEFICIT":
        if reserva < 20:
            mensagem += " e reserva CRITICA"
        elif reserva < 50:
            mensagem += " e reserva baixa"
        else:
            mensagem += " (reserva acima de 50%)"

    if reserva is not None and situacao == "EXCEDENTE" and reserva >= 100:
        mensagem = "SUGESTAO: baterias cheias - ligar sistemas nao essenciais / estufa"

    return {"geracao": geracao, "consumo": consumo, "saldo": saldo,
            "situacao": situacao, "mensagem": mensagem}


def eficiencia(geracao, consumo):
    """Percentual do consumo coberto pela geracao."""
    if consumo == 0:
        return 100.0
    return round(geracao / consumo * 100, 1)
