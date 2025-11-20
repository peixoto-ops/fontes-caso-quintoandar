#!/usr/bin/env python3
"""
Script para identificar os IDs dos arquivos que realmente pertencem à coleção específica
"""
import subprocess
import re
import sys

def obter_ids_da_colecao(regex_colecao):
    """Obtém os IDs dos arquivos da coleção específica usando zotsite print"""
    try:
        result = subprocess.run(['zotsite', 'print', '--collection', regex_colecao], 
                                capture_output=True, text=True, check=True)
        output = result.stdout
        
        # Extrai IDs dos itens da coleção (procura por padrões como: i123.pdf ou i123) (Item))
        ids = set()
        
        for line in output.split('\n'):
            # Procura IDs em PDF attachments
            pdf_matches = re.findall(r'i(\d+)\.pdf', line)
            ids.update(pdf_matches)
            
            # Procura IDs em itens
            item_matches = re.findall(r'i(\d+)\) \(Item\)', line)
            ids.update(item_matches)
            
            # Procura IDs em outros formatos possíveis
            other_matches = re.findall(r'i(\d+)(?:\.html)?\s+', line)
            ids.update(other_matches)
        
        return ids
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar zotsite print: {e}")
        return set()

def main():
    # Regex da coleção configurada
    regex_colecao = ".*Senten.a Arbitral.*Caso Quinto Andar.*"
    
    print("Obtendo IDs da coleção...")
    ids_permitidos = obter_ids_da_colecao(regex_colecao)
    
    if not ids_permitidos:
        print("Nenhum ID encontrado na coleção. Verifique o regex.")
        return
    
    print(f"Encontrados {len(ids_permitidos)} IDs na coleção")
    print("IDs encontrados:", sorted(list(ids_permitidos)))
    
    # Salva os IDs em um arquivo para uso posterior
    with open('/tmp/ids_colecao_permitidos.txt', 'w') as f:
        for id_val in sorted(ids_permitidos):
            f.write(id_val + '\n')
    
    print(f"\nIDs salvos em /tmp/ids_colecao_permitidos.txt")

if __name__ == "__main__":
    main()