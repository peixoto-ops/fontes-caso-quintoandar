#!/bin/bash

# ==============================================================================
# DEPLOY VIA BRANCH ORFÃO (Clean Architecture)
# ==============================================================================

# --- CONFIGURAÇÕES ---
# Carrega variáveis do arquivo .env
if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo "❌ Arquivo .env não encontrado!"
    exit 1
fi

# Valores padrão ou Erro se não definido
ZOTERO_DB="${ZOTERO_DB:-$HOME/Zotero}"
REPO_URL="${REPO_URL:?❌ Erro: REPO_URL não definido no .env}"
REPO_NAME="${REPO_NAME:?❌ Erro: REPO_NAME não definido no .env}"
BUILD_DIR="${BUILD_DIR:-public}"
REGEX_COLECAO="${REGEX_COLECAO:?❌ Erro: REGEX_COLECAO não definido no .env}"
SITE_TITLE="${SITE_TITLE:-Memorial Digital}"

echo ">>> [1/6] Preparando ambiente..."
source venv/bin/activate
rm -rf "$BUILD_DIR"
rm -rf zotero-site

echo ">>> [2/6] Exportando Zotero..."
# Configuração temporária
cat > zotsite.conf <<EOF
[zotsite_zotero_app]
data_dir = ${ZOTERO_DB}
[zotsite_export_app]
output_dir = ${BUILD_DIR}
collection = ${REGEX_COLECAO}
EOF

zotsite export --config zotsite.conf
rm zotsite.conf

# Se o Zotsite criar pasta com nome errado, corrige
if [ -d "zotero-site" ]; then mv zotero-site "$BUILD_DIR"; fi
if [ ! -d "$BUILD_DIR" ]; then echo "❌ Falha na exportação"; exit 1; fi

echo ">>> [3/6] Correções de Rota (Links Relativos)..."
touch "$BUILD_DIR/.nojekyll"

# Remove links absolutos (/items -> items)
find "$BUILD_DIR" -name "*.js" -print0 | xargs -0 sed -i 's|"/items/|"items/|g'
find "$BUILD_DIR" -name "*.js" -print0 | xargs -0 sed -i 's|"/projects/|"projects/|g'
find "$BUILD_DIR" -name "*.js" -print0 | xargs -0 sed -i 's|"/documents/|"documents/|g'
find "$BUILD_DIR" -name "*.html" -print0 | xargs -0 sed -i 's|href="/items/|href="items/|g'
find "$BUILD_DIR" -name "*.html" -print0 | xargs -0 sed -i 's|src="/items/|src="items/|g'

# Base URL e Título
sed -i "s|<head>|<head><base href=\"/$REPO_NAME/\">|g" "$BUILD_DIR/index.html"
sed -i "s|<title>.*</title>|<title>$SITE_TITLE</title>|g" "$BUILD_DIR/index.html"

echo ">>> [4/6] Gerando Contexto IA..."
# Passamos a pasta BUILD_DIR como argumento
python3 gerar_contexto.py "$BUILD_DIR"
echo "📄 Arquivo de Contexto: $(pwd)/$BUILD_DIR/contexto_para_ia.md"

echo ">>> [5/6] Publicando no branch 'gh-pages'..."
# Entra na pasta, cria um git temporário e força o envio
cd "$BUILD_DIR"
git init
git add .
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M')"
# Força o push para o branch gh-pages do repositório remoto
git push --force "$REPO_URL" HEAD:gh-pages
cd ..

echo ">>> [6/6] Limpeza..."
# Opcional: manter a pasta public para conferência ou apagar
# rm -rf "$BUILD_DIR" 

echo "========================================================"
echo " ✅ DEPLOY FINALIZADO!"
echo " Site: https://${GITHUB_USER:-peixoto-ops}.github.io/$REPO_NAME/"
echo " Branch: gh-pages (Conteúdo gerado)"
echo " Branch: main (Seus scripts)"
echo "========================================================"