import os
import glob
import sys

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
    
    REPO_NAME = os.environ.get("REPO_NAME", "meu-projeto-juridico")
    GITHUB_USER = os.environ.get("GITHUB_USER", "seu-usuario")
    SITE_TITLE = os.environ.get("SITE_TITLE", f"ACERVO JURÍDICO: {REPO_NAME.upper()}")
    URL_BASE = f"https://{GITHUB_USER}.github.io/{REPO_NAME}"

    print(f"--- 🔍 Varrendo: {TARGET_DIR} ---")

    if not os.path.exists(TARGET_DIR):
        print(f"❌ ERRO: A pasta {TARGET_DIR} não existe.")
        return

    markdown_content = [
        f"# {SITE_TITLE}",
        "> 🤖 Documento gerado automaticamente para ingestão em LLMs.",
        "",
        "## 📂 Lista de Fontes",
        ""
    ]
    
    # Busca recursiva
    files = sorted(glob.glob(os.path.join(TARGET_DIR, "**", "*.pdf"), recursive=True))
    
    for file_path in files:
        filename = os.path.basename(file_path)
        # Cria link relativo removendo o caminho da pasta base
        relative_path = os.path.relpath(file_path, TARGET_DIR).replace(os.sep, "/")
        public_link = f"{URL_BASE}/{relative_path}"
        
        display_name = filename.replace(".pdf", "").replace("_", " ")
        markdown_content.append(f"### 📄 {display_name}")
        markdown_content.append(f"- [Abrir Documento]({public_link})")
        markdown_content.append("")

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_content))
        print(f"✅ Contexto IA gerado: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()