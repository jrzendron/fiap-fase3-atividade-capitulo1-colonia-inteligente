"""Gera três páginas editáveis no draw.io usando apenas a biblioteca padrão.

Rode este arquivo na pasta dos diagramas. Os pontos do gráfico são lidos do CSV.
Depois, abra figuras-aurora.drawio no draw.io para editar ou exportar as páginas.
"""
from pathlib import Path
import csv
import xml.etree.ElementTree as ET

PASTA = Path(__file__).resolve().parent
ROSA = '#E6005C'
ARQUIVO = PASTA / 'figuras-aurora.drawio'
mxfile = ET.Element('mxfile', host='app.diagrams.net', type='device', version='32.6.10')


def pagina(numero, nome, largura, altura):
    diagrama = ET.SubElement(mxfile, 'diagram', id=f'aurora-{numero}', name=nome)
    modelo = ET.SubElement(diagrama, 'mxGraphModel', dx='1200', dy='800', grid='1',
        gridSize='10', guides='1', tooltips='1', connect='1', arrows='1', fold='1',
        page='1', pageScale='1', pageWidth=str(largura), pageHeight=str(altura),
        math='0', shadow='0', background='#FFFFFF')
    raiz = ET.SubElement(modelo, 'root')
    ET.SubElement(raiz, 'mxCell', id='0')
    ET.SubElement(raiz, 'mxCell', id='1', parent='0')
    return raiz


def caixa(raiz, identificador, texto, x, y, largura, altura, destaque=False):
    estilo = ('rounded=1;arcSize=8;whiteSpace=wrap;html=0;'
        'fillColor=' + ('#F8EFF3' if destaque else '#F6F6F6') + ';'
        'strokeColor=#777777;strokeWidth=1;fontColor=#222222;fontFamily=Arial;'
        'fontSize=18;align=center;verticalAlign=middle;spacing=5;')
    return vertice(raiz, identificador, texto, x, y, largura, altura, estilo)


def vertice(raiz, identificador, texto, x, y, largura, altura, estilo):
    celula = ET.SubElement(raiz, 'mxCell', id=identificador, value=texto,
        style=estilo, vertex='1', parent='1')
    ET.SubElement(celula, 'mxGeometry', x=str(x), y=str(y),
        width=str(largura), height=str(altura), **{'as': 'geometry'})
    return celula


def texto(raiz, identificador, valor, x, y, largura, altura=30, cor='#222222', alinhar='center', tamanho=18):
    return vertice(raiz, identificador, valor, x, y, largura, altura,
        f'text;html=0;whiteSpace=wrap;strokeColor=none;fillColor=none;'
        f'fontFamily=Arial;fontSize={tamanho};fontColor={cor};align={alinhar};'
        'verticalAlign=middle;spacing=0;')


def ligar(raiz, identificador, origem, destino, estilo=''):
    c = ET.SubElement(raiz, 'mxCell', id=identificador, value='', edge='1', parent='1',
        source=origem, target=destino,
        style='edgeStyle=none;html=0;endArrow=open;endFill=0;strokeColor=#777777;strokeWidth=1.2;' + estilo)
    ET.SubElement(c, 'mxGeometry', relative='1', **{'as': 'geometry'})
    return c


def linha(raiz, identificador, x1, y1, x2, y2, cor='#777777', espessura=1, tracejada=False, seta=False):
    estilo = (f'html=0;endArrow={"open" if seta else "none"};endFill=0;'
        f'strokeColor={cor};strokeWidth={espessura};' + ('dashed=1;dashPattern=5 4;' if tracejada else ''))
    c = ET.SubElement(raiz, 'mxCell', id=identificador, value='', edge='1', parent='1', style=estilo)
    g = ET.SubElement(c, 'mxGeometry', relative='1', **{'as': 'geometry'})
    ET.SubElement(g, 'mxPoint', x=str(x1), y=str(y1), **{'as': 'sourcePoint'})
    ET.SubElement(g, 'mxPoint', x=str(x2), y=str(y2), **{'as': 'targetPoint'})
    return c


# Página 1: cada caixa, texto e ligação pode ser editado separadamente.
r = pagina(1, '1 Dados da colônia', 1000, 270)
caixa(r, 'colonia', 'Colônia Aurora', 390, 15, 220, 48, True)
filhos = [
    ('energia', 'Energia', 'Reserva e geração\nsolar / eólica', 20),
    ('clima', 'Clima', 'Vento e\ntemperatura', 275),
    ('sistemas', 'Sistemas', 'Essenciais e\nnão essenciais', 530),
    ('historico', 'Histórico', 'Listas de vento\ne energia', 785),
]
for nome, titulo, detalhe, x in filhos:
    caixa(r, nome, titulo, x, 125, 195, 45)
    ligar(r, 'liga-' + nome, 'colonia', nome,
        'exitX=0.5;exitY=1;entryX=0.5;entryY=0;')
    texto(r, 'detalhe-' + nome, detalhe, x - 4, 188, 203, 54, tamanho=17)

# Página 2: gráfico formado por linhas, pontos, eixos e textos do draw.io.
with (PASTA / 'dados-regressao.csv').open(encoding='utf-8', newline='') as f:
    pares = [(float(i['vento_ms']), float(i['energia_kwh'])) for i in csv.DictReader(f)]
