import os
import glob

def main():
    # --- CONFIGURAÇÕES ---
    # Caminho absoluto (onde o script está)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DOCS_DIR = os.path.join(ROOT_DIR, "docs")
    OUTPUT_FILE = os.path.join(DOCS_DIR, "contexto_para_ia.md")
    
    # Seu Repositório
    REPO_NAME = "fontes-caso-quintoandar"
    URL_BASE = f"https://peixoto-ops.github.io/{REPO_NAME}"

    print(f"--- 🔍 Iniciando Varredura em: {DOCS_DIR} ---")

    if not os.path.exists(DOCS_DIR):
        print(f"❌ ERRO: A pasta {DOCS_DIR} não existe.")
        return

    markdown_content = [
        f"# ACERVO JURÍDICO: {REPO_NAME.upper()}",
        "> 🤖 Documento gerado automaticamente para ingestão em LLMs.",
        "",
        "## 📂 Lista de Fontes e Links",
        ""
    ]
    
    # O PULO DO GATO: Busca Recursiva (**)
    # Procura PDFs em qualquer subpasta (projects, storage, files, etc.)
    search_pattern = os.path.join(DOCS_DIR, "**", "*.pdf")
    # recursive=True faz ele mergulhar em todas as pastas
    files = sorted(glob.glob(search_pattern, recursive=True))
    
    if not files:
        print("⚠️ AVISO: Nenhum PDF encontrado em lugar nenhum dentro de 'docs'!")
        print("   Verifique se o Zotsite realmente exportou os arquivos.")
    else:
        print(f"✅ Encontrados {len(files)} documentos.")

    for file_path in files:
        filename = os.path.basename(file_path)
        
        # Calcula o caminho relativo para montar o link correto
        # Ex: se o arquivo está em docs/storage/123/file.pdf, vira storage/123/file.pdf
        relative_path = os.path.relpath(file_path, DOCS_DIR)
        
        # Monta o link público (GitHub Pages)
        # O .replace() garante que barras invertidas do Windows não quebrem o link
        web_path = relative_path.replace(os.sep, "/")
        public_link = f"{URL_BASE}/{web_path}"
        
        # Limpa o nome para exibição
        display_name = filename.replace(".pdf", "").replace("_", " ")
        
        markdown_content.append(f"### 📄 {display_name}")
        markdown_content.append(f"- **Acesso:** [Abrir Documento]({public_link})")
        markdown_content.append("")

    # Salva o arquivo
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_content))
        print(f"💾 Arquivo salvo em: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ ERRO ao salvar: {e}")

if __name__ == "__main__":
    main()