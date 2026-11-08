"""Cálculos de regressão linear (mínimos quadrados) usados nas previsões."""


def media(valores):
    """Calcula a média dos valores recebidos."""
    return sum(valores) / len(valores)  # Soma os valores e divide pela quantidade.


def ajustar_reta(x, y):
    """Encontra β0 (intercepto) e β1 (inclinação) da reta ŷ = β0 + β1·x."""
    if len(x) != len(y) or len(x) < 2:  # Cada entrada precisa ter uma saída.
        raise ValueError("As listas precisam ter o mesmo tamanho (minimo 2 pontos).")

    x_barra = media(x)  # x̄: centro dos valores de entrada.
    y_barra = media(y)  # ȳ: centro dos valores de saída.

    soma_produtos = 0     # Σ(xi − x̄)(yi − ȳ): como entrada e saída variam juntas.
    soma_quadrados_x = 0  # Σ(xi − x̄)²: variação das entradas.
    for i in range(len(x)):  # Usa todas as medições históricas.
        soma_produtos = soma_produtos + (x[i] - x_barra) * (y[i] - y_barra)
        soma_quadrados_x = soma_quadrados_x + (x[i] - x_barra) ** 2

    if soma_quadrados_x == 0:  # Entradas iguais não definem a inclinação.
        raise ValueError("O historico precisa ter pelo menos dois valores distintos de entrada.")
    beta1 = soma_produtos / soma_quadrados_x  # β1: inclinação da reta.
    beta0 = y_barra - beta1 * x_barra         # β0: intercepto (valor de y quando x = 0).
    return beta0, beta1  # Mesma ordem do capítulo: ŷ = β0 + β1·x


def prever(beta0, beta1, x_novo):
    """Aplica a reta ŷ = β0 + β1·x a um novo valor de entrada."""
    return beta0 + beta1 * x_novo  # Exemplo: vento previsto vira energia estimada.


def erro_medio(x, y, beta0, beta1):
    """Erro absoluto médio; resíduo = valor observado − valor previsto (ei = yi − ŷi)."""
    residuos = []  # Guarda o resíduo de cada medição.
    for i in range(len(x)):  # Compara valor real e previsto.
        residuo = y[i] - prever(beta0, beta1, x[i])
        residuos.append(abs(residuo))
    return media(residuos)  # Resume os resíduos em um único valor.


def tendencia(serie):
    """Estima o próximo valor de uma sequência, como o consumo por hora."""
    tempos = list(range(len(serie)))  # Numera as horas a partir de zero.
    beta0, beta1 = ajustar_reta(tempos, serie)  # Ajusta a reta ao histórico.
    return prever(beta0, beta1, len(serie)), beta1  # Próxima hora e a inclinação (tendência).