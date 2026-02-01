

# 📑 NFe Duplicate Extractor (Python)

## 🚀 Sobre o Projeto
Este projeto nasceu de uma necessidade real: automatizar a digitação manual de dados de cobrança (duplicatas) vindos de arquivos XML de Notas Fiscais Eletrônicas (NF-e) para planilhas de controle financeiro.

O script varre um diretório, processa todos os XMLs encontrados e gera um arquivo CSV estruturado, transformando horas de trabalho manual em segundos de execução automatizada.

## 🛠️ Tecnologias Utilizadas
* **Python 3.x**
* **XML.etree.ElementTree**: Para parsing dos arquivos fiscais.
* **Pathlib**: Para manipulação inteligente de caminhos de diretórios.
* **CSV**: Para geração da saída compatível com Excel e Google Sheets.

## 📊 Como Funciona
1. O script identifica o *namespace* do XML automaticamente.
2. Localiza as tags de cobrança `<cobr>` e suas respectivas duplicatas `<dup>`.
3. Extrai: **Número da NF, Número da Parcela, Data de Vencimento e Valor**.
4. Consolida tudo em um arquivo `duplicatas_nfs.csv` usando `;` como delimitador (padrão brasileiro).

## 🚀 Como Executar
1. Clone o repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/nfe-duplicata-extractor.git](https://github.com/SEU_USUARIO/nfe-duplicata-extractor.git)
