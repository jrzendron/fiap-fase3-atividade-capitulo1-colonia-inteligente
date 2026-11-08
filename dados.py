"""Dados usados na simulação da colônia."""

# Este dicionário reúne as leituras do cenário inicial.
estado_atual = {
    "energia_reserva": 40,      # Carga atual das baterias, em porcentagem.
    "consumo": 70,              # Energia consumida em uma hora, em kWh.
    "temperatura": -63,         # Temperatura externa, em graus Celsius.
    "vento_previsto": 11,       # Vento esperado na próxima hora, em m/s.
    "irradiacao_prevista": 450, # Irradiação esperada, em W/m2.
    "tempestade_poeira": False, # Indica se há uma tempestade de poeira.
}

# Cada posição das listas abaixo representa a mesma medição histórica.
historico_vento = [8, 10, 12, 6, 14]             # Vento, em m/s.
historico_energia_eolica = [20, 26, 29, 14, 36]  # Geração eólica, em kWh.

historico_irradiacao = [200, 300, 400, 500, 600] # Irradiação, em W/m2.
historico_energia_solar = [11, 14, 21, 24, 31]   # Geração solar, em kWh.

historico_consumo = [55, 60, 58, 65, 70]          # Consumo nas últimas cinco horas.

# Cada item da hierarquia usa o mesmo formato.
def no(nome, prioridade=None, consumo=0, filhos=None):
    """Monta um sistema ou equipamento da colônia."""
    return {
        "nome": nome,                             # Nome mostrado na árvore.
        "prioridade": prioridade,                 # 1 é essencial; 3 é dispensável.
        "consumo": consumo,                       # Consumo do equipamento em kWh.
        "ligado": True,                          # Todos começam ligados.
        "filhos": filhos if filhos is not None else [], # Lista vazia para equipamentos.
    }


# Os grupos organizam os equipamentos por função.
arvore_colonia = no("Colonia", filhos=[
    no("Sistema Energetico", filhos=[
        no("Solar", prioridade=1),                 # Fonte solar.
        no("Eolico", prioridade=1),                # Fonte eólica.
        no("Baterias", prioridade=1),              # Reserva de energia.
    ]),
    no("Suporte a Vida", filhos=[
        no("Oxigenio", prioridade=1, consumo=15),  # Mantém o ar respirável.
        no("Aquecimento", prioridade=1, consumo=12), # Mantém a temperatura.
        no("Agua", prioridade=1, consumo=8),       # Mantém o fornecimento de água.
    ]),
    no("Producao", filhos=[
        no("Estufa", prioridade=2, consumo=10),    # Produção de alimentos.
        no("Laboratorio", prioridade=3, consumo=9), # Pesquisa não essencial.
    ]),
    no("Conforto", filhos=[
        no("Iluminacao Decorativa", prioridade=3, consumo=6), # Iluminação extra.
        no("Entretenimento", prioridade=3, consumo=10),      # Uso recreativo.
    ]),
])