if len(pares) < 2:
    raise ValueError('O CSV precisa ter pelo menos dois pares de valores.')
x = [a for a, _ in pares]
y = [b for _, b in pares]
media_x = sum(x) / len(x)
media_y = sum(y) / len(y)
denominador = sum((a - media_x) ** 2 for a in x)
if denominador == 0:
    raise ValueError('O histórico precisa ter ventos diferentes.')
b1 = sum((a - media_x) * (b - media_y) for a, b in pares) / denominador
b0 = media_y - b1 * media_x
vento_previsto = 11
energia_prevista = b0 + b1 * vento_previsto

r = pagina(2, '2 Gráfico da regressão', 1000, 470)
min_x, max_x = min(x) - .5, max(x) + .5
min_y, max_y = min(y) - 2, max(y) + 2


def px(valor):
    return 95 + (valor - min_x) / (max_x - min_x) * 865


def py(valor):
    return 360 - (valor - min_y) / (max_y - min_y) * 310


texto(r, 'eixo-y-titulo', 'Energia eólica (kWh)', 95, 0, 500, 32, alinhar='left')
for i, vento in enumerate(x):
    xx = px(vento)
    linha(r, f'grade-x-{i}', xx, 50, xx, 360, '#E4E4E4', .8)
    texto(r, f'valor-x-{i}', f'{vento:g}'.replace('.', ','), xx - 30, 370, 60)
for i, energia in enumerate(sorted(set(y))):
    yy = py(energia)
    linha(r, f'grade-y-{i}', 95, yy, 960, yy, '#E4E4E4', .8)
    texto(r, f'valor-y-{i}', f'{energia:g}'.replace('.', ','), 25, yy - 15, 55, alinhar='right')
linha(r, 'eixo-x', 95, 360, 960, 360, '#333333', 1.5)
linha(r, 'eixo-y', 95, 50, 95, 360, '#333333', 1.5)
linha(r, 'reta-regressao', px(min(x)), py(b0 + b1 * min(x)),
    px(max(x)), py(b0 + b1 * max(x)), '#252525', 2.4)
linha(r, 'guia-vento', px(vento_previsto), 360,
    px(vento_previsto), py(energia_prevista), '#999999', 1, True)
linha(r, 'guia-energia', 95, py(energia_prevista),
    px(vento_previsto), py(energia_prevista), '#999999', 1, True)
for i, (vento, energia) in enumerate(pares):
    vertice(r, f'ponto-{i}', '', px(vento) - 5, py(energia) - 5, 10, 10,
        'ellipse;fillColor=#252525;strokeColor=#252525;')
vertice(r, 'ponto-previsto', '', px(vento_previsto) - 6, py(energia_prevista) - 6, 12, 12,
    f'ellipse;fillColor={ROSA};strokeColor={ROSA};')
texto(r, 'previsao-texto', f'11 m/s = {energia_prevista:g} kWh'.replace('.', ','),
    175, 65, 310, 35, cor=ROSA, alinhar='left', tamanho=20)
linha(r, 'previsao-seta', 460, 94, px(vento_previsto) - 8,
    py(energia_prevista) - 5, ROSA, 1.1, seta=True)
linha(r, 'legenda-reta', 705, 285, 744, 285, '#252525', 2.4)
texto(r, 'legenda-reta-texto', f'Reta y = {b0:g} + {b1:g}x'.replace('.', ','),
    755, 270, 200, alinhar='left', tamanho=16)
vertice(r, 'legenda-ponto', '', 719, 316, 10, 10,
    'ellipse;fillColor=#252525;strokeColor=#252525;')
texto(r, 'legenda-ponto-texto', 'Valores do exemplo', 755, 306, 200, alinhar='left', tamanho=16)
texto(r, 'eixo-x-titulo', 'Vento (m/s)', 355, 420, 350, 35, tamanho=20)

# Página 3: as setas ficam ligadas às caixas ao movê-las no editor.
r = pagina(3, '3 Fluxo do sistema', 1000, 265)
etapas = [
    ('entrada', 'Receber os dados', 10, 15),
    ('organizar', 'Organizar e conferir', 370, 15),
    ('prever', 'Calcular a previsão', 730, 15),
    ('decidir', 'Aplicar as regras', 730, 185),
    ('priorizar', 'Manter os essenciais', 370, 185),
    ('saida', 'Mostrar saldo e ações', 10, 185),
]
for nome, titulo, x, y in etapas:
    caixa(r, nome, titulo, x, y, 260, 55, nome == 'decidir')
for i, (origem, destino) in enumerate([('entrada','organizar'),('organizar','prever'),
    ('prever','decidir'),('decidir','priorizar'),('priorizar','saida')]):
    ligar(r, f'fluxo-{i}', origem, destino)

ET.indent(mxfile, space='  ')
ET.ElementTree(mxfile).write(ARQUIVO, encoding='utf-8', xml_declaration=True)
print(f'Arquivo criado: {ARQUIVO}')
print(f'Regressão: b0={b0:g}; b1={b1:g}; previsão={energia_prevista:g} kWh')
