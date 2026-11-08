"""Executa uma demonstração completa do sistema da colônia."""
import copy
import sys

# Cada módulo cuida de uma parte do trabalho.
import dados
import estruturas
import previsao
import analise_energia
import regras

# A configuração evita erros com caracteres acentuados em alguns terminais.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def titulo(texto):
    """Separa as etapas na saída do terminal."""
    print("\n" + "=" * 64)
    print(" " + texto)
    print("=" * 64)


def mostrar_dados(arvore):
    """Mostra o estado atual e como os sistemas estão organizados."""
    titulo("1) DADOS DA COLONIA")
    print("Estado atual (chave-valor):")
    for chave, valor in dados.estado_atual.items():  # Lê cada par do dicionário.
        print(f"   {chave:<20} = {valor}")

    print("\nHierarquia dos sistemas (arvore):")
    estruturas.imprimir_arvore(arvore)  # Percorre todos os níveis da árvore.

    indice = estruturas.criar_indice(arvore)  # Permite buscar pelo nome.
    print("\nBusca pela tabela hash, indice['Oxigenio']:",
          indice["Oxigenio"]["consumo"], "kWh, prioridade", indice["Oxigenio"]["prioridade"])

    solar = estruturas.navegar(arvore, ["Sistema Energetico", "Solar"])  # Exemplo de caminho.
    print("Navegacao pela Colonia, Sistema Energetico, Solar:", solar["nome"], "encontrado")


def fazer_previsoes(estado):
    """Estima geração e consumo usando os históricos."""
    titulo("2) PREVISAO (regressao linear)")

    # O histórico de vento determina a reta da geração eólica.
    a_e, b_e = previsao.ajustar_reta(dados.historico_vento, dados.historico_energia_eolica)
    eolica = previsao.prever(a_e, b_e, estado["vento_previsto"])  # Aplica o vento previsto.
    print(f"Eolica: energia = {a_e:.2f} * vento {b_e:+.2f}  "
          f"(erro medio {previsao.erro_medio(dados.historico_vento, dados.historico_energia_eolica, a_e, b_e):.2f})")
    print(f"   vento = {estado['vento_previsto']} m/s; previsao = {eolica:.1f} kWh")

    # A irradiação prevista alimenta a mesma conta para os painéis solares.
    a_s, b_s = previsao.ajustar_reta(dados.historico_irradiacao, dados.historico_energia_solar)
    solar = previsao.prever(a_s, b_s, estado["irradiacao_prevista"])
    if estado["tempestade_poeira"]:  # A poeira prejudica os painéis.
        solar = solar * 0.3  # Considera 30% da geração solar prevista.
    print(f"Solar:  energia = {a_s:.3f} * irradiacao {b_s:+.2f}")
    print(f"   irradiacao = {estado['irradiacao_prevista']} W/m2; previsao = {solar:.1f} kWh")

    consumo_prox, inclinacao = previsao.tendencia(dados.historico_consumo)  # Próxima hora.
    direcao = "subindo" if inclinacao > 0 else "caindo"  # Interpreta a inclinação.
    print(f"Consumo: tendencia {direcao} ({inclinacao:+.1f} kWh/h); proxima hora: {consumo_prox:.1f} kWh")

    # A geração total será usada na análise e nas regras.
    return {"eolica": eolica, "solar": solar, "total": eolica + solar, "consumo_previsto": consumo_prox}


def analisar(estado, previsoes):
    """Compara a geração prevista com o consumo atual."""
    titulo("3) ANALISE DE ENERGIA")
    resultado = analise_energia.analisar_energia(round(previsoes["total"], 1), estado["consumo"],
                                                 estado["energia_reserva"])
    # O saldo mostra quanto sobra ou falta na próxima hora.
    print(f"Geracao prevista: {resultado['geracao']} kWh | Consumo: {resultado['consumo']} kWh "
          f"| Saldo: {resultado['saldo']:+.1f} kWh")
    print(f"Cobertura: {analise_energia.eficiencia(resultado['geracao'], resultado['consumo'])}%")
    print("Resultado:", resultado["mensagem"])
    return resultado  # O diagnóstico também pode ser usado por outra etapa.


