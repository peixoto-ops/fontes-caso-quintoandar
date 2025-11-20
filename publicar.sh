#!/bin/bash

# ==============================================================================
# SCRIPT DE DEPLOY: ACERVO JURÍDICO + PRODUTO IA
# ==============================================================================

# --- 1. CONFIGURAÇÕES ---
ZOTERO_DB="$HOME/Zotero"
REPO_NAME="fontes-caso-quintoandar"
OUTPUT_DIR="docs"
# Regex da coleção
COLECAO=".*Senten.a Arbitral.*Caso Quinto Andar.*"

# --- 2. PREPARAÇÃO ---
echo ">>> [1/7] Ativando ambiente virtual..."
source venv/bin/activate

echo ">>> [2/7] Limpando versão anterior (Reset)..."
# AQUI ERA ONDE SEU ARQUIVO SUMIA:
rm -rf "$OUTPUT_DIR"

# --- 3. GERAÇÃO DO SITE (ZOTSITE) ---
echo ">>> [3/7] Exportando coleção: $COLECAO"
zotsite export "$ZOTERO_DB" --output "$OUTPUT_DIR" --collection "$COLECAO"

# --- 4. CORREÇÃO DE ROTAS (FIX TÉCNICO) ---
echo ">>> [4/7] Aplicando correções para GitHub Pages..."
touch "$OUTPUT_DIR/.nojekyll"

# Corrige caminhos no Javascript e HTML (Remove barra inicial)
find "$OUTPUT_DIR" -name "*.js" -print0 | xargs -0 sed -i 's|"/items/|"items/|g'
find "$OUTPUT_DIR" -name "*.js" -print0 | xargs -0 sed -i 's|"/projects/|"projects/|g'
find "$OUTPUT_DIR" -name "*.js" -print0 | xargs -0 sed -i 's|"/documents/|"documents/|g'
find "$OUTPUT_DIR" -name "*.html" -print0 | xargs -0 sed -i 's|href="/items/|href="items/|g'
find "$OUTPUT_DIR" -name "*.html" -print0 | xargs -0 sed -i 's|src="/items/|src="items/|g'

# Define a Base URL
sed -i "s|<head>|<head><base href=\"/$REPO_NAME/\">|g" "$OUTPUT_DIR/index.html"

# --- 5. GERAÇÃO DO PRODUTO IA (AGORA NA HORA CERTA) ---
echo ">>> [5/7] Gerando Arquivo Mestre para IA..."
# O Zotsite já criou os PDFs no passo 3, então agora o Python vai achá-los
python gerar_contexto.py

# --- 6. CUSTOMIZAÇÃO ---
echo ">>> [6/7] Ajustando título..."
sed -i "s|<title>.*</title>|<title>Memorial Digital - Caso Quinto Andar</title>|g" "$OUTPUT_DIR/index.html"

# --- 7. DEPLOY ---
echo ">>> [7/7] Enviando para o GitHub..."
git add .
git commit -m "Update: Site + Contexto IA em $(date '+%d/%m/%Y %H:%M')"
git push origin main

echo "========================================================"
echo " ✅ SUCESSO TOTAL!"
echo " 1. Site: https://peixoto-ops.github.io/$REPO_NAME/"
echo " 2. Contexto IA: https://github.com/peixoto-ops/$REPO_NAME/blob/main/docs/contexto_para_ia.md"
echo "========================================================"