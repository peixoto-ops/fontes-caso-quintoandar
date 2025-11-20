import sqlite3
import os
import shutil

# Caminho do banco de dados
original_db = "/home/peixoto/Zotero/zotero.sqlite"
temp_db = "zotero_temp_final.sqlite"

# Copia o banco
if os.path.exists(original_db):
    shutil.copy2(original_db, temp_db)
else:
    print(f"❌ Banco de dados não encontrado: {original_db}")
    exit(1)

try:
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    # Keywords para buscar
    keywords = [
        "Contrato de Locação",
        "Sentença Arbitral", 
        "2172223",
        "1.602.076",
        "Franquia",
        "QuintoAndar"
    ]

    print("--- 🔍 Mapeamento de Documentos Zotero ---")
    print("ID do Anexo -> Título do Pai (Nome do arquivo original)")

    for keyword in keywords:
        print(f"\n🔎 Buscando por: '{keyword}'")
        
        # Busca o ID do item pai pelo título
        query = f"""
        SELECT items.itemID, itemDataValues.value 
        FROM items 
        JOIN itemData ON items.itemID = itemData.itemID 
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID 
        JOIN fields ON itemData.fieldID = fields.fieldID 
        WHERE fields.fieldName = 'title' 
        AND itemDataValues.value LIKE ?
        """
        cursor.execute(query, (f'%{keyword}%',))
        parents = cursor.fetchall()
        
        if not parents:
            print("   ❌ Nenhum item encontrado.")
            continue

        for parent in parents:
            parent_id = parent[0]
            title = parent[1]
            
            # Busca anexos na tabela itemAttachments
            attach_query = "SELECT itemID, path FROM itemAttachments WHERE parentItemID = ?"
            cursor.execute(attach_query, (parent_id,))
            children = cursor.fetchall()
            
            if children:
                for child in children:
                    child_id = child[0]
                    path = child[1]
                    # Limpa o path se tiver prefixo storage:
                    if path and path.startswith("storage:"):
                        path = path.replace("storage:", "")
                    
                    print(f"   ✅ i{child_id}.pdf  <--  {title} (Original: {path})")
            else:
                # Se não tem anexo, pode ser que o próprio item seja o PDF? (Raro no Zotero)
                print(f"   ⚠️ [ID {parent_id}] {title} (Sem anexos detectados)")

    conn.close()

except Exception as e:
    print(f"❌ Erro ao ler banco: {e}")

finally:
    if os.path.exists(temp_db):
        os.remove(temp_db)
