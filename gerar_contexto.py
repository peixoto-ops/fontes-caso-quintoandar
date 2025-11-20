import json
import glob
import os

# Caminho onde o Zotsite salvou os dados
BASE_DIR = "docs"
URL_BASE = "https://peixoto-ops.github.io/fontes-caso-quintoandar"

def main():
    print("--- Gerando Contexto para IA ---")
    
    # O Zotsite salva dados em arquivos JS na pasta 'js/data' ou similar
    # Mas a maneira mais robusta é varrer a estrutura de pastas gerada
    
    markdown_content = ["# CONTEXTO JURÍDICO: CASO QUINTO ANDAR", ""]
    
    # Varrer PDFs processados
    projects = sorted(glob.glob(f"{BASE_DIR}/projects/*"))
    
    for project_path in projects:
        filename = os.path.basename(project_path)
        # Limpa o nome para ficar legível
        display_name = filename.replace(".pdf", "").replace("_", " ")
        
        # Link Público
        public_link = f"{URL_BASE}/projects/{filename}"
        
        markdown_content.append(f"## Documento: {display_name}")
        markdown_content.append(f"- **Link para Fonte Real:** [Acessar PDF]({public_link})")
        
        # Tenta achar notas associadas (se o zotsite exportou notas como txt/html)
        # Se não, apenas a existência do documento validado já é ouro para a IA.
        markdown_content.append("\n---\n")

    # Salva o arquivo
    with open(f"{BASE_DIR}/contexto_para_ia.md", "w") as f:
        f.write("\n".join(markdown_content))
        
    print(f"Sucesso! Arquivo gerado em: {BASE_DIR}/contexto_para_ia.md")

if __name__ == "__main__":
    main()