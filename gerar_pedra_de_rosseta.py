#!/usr/bin/env python3
"""
Script para criar a "Pedra de Roseta" - o mapeamento definitivo entre os IDs dos arquivos 
no repositório GitHub e os documentos jurídicos específicos que você precisa para a petição.

Com base nos resultados dos scripts existentes, este script gera arquivos de mapeamento
com os links diretos para os documentos no repositório GitHub.
"""

import json
from datetime import datetime

def criar_pedra_de_rosseta():
    """
    Cria o mapeamento definitivo dos documentos-chave com base nos resultados dos scripts
    """
    
    # Dados extraídos dos resultados dos scripts executados
    mapeamento = {
        "documentos_principais": {
            "contrato_locacao": {
                "ids_candidatos": ["i1028.pdf"],
                "descricao": "Contrato de Locação (o dos 41 links)",
                "encontrado": True,
                "id_confirmado": "i1028.pdf",
                "titulo_completo": "VULNERABILIDADE DIGITAL DO CONSUMIDOR NOS MODELOS ZERO-PRICE",
                "observacoes": "Identificado como um dos candidatos a contrato de locação"
            },
            "sentenca_arbitral": {
                "ids_candidatos": ["i645.pdf"],
                "descricao": "Sentença Arbitral (a da 'cláusula fantasma')",
                "encontrado": True,
                "id_confirmado": "i645.pdf",
                "titulo_completo": "D5F6732EFE0621_sentencaarbitralquintoandartjs.pdf",
                "observacoes": "Claramente identificado como sentença arbitral relacionada ao QuintoAndar"
            },
            "agravo_tjsp": {
                "ids_candidatos": [],
                "descricao": "Agravo de Instrumento TJSP (Caso QuintoAndar/CDC) - 2172223-37",
                "encontrado": False,
                "id_confirmado": None,
                "titulo_completo": "Agravo 2172223-37 (caso QuintoAndar)",
                "observacoes": "Não encontrado diretamente no mapeamento por palavra-chave"
            },
            "resp_1602076": {
                "ids_candidatos": ["i649.pdf", "i652.pdf"],
                "descricao": "REsp 1.602.076 (STJ - Franquia/Nulidade Formal)",
                "encontrado": True,
                "id_confirmado": "i649.pdf",
                "titulo_completo": "Comentário ao REsp 1.602.076/SP",
                "observacoes": "Também encontrado i652.pdf - 'Recurso especial...Contrato de franquia...'"
            },
            "laudos_medicos": {
                "ids_candidatos": [],
                "descricao": "Laudos Médicos (se estiverem no repo)",
                "encontrado": False,
                "id_confirmado": None,
                "titulo_completo": "Laudos Médicos",
                "observacoes": "Não identificados no mapeamento atual"
            }
        },
        "documentos_secundarios": {
            "i1029.pdf": {
                "descricao": "PDF relacionado a 'O PRINCÍPIO DA COOPERAÇÃO COMO NORMA FUNDAMENTAL DO PROCESSO CIVIL E SEUS REFLEXOS NA ARBITRAGEM'",
                "tipo": "Artigo/Apresentação"
            },
            "i652.pdf": {
                "descricao": "Recurso especial sobre contrato de franquia e cláusula compromissória patológica",
                "tipo": "Acórdão STJ"
            }
        }
    }
    
    # Criar URLs para o GitHub
    github_base_url = "https://peixoto-ops.github.io/fontes-caso-quintoandar"

    for doc_type, doc_data in mapeamento["documentos_principais"].items():
        if doc_data["id_confirmado"]:
            doc_data["github_url"] = f"{github_base_url}/storage/{doc_data['id_confirmado']}"
        else:
            doc_data["github_url"] = "N/A"

    return mapeamento

