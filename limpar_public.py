#!/usr/bin/env python3
"""
Script para limpar o diretório public mantendo apenas os arquivos 
que fazem parte da coleção específica do Zotero.
"""
import os
import re
import subprocess
import json
import tempfile

def obter_ids_da_colecao(regex_colecao):
    """Obtém os IDs dos arquivos da coleção específica usando zotsite print"""
    try:
        result = subprocess.run(['zotsite', 'print', '--collection', regex_colecao], 
                                capture_output=True, text=True, check=True)
        output = result.stdout
        
        # Extrai IDs dos itens da coleção
        ids = set()
        
        # Procura por padrões como i123.pdf ou i123) (Item)
        for line in output.split('\n'):
            # Procura IDs em PDF attachments
            pdf_matches = re.findall(r'i(\d+)\.pdf', line)
            ids.update(pdf_matches)
            
            # Procura IDs em itens
            item_matches = re.findall(r'i(\d+)\) \(Item\)', line)
            ids.update(item_matches)
        
        return ids
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar zotsite print: {e}")
        return set()

def limpar_diretorio_storage(public_dir, ids_permitidos):
    """Remove arquivos do diretório storage que não estão na lista de IDs permitidos"""
    storage_dir = os.path.join(public_dir, 'storage')
    
    if not os.path.exists(storage_dir):
        print(f"Diretório {storage_dir} não encontrado")
        return
    
    arquivos_removidos = 0
    arquivos_permitidos = 0
    
    for filename in os.listdir(storage_dir):
        if filename.endswith('.pdf'):
            # Extrai o número do ID do nome do arquivo (ex: i123.pdf -> 123)
            match = re.match(r'i(\d+)\.pdf', filename)
            if match:
                id_arquivo = match.group(1)
                
                if id_arquivo not in ids_permitidos:
                    filepath = os.path.join(storage_dir, filename)
                    os.remove(filepath)
                    print(f"Removido: {filename}")
                    arquivos_removidos += 1
                else:
                    print(f"Permitido: {filename}")
                    arquivos_permitidos += 1
    
    print(f"\nResumo: {arquivos_permitidos} arquivos mantidos, {arquivos_removidos} arquivos removidos")

def main():
    # Regex da coleção configurada
    regex_colecao = ".*Senten.a Arbitral.*Caso Quinto Andar.*"
    
    print("Obtendo IDs da coleção...")
    ids_permitidos = obter_ids_da_colecao(regex_colecao)
    
    if not ids_permitidos:
        print("Nenhum ID encontrado na coleção. Verifique o regex.")
        return
    
    print(f"Encontrados {len(ids_permitidos)} IDs na coleção")
    print(f"IDs: {sorted(list(ids_permitidos))}")
    
    # Diretório public
    public_dir = "public"
    
    if not os.path.exists(public_dir):
        print(f"Diretório {public_dir} não encontrado")
        return
    
    print(f"\nLimpando diretório {public_dir}/storage...")
    limpar_diretorio_storage(public_dir, ids_permitidos)
    
    print("\nLimpeza concluída!")

if __name__ == "__main__":
    main()