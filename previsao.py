"""Cálculos de regressão linear usados nas previsões."""


def media(valores):
    """Calcula a média dos valores recebidos."""
    return sum(valores) / len(valores)  # Soma os valores e divide pela quantidade.


def ajustar_reta(x, y):
    """Encontra a inclinação e o ponto inicial da reta que aproxima os dados."""
    if len(x) != len(y) or len(x) < 2:  # Cada entrada precisa ter uma saída.
        raise ValueError("As listas precisam ter o mesmo tamanho (minimo 2 pontos).")

    mx = media(x)  # Centro dos valores de entrada.
    my = media(y)  # Centro dos valores de saída.

    numerador = 0  # Mede como entrada e saída variam juntas.
    denominador = 0  # Mede a variação das entradas.
    for i in range(len(x)):  # Usa todas as medições históricas.
        numerador = numerador + (x[i] - mx) * (y[i] - my)
        denominador = denominador + (x[i] - mx) ** 2

    a = numerador / denominador  # Inclinação da reta.
    b = my - a * mx  # Valor onde a reta começa.
    return a, b  # Esses dois números permitem prever outro ponto.


def prever(a, b, x_novo):
    """Aplica a reta a um novo valor de entrada."""
    return a * x_novo + b  # Exemplo: vento previsto vira energia estimada.


def erro_medio(x, y, a, b):
    """Mostra a diferença média entre a reta e os dados conhecidos."""
    erros = []  # Guarda o erro de cada medição.
    for i in range(len(x)):  # Compara previsão e resultado real.
        erros.append(abs(y[i] - prever(a, b, x[i])))
    return media(erros)  # Resume os erros em um único valor.


def tendencia(serie):
    """Estima o próximo valor de uma sequência, como o consumo por hora."""
    tempos = list(range(len(serie)))  # Numera as horas a partir de zero.
    a, b = ajustar_reta(tempos, serie)  # Ajusta a reta ao histórico.
    return prever(a, b, len(serie)), a  # Devolve a próxima hora e a tendência.
