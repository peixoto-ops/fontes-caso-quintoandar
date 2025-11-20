# Memorial Digital Jurídico

Este projeto automatiza a publicação de fontes bibliográficas jurídicas do Zotero para um site estático no GitHub Pages e gera um artefato Markdown estruturado para uso em LLMs (Large Language Models).

## 🚀 Funcionalidades

1.  **Site Estático**: Gera um site navegável com o acervo jurídico exportado do Zotero.
2.  **Contexto para IA**: Cria um arquivo `contexto_para_ia.md` contendo links indexados para todos os documentos, facilitando a ingestão por IAs.
3.  **Deploy Automatizado**: Script `publicar.sh` que realiza todo o processo de build e deploy para o GitHub Pages.

## 🛠️ Configuração

O projeto utiliza um arquivo `.env` para gerenciar configurações sensíveis e específicas do ambiente.

### 1. Criar arquivo `.env`
Copie o exemplo abaixo e crie um arquivo `.env` na raiz do projeto:

```bash
# Caminho para o banco de dados do Zotero (SQLite)
ZOTERO_DB="/home/seu-usuario/Zotero"

# URL do repositório GitHub (SSH ou HTTPS)
REPO_URL="git@github.com:usuario/repo.git"

# Nome do repositório (usado para gerar a Base URL do site)
REPO_NAME="nome-do-repo"

# Regex para filtrar a coleção do Zotero a ser exportada
REGEX_COLECAO=".*Nome da Coleção.*"

# Título do Site (aparece na aba do navegador e no contexto IA)
SITE_TITLE="Memorial Digital - Meu Caso"

# Usuário do GitHub (usado para gerar a URL do Pages)
GITHUB_USER="seu-usuario"

# Pasta temporária de build (padrão: public)
BUILD_DIR="public"
```

### 2. Dependências
- **Zotero 7**
- **Python 3**
- **Zotsite** (Instalado via pip/venv)

## 📦 Como Usar

Para gerar o site e fazer o deploy, execute o script principal:

```bash
./publicar.sh
```

O script irá:
1.  Ler as configurações do `.env`.
2.  Exportar a coleção definida do Zotero.
3.  Corrigir links e caminhos para o GitHub Pages.
4.  Gerar o arquivo de contexto para IA.
5.  Publicar o resultado no branch `gh-pages`.

## 📂 Estrutura do Projeto

- `publicar.sh`: Script orquestrador de build e deploy.
- `gerar_contexto.py`: Script Python que indexa os PDFs e gera o Markdown.
- `.env`: Arquivo de configuração (não versionado).
- `public/`: Pasta gerada contendo o site estático e o arquivo de contexto (não versionada).

## 🔗 Links Úteis

- [Acesse o Site Publicado](https://peixoto-ops.github.io/fontes-caso-quintoandar/)