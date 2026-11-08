# Figuras do relatório da Aurora

Abra **figuras-aurora.drawio** em [app.diagrams.net](https://app.diagrams.net/).
Escolha **Dispositivo** e depois **Abrir diagrama existente**.

O arquivo tem três páginas, que aparecem nas abas do editor:

1. Dados da colônia.
2. Gráfico da regressão.
3. Fluxo do sistema.

Caixas, setas, pontos, linhas e textos podem ser editados. O gráfico não é uma
imagem colada: seus elementos também são formas do draw.io.

Para gerar uma imagem, escolha a aba desejada e use **Arquivo → Exportar como →
PNG** ou **SVG**. As imagens PNG desta pasta foram exportadas pelo draw.io e são
as mesmas usadas no relatório. Os arquivos SVG também podem ser abertos no editor.

## Mudar os dados do gráfico

Os valores estão em `dados-regressao.csv`. Depois de alterar o CSV, execute:

```text
python gerar_figuras.py
```

O script recria o arquivo draw.io e calcula a reta com os novos valores. Ele usa
somente recursos que já vêm no Python. Faça uma cópia do draw.io antes de rodar
o script se tiver feito mudanças manuais no desenho, pois ele recria as três páginas.

Após gerar ou editar o desenho, exporte a página novamente e troque a figura no
Word. Os números e as tabelas do relatório também precisam acompanhar os novos dados.

As imagens desta entrega foram exportadas com fundo branco, borda de 10 pixels
e escala 2. As páginas estão na mesma ordem das figuras do relatório.
