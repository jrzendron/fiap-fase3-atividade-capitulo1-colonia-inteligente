"""
main.py - SISTEMA INTEGRADO DA COLONIA
Junta as tres camadas:
    DADOS (dados.py)  ->  LOGICA (estruturas, previsao, analise)  ->  DECISAO (regras.py)

Execute:  python main.py
"""
import copy
import sys

import dados
import estruturas
import previsao
import analise_energia
import regras

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def titulo(texto):
    print("\n" + "=" * 64)
    print(" " + texto)
    print("=" * 64)


# ------------------------------------------------------------------
# ETAPA 1 - ORGANIZAR OS DADOS
# ------------------------------------------------------------------
def mostrar_dados(arvore):
    titulo("1) DADOS DA COLONIA")
    print("Estado atual (chave-valor):")
    for chave, valor in dados.estado_atual.items():
        print(f"   {chave:<20} = {valor}")

    print("\nHierarquia dos sistemas (arvore):")
    estruturas.imprimir_arvore(arvore)

    indice = estruturas.criar_indice(arvore)
    print("\nBusca pela tabela hash -> indice['Oxigenio']:",
          indice["Oxigenio"]["consumo"], "kWh, prioridade", indice["Oxigenio"]["prioridade"])

    solar = estruturas.navegar(arvore, ["Sistema Energetico", "Solar"])
    print("Navegacao Colonia > Sistema Energetico > Solar:", solar["nome"], "encontrado")


# ------------------------------------------------------------------
# ETAPA 2 - PREVER (regressao)
# ------------------------------------------------------------------
def fazer_previsoes(estado):
    titulo("2) PREVISAO (regressao linear)")

    a_e, b_e = previsao.ajustar_reta(dados.historico_vento, dados.historico_energia_eolica)
    eolica = previsao.prever(a_e, b_e, estado["vento_previsto"])
    print(f"Eolica: energia = {a_e:.2f} * vento {b_e:+.2f}  "
          f"(erro medio {previsao.erro_medio(dados.historico_vento, dados.historico_energia_eolica, a_e, b_e):.2f})")
    print(f"   vento = {estado['vento_previsto']} m/s  ->  previsao = {eolica:.1f} kWh")

    a_s, b_s = previsao.ajustar_reta(dados.historico_irradiacao, dados.historico_energia_solar)
    solar = previsao.prever(a_s, b_s, estado["irradiacao_prevista"])
    if estado["tempestade_poeira"]:
        solar = solar * 0.3  # poeira cobre os paineis: 30% da geracao
    print(f"Solar:  energia = {a_s:.3f} * irradiacao {b_s:+.2f}")
    print(f"   irradiacao = {estado['irradiacao_prevista']} W/m2  ->  previsao = {solar:.1f} kWh")

    consumo_prox, inclinacao = previsao.tendencia(dados.historico_consumo)
    direcao = "subindo" if inclinacao > 0 else "caindo"
    print(f"Consumo: tendencia {direcao} ({inclinacao:+.1f} kWh/h) -> proxima hora ~ {consumo_prox:.1f} kWh")

    return {"eolica": eolica, "solar": solar, "total": eolica + solar, "consumo_previsto": consumo_prox}


# ------------------------------------------------------------------
# ETAPA 3 - ANALISAR ENERGIA
# ------------------------------------------------------------------
def analisar(estado, prev):
    titulo("3) ANALISE DE ENERGIA")
    resultado = analise_energia.analisar_energia(round(prev["total"], 1), estado["consumo"],
                                                 estado["energia_reserva"])
    print(f"Geracao prevista: {resultado['geracao']} kWh | Consumo: {resultado['consumo']} kWh "
          f"| Saldo: {resultado['saldo']:+.1f} kWh")
    print(f"Cobertura: {analise_energia.eficiencia(resultado['geracao'], resultado['consumo'])}%")
    print("Saida ->", resultado["mensagem"])
    return resultado


# ------------------------------------------------------------------
# ETAPA 4 - DECIDIR E AGIR
# ------------------------------------------------------------------
def decidir_e_agir(estado, prev, arvore):
    titulo("4) DECISAO AUTOMATICA")
    decisao = regras.decidir(estado, prev["total"])
    print("Proposicoes:", ", ".join(f"{k}={'V' if v else 'F'}" for k, v in decisao["proposicoes"].items()))
    print("Modo:", decisao["modo"])
    for acao in decisao["acoes"]:
        print("  ->", acao)

    if decisao["desligar_a_partir_de"] is not None:
        antes = estruturas.consumo_total(arvore)
        desligados = estruturas.desligar_por_prioridade(arvore, decisao["desligar_a_partir_de"])
        depois = estruturas.consumo_total(arvore)
        print("\nSistemas desligados:", ", ".join(desligados))
        print(f"Consumo: {antes} kWh -> {depois} kWh (economia de {antes - depois} kWh)")
        estado["consumo"] = depois

        nova = analise_energia.analisar_energia(round(prev["total"], 1), depois, estado["energia_reserva"])
        print("Nova analise ->", nova["mensagem"])
        print("\nArvore apos a decisao:")
        estruturas.imprimir_arvore(arvore)
    return decisao


# ------------------------------------------------------------------
def executar_ciclo(estado, arvore):
    """Um ciclo completo: dados -> previsao -> analise -> decisao."""
    estado["consumo"] = estruturas.consumo_total(arvore)  # consumo vem da arvore
    mostrar_dados(arvore)
    prev = fazer_previsoes(estado)
    analisar(estado, prev)
    decidir_e_agir(estado, prev, arvore)


def exemplos_rapidos():
    """Exemplos de entrada -> saida pedidos no enunciado."""
    titulo("EXEMPLOS RAPIDOS (entrada -> saida)")

    casos = [{"energia_reserva": 40, "consumo": 70},
             {"energia_reserva": 45, "consumo": 50},
             {"energia_reserva": 15, "consumo": 40},
             {"energia_reserva": 80, "consumo": 30}]
    for caso in casos:
        d = regras.decidir(caso)
        print(f"energia={caso['energia_reserva']}, consumo={caso['consumo']}  ->  " + " | ".join(d["acoes"]))

    print()
    for g, c in [(40, 70), (80, 30), (60, 58)]:
        print(f"geracao={g}, consumo={c}  ->  {analise_energia.analisar_energia(g, c)['mensagem']}")

    print()
    a, b = previsao.ajustar_reta([8, 10, 12], [20, 25, 30])
    print(f"vento=[8,10,12], energia=[20,25,30] -> reta: energia = {a}*vento + {b}")
    print(f"vento = 11  ->  previsao de energia ~ {previsao.prever(a, b, 11)}")


if __name__ == "__main__":
    estado = copy.deepcopy(dados.estado_atual)
    arvore = copy.deepcopy(dados.arvore_colonia)
    executar_ciclo(estado, arvore)
    exemplos_rapidos()
