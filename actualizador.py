import sqlite3
import os
from supabase import create_client

# 1. Usamos variables de entorno para mayor seguridad (ya no pegues tu clave aquí)
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def sincronizar_db():
    # Obtener datos
    response = supabase.table("Productos").select("*").execute()
    data = response.data
    
    # Conectar y actualizar localmente
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Productos")
    
    datos_a_insertar = [(p['ProductoId'], p['Nombre'], p['Precio'], p['Stock'], p['CategoriaId']) for p in data]
    cursor.executemany("INSERT INTO Productos VALUES (?, ?, ?, ?, ?)", datos_a_insertar)
    
    conn.commit()
    conn.close()
    print("Base de datos local actualizada.")

if __name__ == "__main__":
    sincronizar_db()
