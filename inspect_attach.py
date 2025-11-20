import sqlite3
import os
import shutil

original_db = "/home/peixoto/Zotero/zotero.sqlite"
temp_db = "zotero_temp_attach.sqlite"

if os.path.exists(original_db):
    shutil.copy2(original_db, temp_db)

try:
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(itemAttachments)")
    columns = cursor.fetchall()
    for col in columns:
        print(col)
    conn.close()
except Exception as e:
    print(e)
finally:
    if os.path.exists(temp_db):
        os.remove(temp_db)
