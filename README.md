# Memorial Digital Jurídico - Simplificado

Projeto para publicação de documentos jurídicos do Zotero para GitHub Pages com contexto enriquecido para IA.

## Funcionalidades

- **Exportação Seletiva**: Usa regex para exportar apenas a coleção específica do Zotero
- **Contexto para IA**: Gera `contexto_para_ia.md` com mapeamento "Pedra de Roseta" (contrato, sentença, REsp)
- **Publicação Automática**: Faz deploy para GitHub Pages

## Configuração

Crie um arquivo `.env`:

```bash
ZOTERO_DB="/home/seu-usuario/Zotero"
REPO_URL="git@github.com:usuario/repo.git"
REPO_NAME="nome-do-repo"
REGEX_COLECAO=".*Nome da Coleção.*"
GITHUB_USER="seu-usuario"
SITE_TITLE="Memorial Digital"
```

## Uso

```bash
./publicar.sh
```

O script:
1. Lê configurações do `.env`
2. Exporta coleção específica do Zotero via zotsite
3. Gera contexto para IA com Pedra de Roseta
4. Publica no gh-pages

## Scripts

- `publicar.sh`: Publicação automatizada
- `gerar_contexto.py`: Gera contexto para IA com mapeamento enriquecido
- `pedra_de_rosseta.json`: Mapeamento entre IDs e documentos jurídicos