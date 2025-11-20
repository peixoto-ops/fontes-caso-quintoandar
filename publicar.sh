#!/bin/bash

# ==============================================================================
# PEIXOTO-OPS: AUTOMATIZAÇÃO DE DEPLOY DO ACERVO JURÍDICO (ZOTERO -> GITHUB)
# ==============================================================================

# --- 1. CONFIGURAÇÕES ---
# Caminho do Banco de Dados
ZOTERO_DB="$HOME/Zotero"

# Nome EXATO do seu repositório no GitHub (Extraído do seu link)
# IMPORTANTE: Se mudar o nome do repo, mude aqui.
REPO_NAME="fontes-caso-quintoandar"

# Regex da Coleção (Usamos .* para garantir que pegue a pasta correta)
# O ponto em "Senten.a" ignora se é 'ç' ou 'c' para evitar erro de encoding
COLECAO=".*Senten.a Arbitral.*Caso Quinto Andar.*"

# Pasta de saída
OUTPUT_DIR="docs"

# --- 2. PREPARAÇÃO ---
echo ">>> [1/5] Ativando ambiente virtual..."
source venv/bin/activate

echo ">>> [2/5] Limpando build anterior..."
rm -rf "$OUTPUT_DIR"

# --- 3. GERAÇÃO DO SITE (ZOTSITE) ---
echo ">>> [3/5] Exportando coleção: $COLECAO"
# Exporta apenas a coleção filtrada
zotsite export --data "$ZOTERO_DB" --output "$OUTPUT_DIR" --collection "$COLECAO"

# --- 4. CORREÇÕES PÓS-PROCESSAMENTO (CRÍTICO PARA GITHUB PAGES) ---
echo ">>> [4/5] Aplicando correções de rota para GitHub Pages..."

# 4.1. Cria arquivo para impedir que o GitHub ignore pastas com underline (_)
touch "$OUTPUT_DIR/.nojekyll"

# 4.2. Injeta a tag <base> no HTML para corrigir links quebrados (No Content Fix)
# Isso diz ao navegador: "A raiz do site é /fontes-caso-quintoandar/, não peixoto-ops.github.io/"
sed -i "s|<head>|<head><base href=\"/$REPO_NAME/\">|g" "$OUTPUT_DIR/index.html"

# --- 5. DEPLOY (GIT) ---
echo ">>> [5/5] Enviando para o GitHub..."

git add .
git commit -m "Update: Acervo atualizado em $(date '+%d/%m/%Y %H:%M') - AutoDeploy"
git push origin main

echo "========================================================"
echo " SUCESSO! O acervo foi atualizado."
echo " Acesse em: https://peixoto-ops.github.io/$REPO_NAME/"
echo " (Pode levar até 2 min para o GitHub atualizar o cache)"
echo "========================================================"