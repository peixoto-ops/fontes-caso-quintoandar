import sqlite3
import os

db_path = "zotero_temp.sqlite"
if not os.path.exists(db_path):
    print(f"Banco de dados não encontrado: {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT collectionName FROM collections")
    rows = cursor.fetchall()
    print("Coleções encontradas:")
    for row in rows:
        print(f"- {row[0]}")
    conn.close()
except Exception as e:
    print(f"Erro ao ler banco: {e}")
