# Project Summary

## Overall Goal
Criar um site estático do GitHub Pages que contenha apenas os documentos jurídicos relevantes da coleção específica "Sentença Arbitral - Caso Quinto Andar", filtrando-os de toda a biblioteca do Zotero, e gerar contexto enriquecido para LLMs.

## Key Knowledge
- O projeto utiliza `zotsite` para exportar coleções específicas do Zotero para um site estático
- Regex utilizado para filtragem: `REGEX_COLECAO=".*Senten.a Arbitral.*Caso Quinto Andar.*"`
- O script `publicar.sh` automatiza o processo de exportação, filtragem e publicação
- A "Pedra de Roseta" (arquivo `pedra_de_rosseta.json`) mapeia IDs de arquivos aos documentos jurídicos específicos
- Documentos principais identificados: i1028.pdf (Contrato de Locação), i645.pdf (Sentença Arbitral), i649.pdf (REsp 1.602.076)
- O GitHub Pages está configurado para servir do branch `gh-pages`
- Arquivos mantidos após filtragem: 73 arquivos (exclusivamente da coleção específica)
- Arquivos removidos: 95 arquivos (conteúdo indesejado de outras coleções)

## Recent Actions
- [DONE] Identificado problema: site continha conteúdo de toda a biblioteca Zotero em vez de apenas da coleção específica
- [DONE] Investigado e corrigido a sintaxe do parâmetro `collection` do zotsite
- [DONE] Desenvolvido script de filtragem que identifica os 149 IDs corretos da coleção e mantém apenas os 73 arquivos relacionados
- [DONE] Reset completo do branch `gh-pages` e reconstrução limpa com conteúdo filtrado
- [DONE] Deploy bem-sucedido para o branch `gh-pages` com apenas os documentos corretos
- [DONE] Implementado script `limpar_apos_exportar.py` que remove arquivos que não pertencem à coleção específica
- [DONE] Atualizado o script `publicar.sh` para incluir etapa de limpeza pós-exportação

## Current Plan
- [DONE] Site contendo apenas os 73 arquivos corretos da coleção específica está publicado em https://peixoto-ops.github.io/fontes-caso-quintoandar/
- [DONE] Documentos principais (contrato, sentença, REsp) mantidos e acessíveis
- [DONE] Snapshots HTML relacionados mantidos para resiliência e acesso offline
- [DONE] Script `gerar_contexto.py` atualizado para gerar contexto com base nos documentos filtrados
- [DONE] Configuração do GitHub Pages confirmada para usar o branch `gh-pages` com conteúdo limpo

---

## Summary Metadata
**Update time**: 2025-11-20T21:54:42.589Z 
