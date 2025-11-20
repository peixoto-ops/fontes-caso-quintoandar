#!/bin/bash

# ==============================================================================
# SCRIPT DE DEPLOY: ACERVO JURÍDICO (ZOTERO -> GITHUB PAGES)
# Autor: Peixoto-Ops
# Correção Aplicada: Path Fix (Links Relativos para Subdiretório)
# ==============================================================================

# --- 1. CONFIGURAÇÕES ---
ZOTERO_DB="$HOME/Zotero"
REPO_NAME="fontes-caso-quintoandar"
OUTPUT_DIR="docs"

# Regex segura para encontrar a coleção (Ignora acentos de 'Sentença')
COLECAO=".*Senten.a Arbitral.*Caso Quinto Andar.*"

# --- 2. PREPARAÇÃO ---
echo ">>> [1/6] Ativando ambiente virtual..."
source venv/bin/activate

echo ">>> [2/6] Limpando versão anterior..."
rm -rf "$OUTPUT_DIR"

# --- 3. GERAÇÃO (ZOTSITE) ---
echo ">>> [3/6] Exportando coleção: $COLECAO"
zotsite export --output "$OUTPUT_DIR" --collection "$COLECAO"

# --- 4. CORREÇÃO DE ROTAS (O "PULO DO GATO" TÉCNICO) ---
echo ">>> [4/6] Aplicando correções para GitHub Pages..."

# 4.1. Impede que o GitHub ignore pastas do sistema
touch "$OUTPUT_DIR/.nojekyll"

# 4.2. CORREÇÃO DE LINKS QUEBRADOS (Transforma Absoluto em Relativo)
# O Zotsite gera links como "/items/...", o que quebra no GitHub.
# Estes comandos removem a barra inicial dentro dos arquivos JS e HTML gerados.

# Corrige caminhos nos arquivos Javascript (onde fica a árvore de navegação)
find "$OUTPUT_DIR" -name "*.js" -print0 | xargs -0 sed -i 's|"/items/|"items/|g'
find "$OUTPUT_DIR" -name "*.js" -print0 | xargs -0 sed -i 's|"/projects/|"projects/|g'
find "$OUTPUT_DIR" -name "*.js" -print0 | xargs -0 sed -i 's|"/documents/|"documents/|g'

# Corrige caminhos no HTML
find "$OUTPUT_DIR" -name "*.html" -print0 | xargs -0 sed -i 's|href="/items/|href="items/|g'
find "$OUTPUT_DIR" -name "*.html" -print0 | xargs -0 sed -i 's|src="/items/|src="items/|g'

# 4.3. Define a Base URL correta
sed -i "s|<head>|<head><base href=\"/$REPO_NAME/\">|g" "$OUTPUT_DIR/index.html"

# --- 5. CUSTOMIZAÇÃO VISUAL (OPCIONAL) ---
echo ">>> [5/6] Ajustando título da página..."
sed -i "s|<title>.*</title>|<title>Memorial Digital - Caso Quinto Andar</title>|g" "$OUTPUT_DIR/index.html"

# --- 6. DEPLOY ---
echo ">>> [6/6] Enviando para o GitHub..."
git add .
git commit -m "Update: Correção de links e novos documentos em $(date '+%d/%m/%Y %H:%M')"
git push origin main

echo "========================================================"
echo " CONCLUÍDO COM SUCESSO!"
echo " Teste em: https://peixoto-ops.github.io/$REPO_NAME/"
echo " (Aguarde 2 min e use Ctrl+F5 para limpar cache)"
echo "========================================================"