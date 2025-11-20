#!/bin/bash

# --- CONFIGURAÇÃO ---
# Caminho da sua pasta de dados do Zotero
ZOTERO_DATA="$HOME/Zotero"
# Nome da coleção específica (se quiser todas, remova a flag --collection abaixo)
COLECAO="Nome do Cliente ou Caso"

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
echo "Acesse em: https://peixoto-ops.github.io/fontes-processuais/"