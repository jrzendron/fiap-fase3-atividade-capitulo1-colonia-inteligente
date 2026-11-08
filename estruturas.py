"""Funções para consultar e atualizar a hierarquia da colônia."""


def imprimir_arvore(no, nivel=0):
    """Mostra cada sistema e, logo abaixo, seus equipamentos."""
    status = "ON " if no["ligado"] else "OFF"  # Traduz o estado para a tela.
    info = ""  # Grupos não têm consumo nem prioridade próprios.
    if no["prioridade"] is not None:  # Só equipamentos mostram esses dados.
        info = f"  [prio {no['prioridade']} | {status} | {no['consumo']} kWh]"
    print("   " * nivel + no["nome"] + info)  # Indenta pelo nível.
    for filho in no["filhos"]:  # Visita os itens dentro do grupo.
        imprimir_arvore(filho, nivel + 1)  # O filho aparece um nível abaixo.


def listar_folhas(no):
    """Devolve somente os equipamentos, sem os grupos da árvore."""
    if len(no["filhos"]) == 0:  # Um item sem filhos é um equipamento.
        return [no]  # A lista permite juntar resultados de vários ramos.
    folhas = []  # Guarda os equipamentos encontrados neste grupo.
    for filho in no["filhos"]:  # Percorre cada ramo.
        folhas = folhas + listar_folhas(filho)  # Junta os equipamentos do ramo.
    return folhas  # Entrega a lista completa.


def criar_indice(no, indice=None):
    """Cria uma busca por nome usando um dicionário."""
    if indice is None:  # A primeira chamada ainda não tem índice.
        indice = {}  # As chamadas seguintes compartilham este dicionário.
    indice[no["nome"]] = no  # O nome aponta para o item da árvore.
    for filho in no["filhos"]:  # Inclui também os itens dos outros níveis.
        criar_indice(filho, indice)
    return indice  # Devolve o índice preenchido.


def navegar(arvore, caminho):
    """Segue uma sequência de nomes até encontrar o equipamento."""
    atual = arvore  # Começa na colônia.
    for nome in caminho:  # Cada nome representa o próximo nível.
        encontrado = None  # Marca que o próximo nível ainda não foi achado.
        for filho in atual["filhos"]:  # Procura entre os filhos do nível atual.
            if filho["nome"] == nome:  # Encontrou o nome solicitado.
                encontrado = filho
        if encontrado is None:  # Um nome ausente interrompe a busca.
            return None
        atual = encontrado  # Continua a partir do item encontrado.
    return atual  # Devolve o último item do caminho.


def consumo_total(arvore):
    """Soma o consumo dos equipamentos ligados."""
    total = 0  # Acumula o consumo em kWh.
    for equipamento in listar_folhas(arvore):  # Ignora os grupos.
        if equipamento["ligado"]:  # Equipamentos desligados não consomem.
            total = total + equipamento["consumo"]
    return total


def desligar_por_prioridade(arvore, prioridade_minima):
    """Desliga prioridades menos importantes e preserva a prioridade 1."""
    desligados = []  # Registra os nomes para mostrar a decisão.
    for equipamento in listar_folhas(arvore):  # Verifica cada equipamento.
        prioridade = equipamento["prioridade"]
        if prioridade is not None and prioridade != 1 and prioridade >= prioridade_minima and equipamento["ligado"]:
            equipamento["ligado"] = False  # Atualiza o estado na árvore.
            desligados.append(equipamento["nome"])  # Guarda o que foi desligado.
    return desligados
