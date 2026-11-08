"""
estruturas.py - FUNCOES PARA NAVEGAR NOS DADOS
  - percorrer a arvore de sistemas (recursao)
  - montar uma tabela hash (dicionario) nome -> no, para busca rapida
  - somar consumo, ligar/desligar por prioridade
"""


def imprimir_arvore(no, nivel=0):
    """Mostra a hierarquia com indentacao (percurso em pre-ordem, recursivo)."""
    status = "ON " if no["ligado"] else "OFF"
    info = ""
    if no["prioridade"] is not None:
        info = f"  [prio {no['prioridade']} | {status} | {no['consumo']} kWh]"
    print("   " * nivel + "- " + no["nome"] + info)
    for filho in no["filhos"]:
        imprimir_arvore(filho, nivel + 1)


def listar_folhas(no):
    """Retorna uma LISTA com todos os equipamentos (nos sem filhos)."""
    if len(no["filhos"]) == 0:
        return [no]
    folhas = []
    for filho in no["filhos"]:
        folhas = folhas + listar_folhas(filho)
    return folhas


def criar_indice(no, indice=None):
    """
    Cria uma TABELA HASH (dicionario) nome -> no.
    Assim, buscar 'Oxigenio' e O(1) em vez de percorrer a arvore toda (O(n)).
    """
    if indice is None:
        indice = {}
    indice[no["nome"]] = no
    for filho in no["filhos"]:
        criar_indice(filho, indice)
    return indice


def navegar(arvore, caminho):
    """
    Navega pela arvore seguindo um caminho, ex.:
    navegar(arvore, ["Sistema Energetico", "Solar"])
    Retorna o no encontrado ou None.
    """
    atual = arvore
    for nome in caminho:
        encontrado = None
        for filho in atual["filhos"]:
            if filho["nome"] == nome:
                encontrado = filho
        if encontrado is None:
            return None
        atual = encontrado
    return atual


def consumo_total(arvore):
    """Soma o consumo dos equipamentos que estao LIGADOS."""
    total = 0
    for equipamento in listar_folhas(arvore):
        if equipamento["ligado"]:
            total = total + equipamento["consumo"]
    return total


def desligar_por_prioridade(arvore, prioridade_minima):
    """
    Desliga todo equipamento com prioridade >= prioridade_minima.
    Prioridade 1 (suporte a vida) NUNCA e desligada.
    Retorna a lista de nomes desligados.
    """
    desligados = []
    for equipamento in listar_folhas(arvore):
        p = equipamento["prioridade"]
        if p is not None and p != 1 and p >= prioridade_minima and equipamento["ligado"]:
            equipamento["ligado"] = False
            desligados.append(equipamento["nome"])
    return desligados
