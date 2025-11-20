#!/bin/bash

# --- CONFIGURAÇÃO ---
# Caminho da sua pasta de dados do Zotero
ZOTERO_DATA="$HOME/Zotero"
# Nome da coleção específica (se quiser todas, remova a flag --collection abaixo)
COLECAO="Sentença Arbitral - Caso Quinto Andar"

echo "--- 1. Ativando Ambiente Virtual ---"
source venv/bin/activate

echo "--- 2. Gerando Site Estático (Zotsite) ---"
# O output vai para a pasta 'docs' para o GitHub Pages ler
# Se for exportar TUDO, remova: --collection "$COLECAO"
zotsite export --data "$ZOTERO_DATA" --output docs --collection "$COLECAO"

echo "--- 3. Enviando para o GitHub ---"
git add .
git commit -m "Update: Fontes atualizadas em $(date '+%d/%m/%Y %H:%M')"
git push origin main

echo "--- FEITO! ---"
echo "Acesse em: https://peixoto-ops.github.io/fontes-processuais/"#!/bin/bash

# --- CONFIGURAÇÕES ---
# 1. Caminho do banco de dados (Padrão do Ubuntu)
ZOTERO_DB="$HOME/Zotero"

# 2. Pasta de saída (Obrigatório ser 'docs' para o GitHub Pages facilitar)
OUTPUT_DIR="docs"

# 3. NOME EXATO DA COLEÇÃO (Copiei da sua imagem)
# Use aspas duplas para garantir que o bash leia os espaços
COLECAO="Sentença Arbitral - Caso Quinto Andar"

# --- EXECUÇÃO ---

echo "--- 1. Ativando Ambiente Virtual ---"
source venv/bin/activate

echo "--- 2. Limpando versão anterior ---"
# Opcional: garante que arquivos deletados no Zotero sumam do site
rm -rf "$OUTPUT_DIR"

echo "--- 3. Exportando APENAS a coleção: $COLECAO ---"
# A mágica acontece aqui: --collection filtra o DB
zotsite export --data "$ZOTERO_DB" --output "$OUTPUT_DIR" --collection "$COLECAO"

echo "--- 4. Enviando para o GitHub ---"
git add .
git commit -m "Update: Coleção $COLECAO atualizada em $(date '+%d/%m/%Y %H:%M')"
git push origin main

echo "--- CONCLUÍDO ---"
echo "Acesse seu repositório para ver o link do Pages."