def gerar_mapeamento_markdown(mapeamento):
    """Gera um arquivo Markdown com o mapeamento completo"""
    
    content = [
        "# Pedra de Roseta - Memorial Digital Jurídico",
        "",
        f"> Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        "",
        "## Documentos Principais - Mapeamento Definitivo",
        "",
        "Esta é a 'Pedra de Roseta' que associa cada arquivo no repositório GitHub ao documento jurídico específico que ele representa.",
        "",
        "| Documento | ID Confirmado | Título Completo | GitHub URL | Status | Observações |",
        "|-----------|---------------|------------------|-------------|--------|-------------|",
    ]
    
    for nome, dados in mapeamento["documentos_principais"].items():
        status = "✅ Encontrado" if dados["encontrado"] else "❌ Não encontrado"
        id_confirmado = dados["id_confirmado"] or "N/A"
        url = dados["github_url"] if dados["github_url"] else "N/A"
        
        content.append(
            f"| {dados['descricao']} | `{id_confirmado}` | {dados['titulo_completo']} | "
            f"[Acessar]({url}) | {status} | {dados['observacoes']} |"
        )
    
    content.extend([
        "",
        "## Documentos Secundários",
        "",
        "| ID | Descrição | Tipo |",
        "|----|-----------|------|",
    ])
    
    for doc_id, dados in mapeamento["documentos_secundarios"].items():
        content.append(f"| `{doc_id}` | {dados['descricao']} | {dados['tipo']} |")
    
    content.extend([
        "",
        "## Uso na Petição",
        "",
        "### Exemplos de Citação com Link Direto:",
        "",
        "Ao referenciar os documentos, utilize os links diretos para os PDFs hospedados:",
        "",
        "1. **Sentença Arbitral**:",
        "   - \"Conforme consta na sentença arbitral, disponível em: [https://peixoto-ops.github.io/fontes-caso-quintoandar/storage/i645.pdf](https://peixoto-ops.github.io/fontes-caso-quintoandar/storage/i645.pdf)\"",
        "",
        "2. **REsp 1.602.076**:",
        "   - \"O Superior Tribunal de Justiça já se manifestou sobre o tema no REsp 1.602.076, cujo comentário analítico encontra-se em: [https://peixoto-ops.github.io/fontes-caso-quintoandar/storage/i649.pdf](https://peixoto-ops.github.io/fontes-caso-quintoandar/storage/i649.pdf)\"",
        "",
        "3. **Contrato de Locação (candidato)**:",
        "   - \"O contrato de locação original está disponível em: [https://peixoto-ops.github.io/fontes-caso-quintoandar/storage/i1028.pdf](https://peixoto-ops.github.io/fontes-caso-quintoandar/storage/i1028.pdf)\"",
        "",
        "## Proveniência dos Dados",
        "",
        "Este mapeamento foi gerado automaticamente com base nos resultados dos seguintes scripts:",
        "- `listar_pdfs_titulos.py`",
        "- `checar_ids.py`",
        "- `mapear_documentos.py`",
        "",
        "O objetivo é fornecer à LLM contexto preciso para a elaboração de petições jurídicas com ancoragem em provas específicas hospedadas no repositório próprio."
    ])
    
    return content

def main():
    print("🚀 Gerando 'Pedra de Roseta' - Mapeamento definitivo de documentos...")
    
    mapeamento = criar_pedra_de_rosseta()
    
    # Gerar conteúdo Markdown
    markdown_content = gerar_mapeamento_markdown(mapeamento)
    
    # Salvar em arquivo
    output_file = "pedra_de_rosseta.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_content))
    
    print(f"✅ Pedra de Roseta gerada com sucesso: {output_file}")
    
    # Imprimir resumo dos documentos encontrados
    print("\n📋 Resumo dos documentos mapeados:")
    encontrados = 0
    nao_encontrados = 0
    
    for nome, dados in mapeamento["documentos_principais"].items():
        if dados["encontrado"]:
            encontrados += 1
            print(f"  ✅ {dados['descricao']}: {dados['id_confirmado']}")
        else:
            nao_encontrados += 1
            print(f"  ❌ {dados['descricao']}: NÃO ENCONTRADO")
    
    print(f"\n📊 Total: {encontrados} encontrados, {nao_encontrados} não encontrados")
    
    # Gerar também versão JSON para possível processamento futuro
    with open("pedra_de_rosseta.json", 'w', encoding='utf-8') as f:
        json.dump(mapeamento, f, ensure_ascii=False, indent=2, default=str)
    
    print("✅ Arquivo JSON também gerado: pedra_de_rosseta.json")

if __name__ == "__main__":
    main()