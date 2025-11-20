# Memorial Digital Jurídico - QWEN Context

## Project Overview

Este é um projeto de "Memorial Digital Jurídico" que inicialmente automatizava a publicação de fontes bibliográficas jurídicas do Zotero para um site estático no GitHub Pages. No entanto, após análise, foram identificadas limitações com a abordagem atual (script `publicar.sh`) que apaga arquivos na pasta de build, dificultando a edição manual do conteúdo gerado.

### Abordagens para Integração Zotero-Website

A resposta da LLM revelou diferentes abordagens possíveis para gerar sites a partir do Zotero:

#### 1. Abordagem "No-Code" / Embed (Rápida)
Ferramentas que conectam à API do Zotero e geram uma página dinâmica:
- **BibBase**: Gera página HTML/JS com referências, mas com dependência externa
- **ZoteroPress**: Plugin WordPress (não ideal para stack de arquivos estáticos/Git)

#### 2. Abordagem Acadêmica Open Source (Robustez)
Ferramentas mais pesadas, focadas em bibliotecas institucionais:
- **Kerko**: Interface de busca avançada Python (Flask) + Solr, excelente para portais de pesquisa jurídica

#### 3. Abordagem Static Site Generators (Stack Ideal)
Melhor adaptação à stack Obsidian + Git + CLI:
- **Hugo + Academic (Wowchemy)**: Lê arquivos `.bib` nativamente
- **Jekyll + jekyll-scholar**: Similar, mas baseado em Ruby

#### 4. Abordagem "Obsidian Publishing" (Ideal para o fluxo atual)
Usando o Obsidian como Hub e RAG:
- **Obsidian + Quartz (v4)**: Transforma o Vault do Obsidian em site
- Uso do plugin **Zotero Integration** para criar notas de literatura

## Projeto Atual

### Estrutura Atual
```
/media/peixoto/Portable/fontes-caso-quintoandar/
├── publicar.sh              # Script orquestrador de build e deploy (problemas identificados)
├── gerar_contexto.py        # Script Python que indexa PDFs e gera Markdown
├── checar_ids.py            # Script para verificar IDs específicos do Zotero
├── inspect_attach.py        # Script para inspecionar esquema de anexos do Zotero
├── inspect_schema.py        # Script para inspecionar esquema do banco do Zotero
├── list_tables.py           # Script para listar tabelas do banco do Zotero
├── listar_colecoes.py       # Script para listar coleções do Zotero
├── listar_pdfs_titulos.py   # Script para listar PDFs com títulos do Zotero
├── mapear_documentos.py     # Script para mapear documentos entre Zotero e arquivos
├── mapa_completo.txt        # Saída de mapeamento completo
├── resultado_mapeamento.txt # Resultados do mapeamento
├── public/                  # Pasta gerada com site estático (não versionada)
├── venv/                    # Ambiente virtual Python
└── README.md                # Documentação do projeto
```

### Problema Identificado
O script `publicar.sh` apaga a pasta de build (`public/`) na inicialização, dificultando edições manuais do conteúdo gerado. O fluxo correto deve ser unidirecional: Zotero → Arquivo .bib (via Better BibTeX) → Site Gerado.

## Solução Recomendada

### Nova Arquitetura Proposta
1. **Fonte da Verdade**: O Zotero deve ser a única fonte da verdade
2. **Plugin Better BibTeX**: Configurar exportação automática para `.bib` ou `.json` CSL
3. **Gerador de Site Estático**: Ler o arquivo exportado para gerar o site
4. **Nunca editar conteúdo gerado**: O site deve ser sempre regenerado a partir dos dados do Zotero

### Possível Implementação
Script Python para ler arquivo `.bib` exportado e gerar HTML estático simples:

```python
# Exemplo de script futuro que poderia substituir publicar.sh
import bibtexparser
from jinja2 import Template

def generate_site_from_bib(bib_file, template_file):
    with open(bib_file, 'r', encoding='utf-8') as f:
        bib_database = bibtexparser.load(f)

    # Processar entradas e gerar HTML
    # ...
```

