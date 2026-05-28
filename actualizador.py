import sqlite3
from supabase import create_client

# Configuración
supabase = create_client("TU_URL", "TU_KEY")
db_path = "productos.db"

def sincronizar():
    # 1. Traer datos de Supabase
    data = supabase.table("productos").select("*").execute().data
    
    # 2. Conectar a tu base local
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 3. Actualizar la tabla local
    for prod in data:
        cursor.execute("UPDATE Productos SET Stock = ? WHERE Nombre = ?", 
                       (prod['stock'], prod['nombre']))
    
    conn.commit()
    conn.close()
    print("¡Base de datos local actualizada con Supabase!")

sincronizar()
