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

    # Keywords para buscar
    keywords = [
        "Contrato",
        "Sentença", 
        "Agravo",
        "2172223-37",
        "1.602.076",
        "Franquia",
        "Laudo"
    ]

    print("--- 🔍 Buscando Documentos no Zotero ---")

    for keyword in keywords:
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
        rows = cursor.fetchall()
        
        if rows:
            print(f"\n📂 Resultados para '{keyword}':")
            for row in rows:
                item_id = row[0]
                title = row[1]
                # Verifica se existe arquivo correspondente no formato provável
                # O zotsite ou zotero podem usar a chave do anexo ou do pai.
                # Vamos listar apenas o ID e Título por enquanto.
                print(f"   🔹 ID: {item_id} | Título: {title}")
                # Tenta prever o nome do arquivo (zotsite costuma usar ID do anexo, mas vamos ver)

    conn.close()

except Exception as e:
    print(f"❌ Erro ao ler banco: {e}")

finally:
    if os.path.exists(temp_db):
        os.remove(temp_db)