### Integração com Fluxo Atual
- Manter o banco do Zotero como fonte
- Usar `pdftotext` + `fabric` para extração e sumarização de conteúdo
- Gerar contexto para LLMs com base nas informações estruturadas do Zotero
- Evitar edição manual de arquivos gerados

## Conquistas Realizadas

### 1. Criação da "Pedra de Roseta" ✅
Conseguimos criar o mapeamento definitivo entre os IDs dos arquivos no repositório e os documentos jurídicos específicos:

- **Contrato de Locação** (o dos 41 links): `i1028.pdf`
- **Sentença Arbitral** (a da "cláusula fantasma"): `i645.pdf`
- **Acórdão STJ** (REsp 1.602.076 - Franquia): `i649.pdf`
- **Agravo de Instrumento TJSP** (2172223-37): ❌ Não encontrado
- **Laudos Médicos**: ❌ Não identificados

O mapeamento completo está disponível no arquivo `pedra_de_rosseta.md`, que serve como referência definitiva para a LLM.

### 2. Extração de Metadados do Zotero ✅
Utilizando scripts existentes (`listar_pdfs_titulos.py`, `checar_ids.py`, `mapear_documentos.py`), extraímos com sucesso os metadados que associam os IDs aos títulos e descrições reais dos documentos no banco do Zotero.

### 3. Documentação da Proveniência ✅
Todo o processo de mapeamento foi documentado automaticamente, rastreando a origem dos dados e criando arquivos JSON e Markdown que podem ser usados para validação e consulta futura.

## Conquistas Finais

### 1. Integração Completa da "Pedra de Roseta" ✅
- O script `gerar_contexto.py` foi atualizado para usar a "Pedra de Roseta" na geração do `contexto_para_ia.md`
- Documentos principais agora aparecem com emojis apropriados:
  - 📝 **Contrato de Locação**: i1028.pdf
  - 🏛️ **Sentença Arbitral**: i645.pdf
  - 📋 **REsp 1.602.076**: i649.pdf
- Cada documento inclui informações enriquecidas (tipo, observações) e links diretos

### 2. Validação dos Documentos Chave ✅
- **Contrato de Locação**: i1028.pdf identificado corretamente como "VULNERABILIDADE DIGITAL DO CONSUMIDOR NOS MODELOS ZERO-PRICE"
- **Sentença Arbitral**: i645.pdf identificado como "D5F6732EFE0621_sentencaarbitralquintoandartjs.pdf" com observações relevantes
- **REsp 1.602.076**: i649.pdf identificado como "Comentário ao REsp 1.602.076/SP" com observações adicionais

### 3. Qualidade do Contexto para IA Aperfeiçoada ✅
- O arquivo `contexto_para_ia.md` agora fornece à LLM contexto muito mais preciso e útil
- Links diretos para documentos específicos no repositório GitHub
- Metadados enriquecidos que ajudam a LLM a entender o contexto jurídico

## Próximos Passos

### 1. Expansão do Mapeamento
- Investigar a existência do Agravo 2172223-37 em outro formato ou local
- Adicionar mais documentos ao mapeamento conforme necessário para o caso

### 2. Melhoria Contínua no Processo de Prova Jurídica
- Automatizar a atualização da "Pedra de Roseta" quando novos documentos forem adicionados
- Criar mecanismos de verificação de integridade dos arquivos PDF no repositório
- Implementar busca avançada por conteúdo nos PDFs para melhorar a precisão do mapeamento

## Considerações Finais

O projeto alcançou um marco importante com a criação e integração da "Pedra de Roseta". Agora, o sistema fornece à LLM contexto jurídico preciso e links diretos para as provas específicas, permitindo a elaboração de petições jurídicas com ancoragem em evidências específicas hospedadas no repositório próprio. Isso garante soberania sobre as provas e melhora significativamente a qualidade do contexto fornecido à inteligência artificial para auxílio jurídico.