def decidir_e_agir(estado, previsoes, arvore):
    """Aplica as regras e atualiza os equipamentos quando preciso."""
    titulo("4) DECISAO AUTOMATICA")
    decisao = regras.decidir(estado, previsoes["total"])  # Considera o déficit previsto.
    print("Proposicoes:", ", ".join(f"{k}={'V' if v else 'F'}" for k, v in decisao["proposicoes"].items()))
    print("Modo:", decisao["modo"])
    for acao in decisao["acoes"]:  # Uma decisão pode gerar mais de um aviso.
        print("  Acao:", acao)

    if decisao["desligar_a_partir_de"] is not None:  # Só corta energia quando necessário.
        antes = estruturas.consumo_total(arvore)  # Consumo antes da ação.
        desligados = estruturas.desligar_por_prioridade(arvore, decisao["desligar_a_partir_de"])
        depois = estruturas.consumo_total(arvore)  # Consumo após o desligamento.
        print("\nSistemas desligados:", ", ".join(desligados))
        print(f"Consumo antes: {antes} kWh; depois: {depois} kWh; economia: {antes - depois} kWh")
        estado["consumo"] = depois  # Mantém o estado igual à árvore.

        nova = analise_energia.analisar_energia(round(previsoes["total"], 1), depois, estado["energia_reserva"])
        print("Nova analise:", nova["mensagem"])
        print("\nArvore apos a decisao:")
        estruturas.imprimir_arvore(arvore)  # Mostra os equipamentos desligados.
    return decisao


def executar_ciclo(estado, arvore):
    """Executa as quatro etapas na ordem usada pela colônia."""
    estado["consumo"] = estruturas.consumo_total(arvore)  # Lê o consumo da árvore.
    mostrar_dados(arvore)  # Apresenta o cenário inicial.
    previsoes = fazer_previsoes(estado)  # Calcula a próxima hora.
    analisar(estado, previsoes)  # Verifica o saldo de energia.
    decidir_e_agir(estado, previsoes, arvore)  # Escolhe e aplica a ação.


def exemplos_rapidos():
    """Mostra os exemplos simples pedidos no enunciado."""
    titulo("EXEMPLOS RAPIDOS DE ENTRADA E SAIDA")

    # Cada caso mostra como a reserva e o consumo mudam a decisão.
    casos = [{"energia_reserva": 40, "consumo": 70},
             {"energia_reserva": 45, "consumo": 50},
             {"energia_reserva": 15, "consumo": 40},
             {"energia_reserva": 80, "consumo": 30}]
    for caso in casos:
        decisao = regras.decidir(caso)  # Aplica as regras sem alterar a árvore.
        print(f"reserva={caso['energia_reserva']}%, consumo={caso['consumo']} kWh. Decisao: " + " | ".join(decisao["acoes"]))

    print()  # Separa os exemplos de análise.
    for geracao, consumo in [(40, 70), (80, 30), (60, 58)]:
        print(f"geracao={geracao} kWh, consumo={consumo} kWh. Analise: {analise_energia.analisar_energia(geracao, consumo)['mensagem']}")

    print()  # Separa o exemplo de regressão.
    inclinacao, valor_inicial = previsao.ajustar_reta([8, 10, 12], [20, 25, 30])
    print(f"vento=[8,10,12], energia=[20,25,30]. Reta: energia = {inclinacao}*vento + {valor_inicial}")
    print(f"vento = 11; previsao de energia = {previsao.prever(inclinacao, valor_inicial, 11)} kWh")


if __name__ == "__main__":  # Permite importar as funções sem rodar a demonstração.
    estado = copy.deepcopy(dados.estado_atual)  # Preserva os dados originais.
    arvore = copy.deepcopy(dados.arvore_colonia)  # Evita desligar a árvore original.
    executar_ciclo(estado, arvore)  # Mostra o ciclo completo.
    exemplos_rapidos()  # Confere os casos do enunciado.
