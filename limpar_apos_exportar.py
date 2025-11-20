#!/usr/bin/env python3
"""
Script para limpar o diretório de exportação mantendo apenas os arquivos 
que fazem parte da coleção específica do Zotero.
"""
import os
import re
import subprocess
import tempfile

def obter_ids_da_colecao(regex_colecao):
    """Obtém os IDs dos arquivos da coleção específica usando zotsite print"""
    try:
        result = subprocess.run(['zotsite', 'print', '--collection', regex_colecao], 
                                capture_output=True, text=True, check=True)
        output = result.stdout
        
        # Extrai IDs dos itens da coleção
        ids = set()
        
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

def limpar_diretorio_storage(diretorio_storage, ids_permitidos):
    """Remove arquivos do diretório storage que não estão na lista de IDs permitidos"""
    if not os.path.exists(diretorio_storage):
        print(f"Diretório {diretorio_storage} não encontrado")
        return
    
    arquivos_removidos = 0
    arquivos_permitidos = 0
    
    for filename in os.listdir(diretorio_storage):
        # Verifica se é um arquivo PDF ou HTML que segue o padrão i123.pdf ou i123.html
        match = re.match(r'i(\d+)\.(pdf|html)$', filename)
        if match:
            id_arquivo = match.group(1)

            if id_arquivo not in ids_permitidos:
                filepath = os.path.join(diretorio_storage, filename)
                os.remove(filepath)
                print(f"Removido: {filename}")
                arquivos_removidos += 1
            else:
                print(f"Mantido: {filename}")
                arquivos_permitidos += 1
        else:
            # Verifica se é outro tipo de arquivo que pode estar relacionado à coleção
            # Por exemplo, arquivos com nomes como i123456789.html (longos que podem ser snapshots)
            other_match = re.match(r'i([a-zA-Z0-9]+)\.html$', filename)
            if other_match:
                # Para arquivos HTML com IDs mais longos, verificamos se algum dos IDs da coleção
                # está contido no nome do arquivo (alguns snapshots podem ter IDs extendidos)
                is_related = any(id_permitido in filename for id_permitido in ids_permitidos)
                if is_related:
                    print(f"Mantido (snapshot relacionado): {filename}")
                    arquivos_permitidos += 1
                else:
                    filepath = os.path.join(diretorio_storage, filename)
                    os.remove(filepath)
                    print(f"Removido (snapshot não relacionado): {filename}")
                    arquivos_removidos += 1
    
    print(f"\nResumo: {arquivos_permitidos} arquivos mantidos, {arquivos_removidos} arquivos removidos")
    
    # Retorna o número total de arquivos após a limpeza
    total_restantes = len([f for f in os.listdir(diretorio_storage) if re.match(r'i\d+\.', f)])
    return total_restantes

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
    
    # Diretório storage padrão (assumindo que estamos na pasta de destino)
    diretorio_storage = "storage"
    
    if not os.path.exists(diretorio_storage):
        print(f"Diretório {diretorio_storage} não encontrado")
        return
    
    print(f"\nLimpando diretório {diretorio_storage}...")
    total_restantes = limpar_diretorio_storage(diretorio_storage, ids_permitidos)
    
    print(f"\nLimpeza concluída! {total_restantes} arquivos restantes no storage.")
    
    # Salvar lista de arquivos mantidos para verificação
    with open('arquivos_mantidos.log', 'w') as f:
        for filename in os.listdir(diretorio_storage):
            if re.match(r'i\d+\.', filename):
                f.write(filename + '\n')

if __name__ == "__main__":
    main()