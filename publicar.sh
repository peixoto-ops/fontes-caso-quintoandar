#!/bin/bash

# ==============================================================================
# SCRIPT DE PUBLICAÇÃO - SIMPLIFICADO
# ==============================================================================

# Carrega variáveis do arquivo .env, ignorando comentários e tratando aspas
if [ -f .env ]; then
    # Lê e exporta apenas linhas que contêm variáveis (não comentários)
    while IFS= read -r line; do
        if [[ $line =~ ^[^#].*= ]] && [ -n "$line" ]; then
            # Remove espaços em branco no início e fim
            line=$(echo $line | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            # Exporta a variável usando source para interpretar corretamente as aspas
            eval "export $line"
        fi
    done < .env
else
    echo "❌ Arquivo .env não encontrado!"
    exit 1
fi

# Valores obrigatórios
REPO_URL="${REPO_URL:?❌ Erro: REPO_URL não definido no .env}"
REPO_NAME="${REPO_NAME:?❌ Erro: REPO_NAME não definido no .env}"
BUILD_DIR="${BUILD_DIR:-public}"
REGEX_COLECAO="${REGEX_COLECAO:?❌ Erro: REGEX_COLECAO não definido no .env}"

echo ">>> Preparando ambiente..."
source venv/bin/activate
rm -rf "$BUILD_DIR"

echo ">>> Exportando coleção do Zotero..."
# Configuração temporária para zotsite
cat > zotsite.conf <<EOF
[zotsite_zotero_app]
data_dir = ${ZOTERO_DB}
[zotsite_export_app]
output_dir = zotero-site
collection = ${REGEX_COLECAO}
EOF

zotsite export --config zotsite.conf
rm zotsite.conf

# Mover conteúdo para o diretório BUILD_DIR
if [ -d "zotero-site" ]; then
    mv zotero-site "$BUILD_DIR"
else
    echo "❌ Falha na exportação - diretório zotero-site não foi criado"
    exit 1
fi

if [ ! -d "$BUILD_DIR" ]; then
    echo "❌ Falha na exportação - BUILD_DIR não existe"
    exit 1
fi

# Marca para GitHub Pages
touch "$BUILD_DIR/.nojekyll"

echo ">>> Gerando contexto para IA..."
python3 gerar_contexto.py "$BUILD_DIR"

echo ">>> Publicando no gh-pages..."
cd "$BUILD_DIR"
git init
git add .
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M')"
git push --force "$REPO_URL" HEAD:gh-pages
cd ..

echo "✅ Publicação concluída!"
echo "Site disponível em: https://${GITHUB_USER:-peixoto-ops}.github.io/${REPO_NAME}/"