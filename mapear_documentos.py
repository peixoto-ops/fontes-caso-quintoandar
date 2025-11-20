import sqlite3
import os
import shutil

# Caminho do banco de dados
original_db = "/home/peixoto/Zotero/zotero.sqlite"
temp_db = "zotero_temp_map.sqlite"

# Copia o banco para evitar travamento
if os.path.exists(original_db):
    shutil.copy2(original_db, temp_db)
else:
    print(f"❌ Banco de dados não encontrado: {original_db}")
    exit(1)

try:
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    # Verifica colunas da tabela items
    cursor.execute("PRAGMA table_info(items)")
    columns = [col[1] for col in cursor.fetchall()]
    has_parent = 'parentItemID' in columns
    
    # Keywords para buscar
    keywords = [
        "Contrato de Locação",
        "Sentença Arbitral", 
        "2172223-37",
        "1.602.076",
        "Franquia"
    ]

    print("--- 🔍 Buscando Documentos no Zotero ---")

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
            print(f"   📄 Documento Pai: [ID {parent_id}] {title}")

            # Busca anexos (filhos)
            if has_parent:
                # Busca itens que tem este pai
                # Geralmente anexos são do tipo 'attachment' (itemTypeID=2)
                # Mas vamos pegar qualquer filho
                child_query = "SELECT itemID FROM items WHERE parentItemID = ?"
                cursor.execute(child_query, (parent_id,))
                children = cursor.fetchall()
                
                if children:
                    for child in children:
                        child_id = child[0]
                        # Tenta pegar o nome do arquivo do anexo
                        # O nome do arquivo fica em itemData com fieldID correspondente a 'filename' ou similar?
                        # Ou path?
                        # Vamos tentar pegar qualquer valor de dados para esse filho
                        data_query = """
                        SELECT fields.fieldName, itemDataValues.value
                        FROM itemData
                        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
                        JOIN fields ON itemData.fieldID = fields.fieldID
                        WHERE itemData.itemID = ?
                        """
                        cursor.execute(data_query, (child_id,))
                        data_rows = cursor.fetchall()
                        
                        filename = "Desconhecido"
                        for row in data_rows:
                            if row[0] == "filename" or row[0] == "path":
                                filename = row[1]
                        
                        print(f"      📎 Anexo: [ID {child_id}] -> Provável arquivo: i{child_id}.pdf (Nome original: {filename})")
                else:
                    print("      ⚠️ Sem anexos encontrados.")
            else:
                print("      ⚠️ Tabela items sem coluna parentItemID (Schema diferente).")

    conn.close()

except Exception as e:
    print(f"❌ Erro ao ler banco: {e}")

finally:
    if os.path.exists(temp_db):
        os.remove(temp_db)
