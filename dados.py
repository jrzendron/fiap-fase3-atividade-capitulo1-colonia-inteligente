"""
dados.py - CAMADA DE DADOS
Aqui ficam SOMENTE os dados da colonia (nada de regra de decisao).

Estruturas usadas:
  - listas  -> series historicas (vento, energia, consumo...)
  - dicionario (tabela chave-valor / hash) -> estado atual e catalogo de subsistemas
  - arvore (dicionarios aninhados com "filhos") -> hierarquia dos sistemas
"""

# ---------------------------------------------------------------
# 1) ESTADO ATUAL DA COLONIA (chave-valor)
#    Reserva em %, consumo e geracao em kWh, temperatura em C
# ---------------------------------------------------------------
estado_atual = {
    "energia_reserva": 40,     # nivel da bateria em %
    "consumo": 70,             # consumo atual da colonia (kWh)
    "temperatura": -63,        # temperatura externa (C)
    "vento_previsto": 11,      # previsao de vento p/ proxima hora (m/s)
    "irradiacao_prevista": 450,# previsao de irradiacao solar (W/m2)
    "tempestade_poeira": False,
}

# ---------------------------------------------------------------
# 2) HISTORICO (listas paralelas: o indice i de uma lista
#    corresponde ao indice i da outra)
# ---------------------------------------------------------------
historico_vento = [8, 10, 12, 6, 14]             # m/s
historico_energia_eolica = [20, 26, 29, 14, 36]  # kWh gerados

historico_irradiacao = [200, 300, 400, 500, 600]   # W/m2
historico_energia_solar = [11, 14, 21, 24, 31]     # kWh gerados

historico_consumo = [55, 60, 58, 65, 70]           # kWh (ultimas 5 horas)

# ---------------------------------------------------------------
# 3) HIERARQUIA DOS SISTEMAS (arvore)
#    Cada no e um dicionario:  nome, prioridade, ligado, consumo, filhos
#    prioridade: 1 = ESSENCIAL (nunca desliga), 2 = importante, 3 = nao essencial
#    Nos "folha" sao os equipamentos que consomem/geram energia.
# ---------------------------------------------------------------
def no(nome, prioridade=None, consumo=0, filhos=None):
    """Cria um no da arvore (funcao auxiliar para nao repetir codigo)."""
    return {
        "nome": nome,
        "prioridade": prioridade,
        "consumo": consumo,
        "ligado": True,
        "filhos": filhos if filhos is not None else [],
    }


arvore_colonia = no("Colonia", filhos=[
    no("Sistema Energetico", filhos=[
        no("Solar", prioridade=1),
        no("Eolico", prioridade=1),
        no("Baterias", prioridade=1),
    ]),
    no("Suporte a Vida", filhos=[
        no("Oxigenio", prioridade=1, consumo=15),
        no("Aquecimento", prioridade=1, consumo=12),
        no("Agua", prioridade=1, consumo=8),
    ]),
    no("Producao", filhos=[
        no("Estufa", prioridade=2, consumo=10),
        no("Laboratorio", prioridade=3, consumo=9),
    ]),
    no("Conforto", filhos=[
        no("Iluminacao Decorativa", prioridade=3, consumo=6),
        no("Entretenimento", prioridade=3, consumo=10),
    ]),
])
