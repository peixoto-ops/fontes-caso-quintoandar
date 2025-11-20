import sqlite3
import os
import shutil

original_db = "/home/peixoto/Zotero/zotero.sqlite"
temp_db = "zotero_temp_tables.sqlite"

if os.path.exists(original_db):
    shutil.copy2(original_db, temp_db)

try:
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])
    conn.close()
except Exception as e:
    print(e)
finally:
    if os.path.exists(temp_db):
        os.remove(temp_db)
