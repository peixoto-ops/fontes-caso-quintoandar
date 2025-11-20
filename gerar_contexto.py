import os
import glob
import sys
import json

def carregar_pedra_de_rosseta():
    """
    Carrega a Pedra de Roseta se disponível para enriquecer o contexto com metadados
    """
    pedra_de_rosseta_path = os.path.join(os.path.dirname(__file__), "pedra_de_rosseta.json")

    if os.path.exists(pedra_de_rosseta_path):
        try:
            with open(pedra_de_rosseta_path, 'r', encoding='utf-8') as f:
                pedra_de_rosseta = json.load(f)

            # Criar mapeamento de ID para metadados
            mapeamento_ids = {}
            for categoria, documentos in pedra_de_rosseta["documentos_principais"].items():
                if documentos["id_confirmado"]:
                    id_pdf = documentos["id_confirmado"]
                    # Remover .pdf do ID para criar a chave de busca
                    id_sem_extensao = id_pdf.replace('.pdf', '')
                    # Certificar-se de que não estamos duplicando o 'i' no início
                    if id_sem_extensao.startswith('i'):
                        chave_mapeamento = id_sem_extensao  # já tem o 'i' no início
                    else:
                        chave_mapeamento = f"i{id_sem_extensao}"
                    mapeamento_ids[chave_mapeamento] = {
                        "categoria": categoria,
                        "descricao": documentos["descricao"],
                        "titulo_completo": documentos["titulo_completo"],
                        "observacoes": documentos["observacoes"],
                        "github_url": documentos["github_url"]
                    }

            return mapeamento_ids
        except Exception as e:
            print(f"⚠️ Erro ao carregar Pedra de Roseta: {e}")
            return {}

    return {}

def main():
    # Pega o diretório passado pelo shell script ou usa variável de ambiente ou padrão 'public'
    if len(sys.argv) > 1:
        BASE_DIR = sys.argv[1]
    else:
        BASE_DIR = os.environ.get("BUILD_DIR", "public")

    # Caminho absoluto
    ROOT_DIR = os.getcwd() # Assume que está rodando da raiz
    TARGET_DIR = os.path.join(ROOT_DIR, BASE_DIR)
    OUTPUT_FILE = os.path.join(TARGET_DIR, "contexto_para_ia.md")

    REPO_NAME = os.environ.get("REPO_NAME", "Caso Quinto Andar")
    GITHUB_USER = os.environ.get("GITHUB_USER", "seu-usuario")
    SITE_TITLE = os.environ.get("SITE_TITLE", "Memorial Digital - Caso Quinto Andar")
    URL_BASE = f"https://{GITHUB_USER}.github.io/{REPO_NAME}"

    if not os.path.exists(TARGET_DIR):
        print(f"❌ ERRO: A pasta {TARGET_DIR} não existe.")
        return

    # Carrega a Pedra de Roseta para enriquecimento de metadados
    pedra_de_rosseta = carregar_pedra_de_rosseta()

    markdown_content = [
        f"# {SITE_TITLE}",
        "> 🤖 Documento gerado automaticamente para ingestão em LLMs.",
        "",
        "## 📚 Documentos Relevantes",
        ""
    ]

    # Busca recursiva por PDFs
    files = sorted(glob.glob(os.path.join(TARGET_DIR, "**", "*.pdf"), recursive=True))

    for file_path in files:
        filename = os.path.basename(file_path)

        # Extrai o ID do arquivo (ex: i1028.pdf -> i1028)
        file_id = filename.replace('.pdf', '')

        # Cria link relativo removendo o caminho da pasta base
        relative_path = os.path.relpath(file_path, TARGET_DIR).replace(os.sep, "/")
        public_link = f"{URL_BASE}/{relative_path}"

        # Tenta obter informações da Pedra de Roseta
        info_rosseta = pedra_de_rosseta.get(file_id, {})

        # Determina o tipo de documento e título para exibição
        if info_rosseta:
            descricao = info_rosseta.get("descricao", filename.replace(".pdf", "").replace("_", " "))
            titulo_completo = info_rosseta.get("titulo_completo", "")
            observacoes = info_rosseta.get("observacoes", "")

            # Determina o emoji baseado na descrição
            if "sentenca" in str(descricao).lower():
                emoji = "🏛️"
            elif "resp" in str(descricao).lower():
                emoji = "📋"
            elif "contrato" in str(descricao).lower():
                emoji = "📝"
            else:
                emoji = "📄"

            # Usa o título completo se disponível, senão a descrição
            display_name = titulo_completo if titulo_completo else descricao

            # Adiciona à lista com informações enriquecidas
            markdown_content.append(f"### {emoji} {display_name}")
            markdown_content.append(f"- **ID:** `{file_id}.pdf`")
            markdown_content.append(f"- **Tipo:** {descricao}")
            if observacoes:
                markdown_content.append(f"- **Observações:** {observacoes}")
            markdown_content.append(f"- **[Acessar Documento]({public_link})**")
            markdown_content.append("")
        else:
            # Caso não esteja na Pedra de Roseta, exibe como documento genérico
            display_name = filename.replace(".pdf", "").replace("_", " ")
            markdown_content.append(f"### 📄 {display_name}")
            markdown_content.append(f"- **ID:** `{file_id}.pdf`")
            markdown_content.append(f"- **[Acessar Documento]({public_link})**")
            markdown_content.append("")

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_content))
        print(f"✅ Contexto IA gerado: {OUTPUT_FILE}")
        print(f"📊 {len(files)} documentos processados")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()