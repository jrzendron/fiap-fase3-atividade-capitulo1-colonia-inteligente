"""Compara a energia gerada com a energia consumida."""

MARGEM_EQUILIBRIO = 5  # Até 5 kWh de diferença é considerado equilíbrio.


def analisar_energia(geracao, consumo, reserva=None):
    """Devolve o saldo, a situação e uma mensagem para a equipe."""
    saldo = geracao - consumo  # Saldo positivo indica sobra de energia.

    if abs(saldo) <= MARGEM_EQUILIBRIO:  # Diferença pequena não exige ação.
        situacao = "EQUILIBRIO"  # Identifica o caso para outras regras.
        mensagem = "OK: geracao e consumo equilibrados"
    elif consumo > geracao:  # A colônia usa mais do que gera.
        situacao = "DEFICIT"  # O saldo negativo pede atenção.
        mensagem = "ALERTA: consumo maior que geracao"
    else:  # A geração supera o consumo.
        situacao = "EXCEDENTE"  # Há energia disponível para guardar.
        mensagem = "SUGESTAO: armazenar energia excedente"

    # A reserva, quando informada, detalha o risco do déficit.
    if reserva is not None and situacao == "DEFICIT":
        if reserva < 20:  # A bateria está em nível crítico.
            mensagem += " e reserva CRITICA"
        elif reserva < 50:  # Ainda há reserva, mas ela está baixa.
            mensagem += " e reserva baixa"
        else:  # A bateria tem pelo menos metade da carga.
            mensagem += " (reserva de pelo menos 50%)"

    if reserva is not None and situacao == "EXCEDENTE" and reserva >= 100:  # Baterias cheias.
        mensagem = "SUGESTAO: baterias cheias; ligar sistemas nao essenciais ou a estufa"

    # Mantém os números junto da classificação para uso no relatório da execução.
    return {"geracao": geracao, "consumo": consumo, "saldo": saldo,
            "situacao": situacao, "mensagem": mensagem}


def eficiencia(geracao, consumo):
    """Calcula quanto do consumo a geração consegue cobrir."""
    if consumo == 0:  # Evita divisão por zero quando não há consumo.
        return 100.0
    return round(geracao / consumo * 100, 1)  # Mostra uma casa decimal.
