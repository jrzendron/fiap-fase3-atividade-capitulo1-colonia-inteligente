# FIAP Fase 3: Atividade do Capítulo 1, Colônia Inteligente

Sistema em Python que organiza os dados de uma colônia, estima a geração de energia e define ações para equilibrar geração e consumo. O programa usa apenas a biblioteca padrão do Python.

Implementação inicial: Gabriel Hampel Meireles. Organização da entrega da Fase 3: Ronei Lach.

## Como executar

Na pasta do repositório, execute:

```bash
python3 main.py
```

No Windows, com o lançador `py` instalado:

```bash
py -3 main.py
```

O programa mostra os dados da colônia, a previsão de geração, a análise de energia e a decisão tomada. Ao final, apresenta exemplos com entradas e saídas conhecidas.

## Arquivos da entrega

| Arquivo | Função |
| --- | --- |
| `dados.py` | Estado da colônia, históricos e hierarquia dos sistemas. |
| `estruturas.py` | Navegação na hierarquia, cálculo de consumo e desligamento por prioridade. |
| `previsao.py` | Regressão linear simples para estimar a geração. |
| `analise_energia.py` | Comparação entre geração, consumo e nível da reserva. |
| `regras.py` | Condições e ações de cada modo de operação. |
| `main.py` | Integra as etapas e apresenta os resultados. |
| `relatorio/relatorio.pdf` | Relatório da atividade. |

## Dados e decisões

Os históricos de vento, irradiação e consumo ficam em listas. O estado atual usa um dicionário. Outro conjunto de dicionários representa a hierarquia da colônia: sistema energético, suporte à vida, produção e conforto. Cada equipamento tem prioridade, consumo e indicação de ligado ou desligado.

A reserva é medida em porcentagem; geração e consumo são medidos em kWh. Em emergência, o programa desliga equipamentos de prioridades 2 e 3. Em modo de economia, desliga os de prioridade 3. Equipamentos essenciais, como oxigênio e aquecimento, permanecem ligados.

As principais regras são:

- Reserva abaixo de 20%, ou temperatura abaixo de −80 °C com reserva abaixo de 50%: emergência.
- Fora da emergência, reserva abaixo de 50% e demanda acima de 60 kWh: modo de economia.
- Reserva abaixo de 50%: alerta para reduzir o consumo.
- Geração prevista abaixo da demanda de referência, com reserva de pelo menos 50%: modo de atenção e aviso preventivo.

## Previsão e análise de energia

`previsao.py` ajusta uma reta aos dados históricos por mínimos quadrados. A previsão de vento alimenta a estimativa de energia eólica; a irradiação alimenta a estimativa solar. O programa compara a geração prevista à demanda de referência e calcula o saldo. O saldo da próxima hora usa a demanda dos equipamentos atualmente ligados, supondo que permaneçam ligados durante esse período. A estimativa de consumo pela tendência histórica é apenas informativa e fica fora do saldo. Se houver déficit, emite um alerta. Se houver excedente, sugere armazenar energia.

## Exemplos de entrada e saída

```text
reserva=40%, consumo=70 kWh. Decisão: modo de economia e alerta para reduzir o consumo
geração=40 kWh, consumo=70 kWh. Análise: consumo maior que geração
geração=80 kWh, consumo=30 kWh. Análise: armazenar energia excedente
vento=[8, 10, 12], energia=[20, 25, 30], vento previsto=11. Previsão: 27,5 kWh
```

O cenário completo do programa está em `saida_exemplo.txt`.

## Limites da simulação

Os históricos e o estado inicial são exemplos fixos em `dados.py`. O programa executa um ciclo de demonstração; não coleta dados de sensores nem controla equipamentos reais. A previsão é uma estimativa linear baseada nesses exemplos.
