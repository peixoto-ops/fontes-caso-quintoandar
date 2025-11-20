import sqlite3
import os
import shutil

# Caminho do banco de dados
original_db = "/home/peixoto/Zotero/zotero.sqlite"
temp_db = "zotero_temp_schema.sqlite"

# Copia o banco
if os.path.exists(original_db):
    shutil.copy2(original_db, temp_db)
else:
    print(f"❌ Banco de dados não encontrado: {original_db}")
    exit(1)

try:
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    print("--- 📊 Colunas da Tabela 'items' ---")
    cursor.execute("PRAGMA table_info(items)")
    columns = cursor.fetchall()
    for col in columns:
        print(col)

    conn.close()

except Exception as e:
    print(f"❌ Erro ao ler banco: {e}")

finally:
    if os.path.exists(temp_db):
        os.remove(temp_db)
