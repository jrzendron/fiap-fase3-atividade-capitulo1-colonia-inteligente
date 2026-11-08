"""
previsao.py - MODELO DE PREVISAO (regressao linear simples)

Ajusta uma reta  y = a*x + b  pelo metodo dos minimos quadrados:

    a = soma((x - media_x) * (y - media_y)) / soma((x - media_x)^2)
    b = media_y - a * media_x

Sem bibliotecas: so listas, laços e funcoes.
"""


def media(valores):
    return sum(valores) / len(valores)


def ajustar_reta(x, y):
    """Recebe duas listas do mesmo tamanho e retorna (a, b) da reta y = a*x + b."""
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("As listas precisam ter o mesmo tamanho (minimo 2 pontos).")

    mx = media(x)
    my = media(y)

    numerador = 0
    denominador = 0
    for i in range(len(x)):
        numerador = numerador + (x[i] - mx) * (y[i] - my)
        denominador = denominador + (x[i] - mx) ** 2

    a = numerador / denominador
    b = my - a * mx
    return a, b


def prever(a, b, x_novo):
    """Usa a reta para estimar um valor futuro."""
    return a * x_novo + b


def erro_medio(x, y, a, b):
    """Erro medio absoluto: quanto, em media, a reta erra nos dados historicos."""
    erros = []
    for i in range(len(x)):
        erros.append(abs(y[i] - prever(a, b, x[i])))
    return media(erros)


def tendencia(serie):
    """
    Previsao da PROXIMA posicao de uma serie temporal (ex.: consumo por hora).
    O eixo x vira o tempo: 0, 1, 2, ...
    """
    tempos = list(range(len(serie)))
    a, b = ajustar_reta(tempos, serie)
    return prever(a, b, len(serie)), a
